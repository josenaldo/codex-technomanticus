---
title: "Spring Data JPA"
created: 2026-04-11
updated: 2026-04-11
type: concept
status: evergreen
tags:
  - java
  - backend
  - persistencia
  - entrevista
publish: false
---

# Spring Data JPA

Deep dive em persistência na stack Spring — **JPA**, **Hibernate**, **Spring Data repositories**, **transações**, **fetch strategies**, **N+1**, **caching**, **performance tuning**. Para fundamentos gerais de banco de dados (SQL, NoSQL, ACID, índices, sharding), ver [[Banco de dados]]. Para concorrência em transações, ver [[Java Concurrency]]. Para troubleshooting em produção, ver [[Spring Boot]] (seção Troubleshooting).

## O que é

**JPA (Jakarta Persistence API)** — especificação Java para ORM (Object-Relational Mapping). Define anotações (`@Entity`, `@Id`, `@OneToMany`) e API para gerenciar objetos persistentes.

**Hibernate** — a implementação mais popular de JPA. Tem features além da spec (natural IDs, dynamic updates, query cache). É o que você usa 99% do tempo quando usa "JPA".

**Spring Data JPA** — camada sobre JPA/Hibernate que elimina boilerplate de repositories, queries derivadas de nomes de métodos, paginação, auditoria, specifications.

```
┌─────────────────────────────────┐
│  Seu código                     │
├─────────────────────────────────┤
│  Spring Data JPA                │  ← repositories, derived queries
├─────────────────────────────────┤
│  JPA (Jakarta Persistence API)  │  ← anotações, EntityManager
├─────────────────────────────────┤
│  Hibernate                      │  ← implementação
├─────────────────────────────────┤
│  JDBC                           │  ← driver do banco
├─────────────────────────────────┤
│  PostgreSQL / MySQL / ...       │
└─────────────────────────────────┘
```

Em entrevistas, o que diferencia um senior em JPA/Hibernate:

1. **Entender fetch strategies e N+1** — o bug mais caro de JPA
2. **Dominar `@Transactional`** — propagation, isolation, rollback rules, self-invocation
3. **Escolher entre entity, projection e DTO** — cada um tem use case
4. **Saber quando NÃO usar JPA** — queries analíticas, bulk updates, tight SQL
5. **Conhecer Hibernate Session** — 1st level cache, flush, dirty checking, detached entities
6. **Optimistic vs Pessimistic locking**
7. **Query tuning** — `EXPLAIN ANALYZE`, índices, batch fetching
8. **Migrations seguras** (Flyway) — expand-and-contract

---

## Entidades JPA

Uma classe Java anotada com `@Entity` mapeia para uma tabela no banco.

### Anatomia básica

```java
import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "patients")
public class Patient {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "full_name", nullable = false, length = 200)
    private String name;

    @Column(unique = true, nullable = false)
    private String email;

    @Column(name = "birth_date")
    private LocalDate birthDate;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private PatientStatus status = PatientStatus.ACTIVE;

    @CreatedDate
    @Column(name = "created_at", updatable = false)
    private Instant createdAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    private Instant updatedAt;

    @Version
    private Long version;  // optimistic locking

    // JPA exige construtor sem argumentos (pode ser protected)
    protected Patient() {}

    public Patient(String name, String email, LocalDate birthDate) {
        this.name = name;
        this.email = email;
        this.birthDate = birthDate;
    }

    // Getters, setters, equals, hashCode...
}
```

### Estratégias de ID generation

| Estratégia | Como funciona | Quando usar |
| --- | --- | --- |
| **`IDENTITY`** | DB gera ao INSERT (auto-increment) | MySQL; **não permite batching** |
| **`SEQUENCE`** | Usa `SEQUENCE` do banco (PostgreSQL, Oracle) | **Default recomendado** — permite batching |
| **`TABLE`** | Tabela separada para gerar IDs | Compatibilidade máxima, mas lento |
| **`AUTO`** | Hibernate decide | Evite — explicite |
| **`UUID`** | Java gera UUID | IDs distribuídos, sem coordenação |

**Armadilha com `IDENTITY`:** Hibernate precisa fazer INSERT imediatamente para obter o ID, impedindo batch inserts. Para workloads write-heavy, prefira `SEQUENCE`:

```java
@Id
@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "patient_seq")
@SequenceGenerator(name = "patient_seq", sequenceName = "patient_seq", allocationSize = 50)
private Long id;
```

`allocationSize=50` é importante — Hibernate pega 50 IDs de cada vez, reduzindo roundtrips ao banco.

### Entity com Record? Não.

**Records NÃO funcionam bem como `@Entity`** porque:

- Records são imutáveis (fields `final`), mas JPA exige setters para lazy loading funcionar
- JPA exige construtor sem argumentos — records não têm (exceto um compact constructor)

**Solução:** use records para **DTOs** e **projections**, não para entities.

### equals/hashCode em entities — o cuidado crítico

**Nunca use IDs gerados em equals/hashCode antes da persistência**, porque o ID é `null`.

```java
// RUIM — @Data do Lombok ou auto-gerado com todos os campos
@Entity
@Data  // PERIGO
public class Patient {
    @Id @GeneratedValue private Long id;
    @OneToMany private List<Appointment> appointments;  // lazy
    // equals chama appointments.equals() → LazyInitializationException
}

// RUIM — equals por ID (null antes do save)
@Override
public boolean equals(Object o) {
    return o instanceof Patient p && Objects.equals(id, p.id);
}
// Patient antes do save + Patient depois do save de outro objeto podem dar true
```

**Regras:**

1. **Use business key** — campo imutável e único (email, CPF, UUID)
2. **Se não tiver business key, use UUID gerado no construtor**
3. **Nunca use `@Data` em entities**
4. **`@ToString` deve excluir relações** ou você terá lazy loading exception
5. **Consistência:** hashCode deve ser estável — não pode mudar durante o lifecycle

```java
@Entity
public class Patient {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    private Long id;

    @Column(unique = true, nullable = false, updatable = false)
    private String externalId = UUID.randomUUID().toString();  // business key

    // ... outros campos

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Patient other)) return false;
        return Objects.equals(externalId, other.externalId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(externalId);
    }
}
```

### Natural IDs (Hibernate-specific)

Se você tem um campo naturalmente único (CPF, email), marque como `@NaturalId` — Hibernate otimiza buscas.

```java
@Entity
public class Patient {
    @Id @GeneratedValue private Long id;

    @NaturalId(mutable = false)
    @Column(nullable = false, unique = true, updatable = false)
    private String cpf;
}

// Uso — mais rápido que find por ID em alguns casos
Patient p = session.byNaturalId(Patient.class)
    .using("cpf", "12345678900")
    .load();
```

---

## Relacionamentos

### @OneToMany / @ManyToOne

Relação um-para-muitos. O `@ManyToOne` é o **owning side** (tem a foreign key).

```java
@Entity
public class Doctor {

    @Id @GeneratedValue private Long id;
    private String name;

    @OneToMany(mappedBy = "doctor", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Appointment> appointments = new ArrayList<>();

    // Helper para manter ambos os lados sincronizados
    public void addAppointment(Appointment a) {
        appointments.add(a);
        a.setDoctor(this);
    }

    public void removeAppointment(Appointment a) {
        appointments.remove(a);
        a.setDoctor(null);
    }
}

@Entity
public class Appointment {

    @Id @GeneratedValue private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "doctor_id")
    private Doctor doctor;
}
```

**Pontos cruciais:**

- **`mappedBy`** indica que Doctor NÃO é o owning side — Appointment é
- **`cascade = ALL`** propaga operações (save, delete) do pai para os filhos
- **`orphanRemoval = true`** — quando um appointment é removido da lista, é deletado do banco
- **`fetch = LAZY`** — default para `@OneToMany` e `@ManyToMany`, mas EAGER para `@ManyToOne` e `@OneToOne` (cuidado!)
- **Helper methods** mantêm ambos os lados sincronizados — essencial para consistência

### @ManyToMany

Evite em modelagem rica — frequentemente esconde uma entidade de associação que merece existir.

```java
// MINIMAL
@ManyToMany
@JoinTable(
    name = "patient_tags",
    joinColumns = @JoinColumn(name = "patient_id"),
    inverseJoinColumns = @JoinColumn(name = "tag_id")
)
private Set<Tag> tags = new HashSet<>();
```

**Melhor: criar entidade associativa explícita** quando você precisa de campos adicionais (data, quantidade, status).

```java
@Entity
public class PatientAllergy {
    @Id @GeneratedValue private Long id;

    @ManyToOne private Patient patient;
    @ManyToOne private Allergy allergy;

    private Severity severity;
    private LocalDate diagnosedAt;
    private String notes;
}
```

### @OneToOne

Um-para-um. Duas variantes:

```java
// Com foreign key compartilhada
@Entity
public class User {
    @Id @GeneratedValue private Long id;

    @OneToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    @JoinColumn(name = "profile_id")
    private Profile profile;
}
```

**Cuidado:** `@OneToOne` com lazy loading é problemático em JPA — o proxy não funciona bem sem `@MapsId` ou `@LazyToOne(NO_PROXY)` + bytecode enhancement. Muitos preferem modelar como `@ManyToOne` no lado "filho".

---

## Fetch strategies

A decisão mais importante em JPA — como e quando Hibernate busca dados relacionados.

### LAZY vs EAGER

**EAGER** — dados carregados junto com o pai. Simples, mas performance ruim.

**LAZY** — dados só carregados quando acessados. Melhor performance, mas pode causar `LazyInitializationException` fora da sessão.

**Defaults do JPA:**

| Relação | Default |
| --- | --- |
| `@ManyToOne` | **EAGER** (!) |
| `@OneToOne` | EAGER |
| `@OneToMany` | LAZY |
| `@ManyToMany` | LAZY |

**Problema:** `@ManyToOne` EAGER é responsável por MUITOS problemas de performance. Uma entidade com 5 @ManyToOne carrega 5 JOINs em toda query, mesmo quando você não precisa.

**Regra prática: SEMPRE LAZY.**

```java
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "doctor_id")
private Doctor doctor;
```

### N+1: o bug mais caro

O problema mais comum em JPA. Acontece quando você carrega N entidades e depois itera acessando uma relação lazy — causa 1 query para o pai + N queries para os filhos.

```java
// BUG — causa N+1
List<Doctor> doctors = doctorRepo.findAll();          // 1 query
for (Doctor d : doctors) {
    System.out.println(d.getAppointments().size());   // N queries (1 por doctor)
}
// Total: N+1 queries
```

**Como detectar:**

```yaml
# application.yml — ver queries no log
spring:
  jpa:
    show-sql: true
    properties:
      hibernate:
        format_sql: true
        generate_statistics: true

logging:
  level:
    org.hibernate.SQL: DEBUG
    org.hibernate.stat: DEBUG
```

**Em testes:** ferramenta [nplusone](https://github.com/spring-cloud/spring-cloud-kubernetes) lança exceção em dev se detectar N+1.

### Soluções para N+1

**1. JOIN FETCH (JPQL)** — força a carga das relações na mesma query:

```java
@Query("SELECT d FROM Doctor d JOIN FETCH d.appointments WHERE d.active = true")
List<Doctor> findActiveDoctorsWithAppointments();
```

**Cuidado:** só funciona com UMA coleção por query. Múltiplas coleções causam "cartesian product" problem.

**2. @EntityGraph (declarativo)** — preferido para casos comuns:

```java
public interface DoctorRepository extends JpaRepository<Doctor, Long> {

    @EntityGraph(attributePaths = {"appointments", "specialty"})
    List<Doctor> findByActiveTrue();

    // Named entity graph
    @EntityGraph(value = "Doctor.withAppointmentsAndSpecialty")
    Optional<Doctor> findById(Long id);
}

@Entity
@NamedEntityGraph(
    name = "Doctor.withAppointmentsAndSpecialty",
    attributeNodes = {
        @NamedAttributeNode("appointments"),
        @NamedAttributeNode("specialty")
    }
)
public class Doctor { ... }
```

**3. @BatchSize** — em vez de 1 query por parent, Hibernate batches N parents:

```java
@Entity
public class Doctor {

    @OneToMany(mappedBy = "doctor")
    @BatchSize(size = 20)  // carrega até 20 relações por query
    private List<Appointment> appointments;
}
```

**4. DTO Projection** — bypassa entities completamente, melhor performance:

```java
public record DoctorSummary(String name, String specialty, long appointmentCount) {}

@Query("""
    SELECT new com.app.dto.DoctorSummary(d.name, d.specialty.name, COUNT(a))
    FROM Doctor d LEFT JOIN d.appointments a
    WHERE d.active = true
    GROUP BY d.id, d.name, d.specialty.name
    """)
List<DoctorSummary> findDoctorSummaries();
```

**5. Fetch join com pagination — cuidado:**

`JOIN FETCH` + `Pageable` gera warning "HHH000104: firstResult/maxResults specified with collection fetch; applying in memory". O Hibernate carrega TUDO e pagina em memória. Use DTO projection ou subquery.

---

## Spring Data Repositories

### JpaRepository

Interface básica com operações CRUD e paginação:

```java
public interface PatientRepository extends JpaRepository<Patient, Long> {
    // CRUD já herdado: save, findById, findAll, delete, count, existsById...
}
```

Hierarquia:

```
Repository
  └─ CrudRepository (save, findById, delete, ...)
       └─ PagingAndSortingRepository (paginação, sorting)
            └─ JpaRepository (flush, saveAndFlush, deleteInBatch, ...)
```

### Derived queries (queries por nome do método)

Spring Data gera SQL a partir do nome do método.

```java
public interface PatientRepository extends JpaRepository<Patient, Long> {

    Optional<Patient> findByEmail(String email);

    List<Patient> findBySpecialtyAndActiveTrue(String specialty);

    List<Patient> findByAgeGreaterThanEqualOrderByNameAsc(int age);

    long countByActiveTrue();

    boolean existsByCpf(String cpf);

    void deleteByEmailContaining(String fragment);

    // Com pagination
    Page<Patient> findByActiveTrue(Pageable pageable);

    // Retornando stream (cuidado — deixe a tx aberta)
    @QueryHints(@QueryHint(name = HINT_FETCH_SIZE, value = "100"))
    Stream<Patient> findAllBy();
}
```

**Keywords suportadas:** `And`, `Or`, `Is`, `Equals`, `Between`, `LessThan`, `GreaterThan`, `After`, `Before`, `IsNull`, `IsNotNull`, `Like`, `NotLike`, `StartingWith`, `EndingWith`, `Containing`, `OrderBy`, `Not`, `In`, `NotIn`, `True`, `False`, `IgnoreCase`, ...

**Limite:** derived queries ficam ilegíveis rápido. Para qualquer coisa além do básico, use `@Query`.

### @Query — JPQL e native

**JPQL (Java Persistence Query Language)** — parecido com SQL mas usa nomes de entidades e atributos Java, não tabelas/colunas.

```java
@Query("SELECT p FROM Patient p WHERE p.active = true AND p.age > :minAge")
List<Patient> findActiveOverAge(@Param("minAge") int minAge);

// Com LIMIT via pagination
@Query("SELECT p FROM Patient p ORDER BY p.createdAt DESC")
List<Patient> findRecent(Pageable pageable);  // passar PageRequest.of(0, 10)
```

**Native SQL** — quando JPQL não basta:

```java
@Query(value = """
    SELECT p.*,
           ts_rank(to_tsvector('portuguese', p.name), to_tsquery(:query)) as rank
    FROM patients p
    WHERE to_tsvector('portuguese', p.name) @@ to_tsquery(:query)
    ORDER BY rank DESC
    LIMIT 20
    """, nativeQuery = true)
List<Patient> fullTextSearch(@Param("query") String query);
```

**Modifying queries:**

```java
@Modifying
@Query("UPDATE Patient p SET p.status = :status WHERE p.lastLoginAt < :cutoff")
int markInactive(@Param("status") PatientStatus status, @Param("cutoff") Instant cutoff);
// Retorna quantos registros foram afetados
```

**Cuidado com `@Modifying`:** invalida o 1st level cache automaticamente? **Não** — você precisa `@Modifying(clearAutomatically = true, flushAutomatically = true)`.

### Projections

Quando você só precisa de alguns campos, projeções são **muito mais rápidas** que carregar a entidade inteira.

**Interface projection:**

```java
public interface PatientSummary {
    Long getId();
    String getName();
    String getEmail();
}

public interface PatientRepository extends JpaRepository<Patient, Long> {
    List<PatientSummary> findByActiveTrue();  // Spring gera proxy
}
```

**Class-based projection (DTO, recomendado):**

```java
public record PatientDTO(Long id, String name, String email) {}

@Query("SELECT new com.app.dto.PatientDTO(p.id, p.name, p.email) FROM Patient p WHERE p.active = true")
List<PatientDTO> findActiveAsDTO();
```

**Dynamic projection:**

```java
public interface PatientRepository extends JpaRepository<Patient, Long> {
    <T> List<T> findByActiveTrue(Class<T> type);
}

// Uso
List<PatientSummary> summaries = repo.findByActiveTrue(PatientSummary.class);
List<Patient> fullEntities = repo.findByActiveTrue(Patient.class);
```

**Regra prática:** use projections para listagens. Use entities quando precisa modificar.

### Specifications (queries dinâmicas)

Para filtros dinâmicos (frequente em APIs de busca), use `Specification`:

```java
public interface PatientRepository extends JpaRepository<Patient, Long>,
                                            JpaSpecificationExecutor<Patient> {
}

public class PatientSpecs {

    public static Specification<Patient> hasName(String name) {
        return (root, query, cb) -> name == null ? null :
            cb.like(cb.lower(root.get("name")), "%" + name.toLowerCase() + "%");
    }

    public static Specification<Patient> hasSpecialty(String specialty) {
        return (root, query, cb) -> specialty == null ? null :
            cb.equal(root.get("specialty").get("name"), specialty);
    }

    public static Specification<Patient> isActive() {
        return (root, query, cb) -> cb.isTrue(root.get("active"));
    }
}

// Uso
Specification<Patient> spec = where(isActive())
    .and(hasName(request.getName()))
    .and(hasSpecialty(request.getSpecialty()));

Page<Patient> results = repo.findAll(spec, pageable);
```

**Alternativa moderna:** QueryDSL ou jOOQ para queries type-safe mais expressivas.

### Auditing

Popula automaticamente `createdAt`, `updatedAt`, `createdBy`, `updatedBy`.

```java
@SpringBootApplication
@EnableJpaAuditing(auditorAwareRef = "auditorAware")
public class App { }

@Bean
public AuditorAware<String> auditorAware() {
    return () -> {
        // Retorna o user atual (do SecurityContext)
        return Optional.ofNullable(SecurityContextHolder.getContext().getAuthentication())
            .map(Authentication::getName);
    };
}

@EntityListeners(AuditingEntityListener.class)
@MappedSuperclass
public abstract class Auditable {

    @CreatedDate
    @Column(updatable = false)
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;

    @CreatedBy
    @Column(updatable = false)
    private String createdBy;

    @LastModifiedBy
    private String updatedBy;
}

@Entity
public class Patient extends Auditable { ... }
```

---

## EntityManager e Session

Abaixo dos repositories do Spring Data, existe o `EntityManager` (JPA) ou `Session` (Hibernate).

### Persistence Context (1st level cache)

Cada transação tem um **persistence context** — cache de entities gerenciadas por ela.

```java
@Transactional
public void exemplo() {
    Patient p1 = repo.findById(1L).get();  // query SQL
    Patient p2 = repo.findById(1L).get();  // SEM query — vem do cache
    assert p1 == p2;  // mesma referência (identity)

    p1.setName("Novo Nome");
    // Não precisa chamar save()! Dirty checking detecta mudança e flush automático no commit
}
```

**Entity states:**

```
   new/transient ──persist()──► managed ──detach()──► detached
                                  │           ↓
                                  │        merge()
                                  │           │
                                  └──remove()─┘
                                       ↓
                                    removed
```

- **Transient** — novo, não conhecido pelo EM
- **Managed** — dentro do persistence context, tracking automático
- **Detached** — fora do persistence context (tx terminou)
- **Removed** — marcado para delete

### Flush

**Flush** é quando Hibernate envia comandos SQL pendentes ao banco. Acontece em:

1. **Commit da transação** (automático)
2. **Antes de queries** (para garantir consistência)
3. **Manualmente** — `em.flush()`

**Modos de flush:**

- `FlushMode.AUTO` (default) — flush antes de queries se houver mudanças pendentes
- `FlushMode.COMMIT` — flush só no commit
- `FlushMode.MANUAL` — só manual

### Dirty checking

Hibernate monitora entidades managed e, no flush, gera UPDATE para as que mudaram. Você não precisa chamar `save()` em entidades já managed.

```java
@Transactional
public void renomear(Long id, String novoNome) {
    Patient p = repo.findById(id).get();
    p.setName(novoNome);
    // Sem save() — dirty checking gera UPDATE no commit
}
```

**Quando você quer save explícito:** em entidades novas (transient → managed).

### LazyInitializationException

O erro mais comum com Hibernate. Acontece quando você tenta acessar uma relação lazy **fora da transação**.

```java
// BUG
@GetMapping("/doctors/{id}")
public Doctor get(@PathVariable Long id) {
    return repo.findById(id).get();
    // Jackson tenta serializar doctor.getAppointments() → já fora da tx → boom
}
```

**Soluções:**

1. **DTO projection** (recomendado) — retorna dados planos
2. **@EntityGraph** — força fetch da relação
3. **`@Transactional` no controller** (evite, acopla camadas)
4. **Open Session In View (OSIV)** — Spring Boot habilita por default, mas é anti-pattern

### Open Session In View — desabilite em produção

```yaml
spring:
  jpa:
    open-in-view: false  # SEMPRE false em produção
```

**Por que OSIV é ruim:**

- Mantém Session aberta durante toda request (HTTP)
- Queries N+1 que deveriam falhar em dev passam despercebidas
- Connection pool pode ser segurado pela request inteira

### Saving/merging entities

**save vs persist vs merge:**

```java
// persist — entity TRANSIENT → MANAGED
em.persist(newPatient);

// merge — detached → managed (copia estado para entity managed existente)
Patient merged = em.merge(detachedPatient);

// Spring Data save faz ambos:
// - se ID é null → persist (INSERT)
// - se ID existe → merge (SELECT + UPDATE se mudou)
repo.save(patient);
```

**Anti-pattern — `save` em entity já managed:**

```java
@Transactional
public void atualizar(Long id, String novoNome) {
    Patient p = repo.findById(id).get();  // já managed
    p.setName(novoNome);
    repo.save(p);  // desnecessário — dirty checking já faz isso
}
```

---

## Transações — @Transactional deep dive

Ver [[Spring Boot]] (seção Gerenciamento de transações) para a base conceitual. Aqui, foco em aspectos específicos de JPA.

### Transaction manager

Spring Boot autoconfigura `JpaTransactionManager` quando detecta JPA. Ele gerencia EntityManager + DataSource juntos.

### Read-only optimization

```java
@Transactional(readOnly = true)
public List<Patient> listAll() {
    return repo.findAll();
}
```

**Benefícios:**

- Hibernate **desabilita dirty checking** — não precisa fazer snapshots das entities
- Database pode otimizar (alguns DBs usam réplicas de leitura)
- **Sinaliza intenção** do código

**Padrão:** use `@Transactional(readOnly = true)` na classe de Service, sobrescreva com `@Transactional` só nos métodos que modificam:

```java
@Service
@Transactional(readOnly = true)
public class PatientService {

    public List<Patient> listAll() { ... }  // herda readOnly

    @Transactional  // sobrescreve — permite write
    public Patient create(CreatePatientRequest req) { ... }
}
```

### Optimistic locking — @Version

Evita lost updates com **versionamento otimista**. Cada entity tem um campo `@Version`:

```java
@Entity
public class Account {
    @Id @GeneratedValue private Long id;
    private BigDecimal balance;

    @Version
    private Long version;
}

// Hibernate adiciona WHERE version = ? no UPDATE
// UPDATE account SET balance = ?, version = version + 1 WHERE id = ? AND version = ?
// Se 0 rows afetadas → OptimisticLockException
```

**Uso:** evita que 2 users editando a mesma entity ao mesmo tempo sobrescrevam um ao outro.

```java
try {
    Account acc = repo.findById(id).get();
    acc.setBalance(newBalance);
    repo.save(acc);  // commit
} catch (OptimisticLockException e) {
    // Outra tx modificou entre o SELECT e o UPDATE
    // Retry ou reportar ao usuário
}
```

### Pessimistic locking

Lock explícito no banco (`SELECT ... FOR UPDATE`):

```java
public interface AccountRepository extends JpaRepository<Account, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT a FROM Account a WHERE a.id = :id")
    Optional<Account> findByIdForUpdate(@Param("id") Long id);
}

@Transactional
public void transferir(Long fromId, Long toId, BigDecimal amount) {
    Account from = repo.findByIdForUpdate(fromId).get();  // lock
    Account to = repo.findByIdForUpdate(toId).get();      // lock
    from.debitar(amount);
    to.creditar(amount);
    // Locks liberados no commit
}
```

**Cuidado com deadlocks:** sempre adquira locks na **mesma ordem** (ex.: por ID crescente).

**Quando usar:** quando conflitos são frequentes e optimistic seria retry constante.

---

## Caching

### 1st level cache (Session cache)

Automático, por transação. Já coberto acima.

### 2nd level cache (application-wide)

Cache compartilhado entre sessões. Reduz queries para entities lidas repetidamente.

```yaml
spring:
  jpa:
    properties:
      hibernate:
        cache:
          use_second_level_cache: true
          use_query_cache: true
          region:
            factory_class: org.hibernate.cache.jcache.JCacheRegionFactory
        javax:
          cache:
            provider: org.ehcache.jsr107.EhcacheCachingProvider
```

```java
@Entity
@Cacheable
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class Country {
    @Id private Long id;
    private String name;
    private String code;
}

// Query cache — para resultados de queries
@Query("SELECT c FROM Country c")
@QueryHints({ @QueryHint(name = "org.hibernate.cacheable", value = "true") })
List<Country> findAllCountries();
```

**Estratégias:**

- `READ_ONLY` — imutáveis, mais rápido
- `NONSTRICT_READ_WRITE` — aceita dirty reads ocasionais
- `READ_WRITE` — stale data impossível, mas com lock
- `TRANSACTIONAL` — full tx (JTA)

**Quando usar:** entities de referência (country, category, role) lidas muito, modificadas pouco.

**Quando NÃO usar:** dados altamente dinâmicos, multi-nó sem cache distribuído.

### Spring Cache (camada acima do JPA)

`@Cacheable`, `@CacheEvict`, `@CachePut` em service methods — mais comum e mais simples que cache Hibernate.

```java
@Service
public class CountryService {

    @Cacheable(value = "countries", key = "#code")
    public Country findByCode(String code) {
        return repo.findByCode(code).orElseThrow();
    }

    @CacheEvict(value = "countries", allEntries = true)
    public void clearCache() { }
}
```

Suporta Caffeine, Redis, Hazelcast, Ehcache, etc.

---

## Batch operations

Inserir 10.000 entities uma por uma é lento. Use batching.

```yaml
spring:
  jpa:
    properties:
      hibernate:
        jdbc:
          batch_size: 50
        order_inserts: true
        order_updates: true
        batch_versioned_data: true
```

```java
@Transactional
public void bulkInsert(List<Patient> patients) {
    int batchSize = 50;
    for (int i = 0; i < patients.size(); i++) {
        em.persist(patients.get(i));
        if (i % batchSize == 0 && i > 0) {
            em.flush();
            em.clear();  // importante — evita OOM
        }
    }
}
```

**Condição para batching funcionar:**

- **ID não pode ser `IDENTITY`** — Hibernate precisa INSERT imediato para pegar ID, impedindo batch
- Use **`SEQUENCE`** com `allocationSize` adequado

**Para updates/deletes em massa, prefira JPQL direto:**

```java
@Modifying
@Query("UPDATE Patient p SET p.active = false WHERE p.lastLoginAt < :cutoff")
int deactivateStale(@Param("cutoff") Instant cutoff);
// Muito mais rápido que carregar e modificar cada um
```

---

## Testando JPA

### @DataJpaTest com Testcontainers

Ver [[Testes em Java]] para a stack completa. Resumo:

```java
@DataJpaTest
@Testcontainers
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class PatientRepositoryTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @Autowired private PatientRepository repo;
    @Autowired private TestEntityManager em;

    @Test
    void shouldFindByEmail() {
        em.persist(new Patient("Maria", "maria@test.com"));
        em.flush();
        em.clear();  // importante — força ir ao banco na próxima query

        var result = repo.findByEmail("maria@test.com");
        assertThat(result).isPresent();
    }
}
```

**Por que `em.clear()`:** sem ele, a query subsequente pode retornar do 1st level cache, não testando a query real.

**H2 não é Postgres.** Use Testcontainers — ver [[Testes em Java]].

---

## Flyway: migrations seguras

Flyway gerencia versões do schema via arquivos SQL.

### Estrutura

```
src/main/resources/db/migration/
  V1__create_patients.sql
  V2__add_email_index.sql
  V3__add_phone_column.sql
  V4__backfill_phones.sql
```

**Convenção:** `V<versão>__<descrição>.sql`. Duplo underscore.

### Regras de ouro

- **Nunca edite migrations já aplicadas** — crie uma nova
- **Nunca faça rollback automático** — roll-forward é mais seguro
- **Teste migrations em staging** antes de produção
- **Baseline** em projetos existentes: `mvn flyway:baseline`

### Migrations seguras em produção (expand-and-contract)

`ALTER TABLE ADD COLUMN NOT NULL` em tabela com 100M rows trava o banco. Solução: **3 passos** (expand, migrate, contract).

```sql
-- V10__add_email_nullable.sql  (expand)
ALTER TABLE patients ADD COLUMN email VARCHAR(255);

-- Deploy código que ESCREVE no email mas ainda usa o antigo

-- V11__backfill_email.sql  (migrate — em batches, sem lock longo)
UPDATE patients SET email = CONCAT('user_', id, '@legacy.com') WHERE email IS NULL;

-- V12__email_not_null.sql  (contract — após deploy confirmar que tudo escreve)
ALTER TABLE patients ALTER COLUMN email SET NOT NULL;
```

**Nunca:**

- `DROP COLUMN` na mesma release que remove o código que usa a coluna
- `RENAME COLUMN` — crie nova, copie dados, remova antiga depois
- `ALTER TABLE` mudando tipo (exceto widening)
- Criar índice sem `CONCURRENTLY` em tabelas grandes (Postgres):

```sql
-- RUIM — bloqueia writes
CREATE INDEX idx_patients_email ON patients(email);

-- BOM
CREATE INDEX CONCURRENTLY idx_patients_email ON patients(email);
```

→ Ver também [[API Design]] sobre evolução de APIs com deprecation.

---

## Quando NÃO usar JPA

JPA é maravilhoso para CRUD e modelos ricos, mas **não é bala de prata**.

### Use alternativas quando:

- **Queries analíticas complexas** — use SQL nativo, jOOQ, ou views materializadas
- **Bulk operations** — JPA é lento. Use JDBC direto ou `@Modifying` com JPQL.
- **Reporting** — use views, stored procedures, ou query builder (jOOQ)
- **Full-text search** — Elasticsearch ou Postgres `tsvector`
- **Migrações de dados grandes** — JDBC batch ou ferramentas dedicadas
- **Tight control sobre SQL** — jOOQ, JdbcTemplate, ou myBatis

### jOOQ — alternativa type-safe

```java
DSLContext dsl = ...;

List<PatientRecord> patients = dsl
    .selectFrom(PATIENTS)
    .where(PATIENTS.ACTIVE.eq(true))
    .and(PATIENTS.AGE.greaterThan(18))
    .orderBy(PATIENTS.CREATED_AT.desc())
    .limit(10)
    .fetchInto(PatientRecord.class);
```

**Vantagens:** type-safe, SQL poderoso (window functions, CTEs), mais rápido que JPA para queries complexas.

**Desvantagens:** licença comercial para alguns bancos, curva de aprendizado, code generation.

### JdbcTemplate / JdbcClient

Para queries simples e controle total:

```java
@Autowired
private JdbcClient jdbcClient;

List<Patient> patients = jdbcClient.sql("SELECT * FROM patients WHERE active = true")
    .query(Patient.class)
    .list();
```

**Quando usar:** scripts, jobs de batch, queries simples sem relacionamentos, quando JPA overhead não se justifica.

---

## Armadilhas comuns

- **EAGER fetch** em `@ManyToOne` — causa N+1 e queries gigantes. Sempre LAZY.
- **N+1 queries** — o bug mais caro. Use `@EntityGraph`, `JOIN FETCH`, ou projections.
- **`@Data` do Lombok em entities** — quebra equals/hashCode e toString com lazy loading.
- **Open Session In View habilitado** em produção — esconde N+1 e segura connection pool.
- **`save()` em entity managed** — desnecessário, dirty checking faz isso automaticamente.
- **`findById` quando só precisa verificar existência** — use `existsById`, é mais rápido.
- **JPQL com `LIKE '%valor%'`** em tabelas grandes — sem índice, full scan. Considere full-text search.
- **`@Transactional` em método privado** — não funciona (proxy não intercepta). Ver [[Spring Boot]].
- **`@Transactional` em chamada interna (self-invocation)** — não funciona pelo mesmo motivo.
- **Exceção checked não faz rollback** — default só rollback em `RuntimeException`. Use `rollbackFor`.
- **Misturar JPQL e SQL nativo sem saber** — JPQL usa nomes de entidades, SQL nativo usa tabelas.
- **Esquecer `em.clear()` em batch** — memória cresce até OOM.
- **`IDENTITY` com batch inserts** — não funciona. Use `SEQUENCE`.
- **`@ManyToMany` com `FetchType.EAGER`** — dobra N+1. LAZY sempre.
- **Paginação com `JOIN FETCH`** em coleções — carrega tudo na memória. Use DTO projection.
- **Modificar coleção durante iteração** — `ConcurrentModificationException`. Use Iterator.
- **Entity com relações mutáveis sem helper methods** — inconsistência entre os lados da relação.
- **Transação aberta por muito tempo** — connection pool esgota.
- **Dirty checking em loops de milhares de entities** — overhead cresce. Use `em.clear()` periodicamente.
- **`cascade = ALL` sem pensar** — delete em pai deleta filhos. Pode não ser o que você quer.
- **Assumir que `JpaRepository.delete(entity)` é atômico** — se entity não está managed, faz SELECT primeiro.
- **Nunca migrar schema com lock longo** — expand-and-contract em produção.
- **H2 em testes que testam queries reais** — dialeto diferente. Use Testcontainers.
- **Esquecer `@Version`** em entities que podem ser editadas concorrentemente — lost updates silenciosos.

---

## Na prática (da minha experiência)

> **MedEspecialista — patterns que padronizei:**
>
> **1. Sempre LAZY, sempre projections:**
> Default do projeto é `@ManyToOne(fetch = LAZY)` em todas as relações. Para listagens, uso exclusivamente DTO projections (records). Para detail pages, uso `@EntityGraph` com attributePaths específicos. Nunca dependo do padrão da JPA.
>
> **2. Open Session In View desabilitado desde o dia 1:**
> `spring.jpa.open-in-view=false` no `application.yml`. Força pensar em fetch strategies corretamente — qualquer acesso lazy fora da tx quebra em dev, forçando correção antes de ir pra produção.
>
> **3. Service com `readOnly = true` default:**
> Toda classe `@Service` anotada com `@Transactional(readOnly = true)`. Métodos de escrita sobrescrevem com `@Transactional` explícito. Elimina overhead de dirty checking em queries e sinaliza intenção.
>
> **4. Testcontainers desde o primeiro teste:**
> Nunca H2. Todos os testes de repository usam PostgreSQL via Testcontainers com `@ServiceConnection`. Zero bugs de dialect em produção.
>
> **5. Flyway com expand-and-contract religioso:**
> Cada mudança de schema que afeta tabela grande tem 3 migrations: expand, backfill, contract. Deploy sequencial (código que escreve em ambos → código que escreve só no novo → migration que remove o antigo). Zero downtime em mudanças de schema.
>
> **6. Schema prefix por bounded context:**
> Cada bounded context tem seu próprio schema PostgreSQL (`appointments.`, `billing.`, `patients.`). Isso força isolamento — mesmo que os módulos estejam no mesmo monolito, não podem cruzar fronteiras de schema via JPA direto.
>
> **7. Auditoria com Spring Data:**
> Entidade base `Auditable` com `@CreatedDate`, `@LastModifiedDate`, `@CreatedBy`, `@LastModifiedBy`. Todas as entities herdam. `AuditorAware` integra com Spring Security para capturar o user.
>
> **8. Queries complexas em jOOQ:**
> Relatórios analíticos (dashboards, exports) não passam por JPA. jOOQ com window functions e CTEs, muito mais eficiente. JPA fica para o domínio transacional.
>
> **Incidente memorável — N+1 em produção:**
> Dashboard de admin mostrava "lista de médicos com total de consultas este mês". Dev experiente escreveu `doctors.forEach(d -> result.add(d.getName() + ": " + d.getAppointments().size()))`. Funcionou em dev (OSIV habilitado escondeu, e poucos dados). Em produção com 500 médicos e milhões de consultas, a página demorava 30s para carregar — 500 queries para contar appointments, cada uma com full scan. Corrigi com uma query agregada: `SELECT d.id, d.name, COUNT(a) FROM Doctor d LEFT JOIN d.appointments a GROUP BY d.id`. Tempo caiu para 80ms.
>
> **Lição:** N+1 não é teoria de livro — é o bug mais caro que você vai encontrar em JPA. Monitor de query count em testes, SQL logging em dev, e cultura de "sempre cheque quantas queries o endpoint faz".
>
> **A lição principal:** JPA é poderoso mas exige disciplina. As armadilhas não são por má intenção — são por desconhecimento. Invista tempo aprendendo fetch strategies, transações, e padrões de query. Use ferramentas (`@EntityGraph`, projections, Specifications) em vez de depender da mágica do Hibernate.

---

## How to explain in English

> "Spring Data JPA is my daily driver for persistence in Java backend applications. It sits on top of Hibernate and eliminates repository boilerplate, but using it well requires understanding what's happening underneath.
>
> The first principle I apply is: always LAZY. Default JPA makes `@ManyToOne` eager, which is one of the biggest hidden performance issues in enterprise Java. Every association in my entities is LAZY, and I control what gets loaded explicitly with `@EntityGraph` or DTO projections.
>
> The second principle: always know the SQL your code generates. I enable Hibernate SQL logging in dev and actively watch for N+1 queries. N+1 is the most expensive bug in JPA — a list endpoint that looks innocent can generate hundreds of queries if you iterate over a collection of parents and access a lazy relation. I solve N+1 with `@EntityGraph` for simple cases, `JOIN FETCH` for one-level joins, and DTO projections for read-only views.
>
> For transactions, I put `@Transactional(readOnly = true)` at the class level on my Services and override individual methods that modify state with plain `@Transactional`. Read-only gives Hibernate permission to skip dirty checking and signals intent. I also disable Open Session In View in production — it hides N+1 and holds connections longer than needed.
>
> For testing, I use Testcontainers with real PostgreSQL, never H2. SQL dialect differences cause tests to pass in CI and fail in production.
>
> For migrations, I use Flyway with an expand-and-contract pattern for anything that touches large tables — add nullable column, backfill, then add NOT NULL constraint in separate migrations deployed across releases. No downtime.
>
> And when JPA becomes the wrong tool — for complex analytics, aggregations, window functions — I reach for jOOQ. JPA for the transactional domain, jOOQ for the analytical queries. Use the right tool for the job."

### Frases úteis em entrevista

- "Every association in my entities is LAZY. The default is EAGER for @ManyToOne which is a hidden performance killer."
- "I detect N+1 queries with Hibernate SQL logging and solve them with @EntityGraph or DTO projections."
- "I disable Open Session In View in production — it hides bugs and holds connections too long."
- "My Services are `@Transactional(readOnly = true)` at class level, with writes overriding explicitly."
- "For testing, I use Testcontainers with real PostgreSQL, not H2. Dialect differences cause false positives."
- "For migrations on large tables, I use expand-and-contract to avoid downtime."
- "For complex analytical queries, I use jOOQ instead of JPQL — type-safe SQL with window functions."
- "I use `@Version` for optimistic locking on entities that can be edited concurrently."
- "For bulk operations, I use JPQL @Modifying queries, not loading entities one by one."
- "Never use `@Data` Lombok on entities — it breaks equals/hashCode with lazy associations."

### Key vocabulary

- entidade → entity
- relacionamento → relationship / association
- mapeamento → mapping
- estratégia de busca → fetch strategy
- carregamento preguiçoso → lazy loading
- carregamento antecipado → eager loading
- contexto de persistência → persistence context
- verificação de mudanças → dirty checking
- flush → flush
- destacada → detached (entity)
- gerenciada → managed (entity)
- projeção → projection
- especificação → specification
- bloqueio otimista → optimistic locking
- bloqueio pessimista → pessimistic locking
- processamento em lote → batch processing
- migração → migration
- cache de primeiro nível → first-level cache (session)
- cache de segundo nível → second-level cache (application-wide)
- consulta nomeada → named query
- consulta derivada → derived query

---

## Recursos

### Documentação

- [Spring Data JPA Reference](https://docs.spring.io/spring-data/jpa/reference/)
- [Hibernate User Guide](https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html)
- [Jakarta Persistence (JPA) Specification](https://jakarta.ee/specifications/persistence/)
- [Flyway Documentation](https://documentation.red-gate.com/fd/)

### Livros

- **High-Performance Java Persistence** — Vlad Mihalcea (o livro definitivo)
- **Pro JPA 2 in Java EE 8** — Mike Keith, Merrick Schincariol
- **Java Persistence with Hibernate** — Christian Bauer, Gavin King

### Blogs e artigos

- [Vlad Mihalcea — Hibernate expert](https://vladmihalcea.com/) — absolutamente essencial
- [Thorben Janssen — Hibernate Tips](https://thorben-janssen.com/)
- [Baeldung JPA tag](https://www.baeldung.com/persistence-with-spring-series)
- [findById anti-pattern (Vlad)](https://vladmihalcea.com/spring-data-jpa-findbyid/)

### Ferramentas

- [Testcontainers PostgreSQL](https://testcontainers.com/modules/postgresql/)
- [p6spy](https://github.com/p6spy/p6spy) — SQL log com parâmetros resolvidos
- [Hibernate Statistics](https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html#statistics)
- [DBeaver / DataGrip](https://www.jetbrains.com/datagrip/) — explorar o banco
- [jOOQ](https://www.jooq.org/) — alternativa type-safe

---

## Veja também

- [[Spring Boot]] — IoC, AOP, transações, troubleshooting
- [[Spring Security]] — autenticação/autorização
- [[Banco de dados]] — SQL, NoSQL, ACID, índices, sharding, replication
- [[Java Concurrency]] — transações e locks
- [[Testes em Java]] — `@DataJpaTest`, Testcontainers
- [[API Design]] — paginação cursor-based, evolução de APIs
- [[Java Fundamentals]] — a linguagem
- [[System Design]] — connection pools, caching, estratégias
- [[Arquitetura de Software]] — Hexagonal, DDD, bounded contexts
