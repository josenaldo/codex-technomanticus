---
title: "Documentando a API com OpenAPI e Swagger"
created: 2026-06-08
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - web
  - adepto
  - openapi
aliases:
  - "OpenAPI"
  - "Swagger"
  - "springdoc-openapi"
---

# Documentando a API com OpenAPI e Swagger

> [!abstract] TL;DR
> Documente a sua REST API gerando a especificação OpenAPI automaticamente dos controllers com **springdoc-openapi** — não o springfox, que está legado e não funciona com Spring Boot 3. Basta adicionar um starter, subir a aplicação e dois endpoints aparecem de graça: `/v3/api-docs` entrega o contrato em JSON, e `/swagger-ui.html` abre uma interface navegável e interativa. Anotações como `@Operation` e `@ApiResponse` são opcionais — use quando quiser enriquecer o que o framework não consegue inferir automaticamente.

## O que é

**OpenAPI** é uma especificação aberta (mantida pela OpenAPI Initiative) que descreve contratos de APIs REST em formato JSON ou YAML: quais endpoints existem, quais parâmetros aceitam, quais respostas retornam, quais schemas de dados usam. O documento gerado é legível tanto por humanos quanto por máquinas.

**Swagger UI** é uma interface web que consome um documento OpenAPI e renderiza uma página navegável onde é possível ler e testar os endpoints diretamente no browser — sem escrever uma linha de código de cliente.

**springdoc-openapi** é a biblioteca que integra essas duas peças ao ecossistema Spring Boot 3. Ela inspeciona os controllers e configura da aplicação em tempo de execução e produz o documento OpenAPI automaticamente, sem necessidade de escrever a spec à mão.

## Por que importa

Uma API sem documentação é um contrato verbal: funciona enquanto a memória e a equipe permanecem as mesmas. Quando a equipe cresce, quando um frontend novo precisa integrar, ou quando um cliente externo consome o serviço, a falta de documentação vira atrito imediato.

Documentação gerada do código resolve três problemas de uma vez:

- **Sincronismo garantido**: o contrato publicado reflete o código real — não uma wiki que ninguém atualizou.
- **Onboarding rápido**: novos devs exploram a API no browser sem depender de ninguém.
- **Geração de clientes**: ferramentas como o OpenAPI Generator produzem SDKs tipados (TypeScript, Python, Java) a partir do `/v3/api-docs`, eliminando código de integração repetitivo.

Em entrevistas para posições sênior, saber distinguir a spec do contrato (OpenAPI) da interface de exploração (Swagger UI), e citar springdoc como substituto do springfox abandonado, demonstra maturidade na construção de APIs profissionais.

## Como funciona

### OpenAPI (a spec do contrato) vs Swagger UI (a interface)

São camadas independentes com responsabilidades distintas:

| Camada | O que é | Formato | Produzido por |
|---|---|---|---|
| OpenAPI spec | Contrato machine-readable | JSON ou YAML | springdoc-openapi |
| Swagger UI | Interface visual | HTML/JS | Swagger-UI (bundled) |

O documento OpenAPI vive em `/v3/api-docs` (JSON) e `/v3/api-docs.yaml` (YAML). Ele segue a versão 3.x da especificação OpenAPI Initiative — a mesma versão que ferramentas de geração de código e gateways de API entendem.

O Swagger UI está no `/swagger-ui.html`. Ele é apenas um consumidor do documento: lê o JSON, renderiza os endpoints em cards expansíveis e permite executar chamadas HTTP direto do browser com um botão "Try it out". Se você não quiser a UI (produção, por exemplo), basta excluir o starter webmvc-ui e usar o `springdoc-openapi-starter-webmvc-api` — a spec ainda é gerada, mas a interface não existe.

> [!info] Versão da spec
> springdoc-openapi gera documentos no padrão **OpenAPI 3.x**, não Swagger 2 (o antigo formato que o springfox usava). Ferramentas modernas esperam OpenAPI 3.

### springdoc-openapi: o starter, /v3/api-docs, /swagger-ui.html (e por que NÃO springfox)

**Como adicionar**: inclua uma única dependência. Nenhuma configuração extra é obrigatória para o caso básico — o auto-configure do Spring Boot cuida do resto.

**O que acontece no startup**: springdoc varre todos os beans anotados com `@RestController`, inspeciona as assinaturas dos métodos (tipos de retorno, `@PathVariable`, `@RequestParam`, `@RequestBody`) e os mapeamentos HTTP (`@GetMapping`, etc.) e monta o documento OpenAPI. Tipos conhecidos (primitivos, records, POJOs com getters) são refletidos para produzir schemas automáticos.

**Por que não springfox**: springfox gerou a última versão estável em junho de 2018 e suporta apenas Swagger 2 — não OpenAPI 3. Com Spring Boot 3 e Jakarta EE (pacote `jakarta.*`), springfox simplesmente não funciona: não reconhece as anotações Jakarta, tem conflitos com Spring MVC 6 e não tem manutenção ativa. Usar springfox em um projeto Boot 3 resulta em erro na inicialização ou documentação silenciosamente errada.

### Anotando quando o automático não basta (@Operation, @Parameter, @Schema, @ApiResponse)

O springdoc infere muito — mas não tudo. Algumas situações pedem anotações explícitas:

- **`@Operation`**: adiciona sumário e descrição longa ao endpoint. Útil quando o nome do método não é autoexplicativo.
- **`@Parameter`**: documenta um parâmetro específico com descrição, exemplo e se é obrigatório. Necessário quando um `@RequestParam` com nome genérico precisa de contexto.
- **`@ApiResponse`**: documenta respostas além do 200 padrão — 404, 400, 422. Sem isso, o cliente não sabe quais erros esperar.
- **`@Schema`**: aplicada em campos de DTOs/records, descreve o campo, define exemplo, restringe valores aceitos. Útil especialmente para enums ou campos com semântica não óbvia pelo nome.

> [!tip] Anotação mínima necessária
> Documente pelo menos os status de erro com `@ApiResponse`. O 200 o springdoc infere; o 404 e o 400 ele não sabe que existem a menos que você registre ou implemente um `OperationCustomizer`.

## Na prática

**Dependência Maven** (Spring Boot 3, versão springdoc 2.8.17):

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.8.17</version>
</dependency>
```

**Controller anotado** (enriquecendo o automático com descrições de erro):

```java
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/orders")
@Tag(name = "Orders", description = "Gerenciamento de pedidos")
public class OrderController {

    @Operation(
        summary = "Busca pedido por ID",
        description = "Retorna os detalhes completos de um pedido existente"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Pedido encontrado"),
        @ApiResponse(responseCode = "404", description = "Pedido não encontrado"),
        @ApiResponse(responseCode = "400", description = "ID inválido")
    })
    @GetMapping("/{id}")
    public ResponseEntity<OrderResponse> findById(
            @Parameter(description = "ID do pedido", example = "42")
            @PathVariable Long id) {
        // implementação omitida
        return ResponseEntity.ok(new OrderResponse(id, "PENDING"));
    }

    @Operation(summary = "Cria novo pedido")
    @ApiResponse(responseCode = "201", description = "Pedido criado com sucesso")
    @ApiResponse(responseCode = "422", description = "Dados inválidos no corpo")
    @PostMapping
    public ResponseEntity<OrderResponse> create(@Valid @RequestBody OrderRequest request) {
        // implementação omitida
        return ResponseEntity.status(201).body(new OrderResponse(1L, "PENDING"));
    }
}
```

Após subir a aplicação, acesse:
- `http://localhost:8080/swagger-ui.html` — interface navegável.
- `http://localhost:8080/v3/api-docs` — contrato JSON bruto.

## Armadilhas

### (1) Usar springfox em vez de springdoc

**Problema**: o springfox ainda aparece em tutoriais antigos e artigos de 2019-2021. Ao adicioná-lo em um projeto Spring Boot 3, a aplicação falha no startup ou sobe sem documentação funcional. O springfox usa Swagger 2 e não reconhece as anotações `jakarta.*`.

**Sintoma**: `NoSuchMethodError`, `ClassNotFoundException` envolvendo `springfox`, ou o `/v2/api-docs` respondendo vazio/erro.

**Fix**: remover springfox completamente. Migrar para `springdoc-openapi-starter-webmvc-ui`. As anotações mudam de `io.swagger.annotations.*` (v2) para `io.swagger.v3.oas.annotations.*` (v3).

### (2) Achar que é preciso anotar tudo

**Problema**: desenvolvedores que vêm do springfox (onde era preciso anotar praticamente tudo) tendem a encher os controllers de `@Operation`, `@Parameter` e `@Schema` redundantes, gerando ruído e acoplamento.

**Exemplo**: anotar `@Parameter(name = "id", description = "ID do produto")` num parâmetro `@PathVariable Long id` de um método chamado `findById` — o springdoc já inferiu tudo isso.

**Fix**: começar sem anotações. Gerar a spec, abrir o Swagger UI e verificar o que ficou obscuro. Anotar cirurgicamente apenas o que o framework não conseguiu inferir ou o que agrega contexto real para o consumidor.

### (3) Expor o swagger-ui em produção sem controle de acesso

**Problema**: por padrão, o `/swagger-ui.html` e o `/v3/api-docs` ficam acessíveis para qualquer requisição. Em produção, isso expõe o mapa completo da API — endpoints, schemas, exemplos — para qualquer pessoa que adivinhe a URL.

**Fix**: configurar o Spring Security para proteger esses paths (autenticação obrigatória, ou acesso restrito a IPs internos), ou desabilitar completamente via `springdoc.api-docs.enabled=false` e `springdoc.swagger-ui.enabled=false` no perfil de produção. Segurança de API é assunto do galho [[03-Dominios/Tecnologia/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|Segurança]].

### (4) Documentação escrita à mão que desatualiza

**Problema**: manter um arquivo `openapi.yaml` editado manualmente parece dar mais controle, mas na prática ele diverge do código a cada refactor — parâmetros renomeados, endpoints removidos, schemas alterados. A doc fica mentindo.

**Exemplo**: o endpoint `/products/{id}` foi renomeado para `/catalog/{id}` num PR, mas o yaml ainda aponta o path antigo. O cliente integrado quebra em produção.

**Fix**: gerar a spec do código (abordagem code-first com springdoc). Se o projeto exige contract-first, usar o OpenAPI Generator para gerar as interfaces Java a partir da spec — o código passa a ser derivado do contrato, não o contrário. Híbridos manuais são a pior combinação.

## Em entrevista

### Frase pronta (inglês)

"In Spring Boot 3 projects, I use springdoc-openapi to generate OpenAPI 3 documentation automatically from the controllers — it exposes the contract as JSON at `/v3/api-docs` and a navigable UI at `/swagger-ui.html`. I annotate only when the framework can't infer the intent, like documenting error responses with `@ApiResponse`. Springfox is off the table: it's been unmaintained since 2018, targets Swagger 2, and doesn't work with the Jakarta namespace that Boot 3 requires."

### Vocabulário

| Português | Inglês |
|---|---|
| Especificação de contrato | API contract / OpenAPI spec |
| Interface navegável | Interactive API documentation / Swagger UI |
| Geração automática | Auto-generated docs / code-first documentation |
| Contrato em JSON/YAML | Machine-readable contract |
| Anotação opcional | Optional annotation / enrichment annotation |
| Geração de cliente | Client code generation / SDK generation |
| Legado / abandonado | Legacy / unmaintained |
| Abordagem code-first | Code-first approach |

## Veja também

- [[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/13 - Versionamento de API|Versionamento de API]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Tecnologia/Java/Dicionário de Java#OpenAPI|OpenAPI]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#springdoc-openapi|springdoc-openapi]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#Swagger UI|Swagger UI]]

## Referências

- https://springdoc.org/ — documentação oficial do springdoc-openapi (versão 2.x, Spring Boot 3)
- https://spec.openapis.org/oas/v3.1.0 — especificação OpenAPI 3.1 (OpenAPI Initiative)
