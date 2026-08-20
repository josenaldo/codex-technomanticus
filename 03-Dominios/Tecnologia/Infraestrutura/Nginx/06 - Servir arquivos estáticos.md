---
title: "Servir arquivos estáticos"
created: 2026-08-08
updated: 2026-08-09
type: concept
fase: Adepto
status: evergreen
publish: true
tags:
  - infraestrutura
  - nginx
  - configuracao
---

# 06 — Servir arquivos estáticos

> [!abstract] TL;DR
> `root` e `alias` respondem à mesma pergunta — "onde no disco está o arquivo que corresponde a esta URI?" — de duas formas incompatíveis: `root` **concatena** o valor da diretiva com a URI inteira da request; `alias` **substitui** o trecho da URI que casou com o `location` pelo seu próprio valor. Confundir as duas produz o erro mais reproduzido de toda a configuração de Nginx: um `alias` sem barra final servindo do diretório errado, ou pior, vazando parte do caminho do sistema de arquivos para fora do diretório pretendido. Depois de resolvido o caminho, `try_files` decide, na fase `PRECONTENT`, se existe um arquivo, um diretório, ou se cai num fallback — de um `=404` seco a um redirecionamento interno para `/index.html`, o padrão que sustenta toda SPA em produção. E por baixo de tudo isso, `sendfile` e `tcp_nopush` decidem se o arquivo sai do disco direto para o socket sem nunca passar pelo espaço de usuário — o caminho zero-copy que faz a diferença entre servir estático como afterthought e servir estático como algo que não pesa no worker.

Uma configuração comum, escrita por alguém migrando de `root` para `alias` porque queria separar o prefixo público do diretório físico real:

```nginx
location /static/ {
    alias /var/www/assets;
}
```

Uma request para `/static/logo.png` não encontra `/var/www/assetslogo.png` — sem barra nenhuma entre `assets` e `logo.png` — porque `alias` não concatena, ele substitui o trecho `/static/` da URI pelo valor exato da diretiva, e o valor exato aqui termina em `s`, não em `/`. O Nginx tenta abrir um caminho que nunca existiu, e devolve `404`. Ninguém editou a diretiva errada; a diretiva está sintaticamente correta, só falta um caractere que muda o significado inteiro da substituição. Trocar `alias /var/www/assets` por `alias /var/www/assets/` resolve — mas o motivo pelo qual resolve, e por que o mesmo erro não existe (ou existe de forma bem menos silenciosa) com `root`, é o assunto desta nota inteira.

A nota anterior deste galho, [[03-Dominios/Tecnologia/Infraestrutura/Nginx/05 - O ciclo de vida de uma request|05 — O ciclo de vida de uma request]], já fixou onde essas duas diretivas entram no mapa de fases: `try_files` roda em `PRECONTENT` (fase 9), depois que todo o controle de acesso já aprovou a request; o handler de arquivo estático propriamente dito — a leitura do arquivo do disco e a montagem da resposta — roda em `CONTENT` (fase 10), junto de `index`, disputando a mesma fase que `proxy_pass` ocuparia se o `location` fizesse proxy em vez de servir do disco. Esta nota não reabre essas fases; ela abre o que de fato acontece dentro delas quando o destino é um arquivo, não um backend.

## `root` × `alias`: concatenar contra substituir

A documentação oficial descreve `root` com uma frase que vale citar ao pé da letra, porque a palavra escolhida é o próprio mecanismo: o caminho do arquivo é montado *"by merely adding a URI to the value of the root directive"* — **somando** a URI inteira, sem descontar nada, ao valor de `root`. Uma request para `/i/top.gif`, contra `location /i/ { root /data/w3; }`, produz o caminho `/data/w3/i/top.gif` — o `/i/` do `location` continua lá, dentro do caminho final, porque `root` nunca soube que precisava removê-lo; ele só sabe que precisa grudar a URI inteira depois do seu próprio valor.

`alias`, em contraste, é o que a documentação recomenda usar *"if a URI has to be modified"* — quando o trecho que casou com o `location` não deve sobreviver no caminho final. `alias` não concatena a URI inteira: ele troca o trecho que casou com o `location` pelo valor declarado, e só o resto da URI (o que vem depois do prefixo casado) é anexado a esse valor. A mesma request `/i/top.gif`, agora contra `location /i/ { alias /data/w3/images/; }`, produz `/data/w3/images/top.gif` — sem `/i/` nenhum sobrando no meio, porque o `/i/` foi exatamente o trecho substituído.

```mermaid
graph TB
    subgraph "root — concatena a URI inteira"
        R0["Request: GET /i/top.gif"] --> R1["location /i/<br/>root /data/w3;"]
        R1 --> R2["Caminho = valor de root<br/>+ URI completa"]
        R2 --> R3["/data/w3 + /i/top.gif"]
        R3 --> R4["/data/w3/i/top.gif"]
    end

    subgraph "alias — substitui o trecho casado"
        A0["Request: GET /i/top.gif"] --> A1["location /i/<br/>alias /data/w3/images/;"]
        A1 --> A2["Caminho = valor de alias<br/>+ resto da URI, sem o prefixo /i/"]
        A2 --> A3["/data/w3/images/ + top.gif"]
        A3 --> A4["/data/w3/images/top.gif"]
    end

    style R4 fill:#1e5c3a,stroke:#27ae60,color:#fff
    style A4 fill:#1e5c3a,stroke:#27ae60,color:#fff
```

Repare no que o diagrama deixa visível: para a mesma URI de entrada, `/i/top.gif`, e o mesmo prefixo de `location`, `/i/`, os dois caminhos finais diferem só porque um deles carrega o prefixo casado dentro do resultado e o outro não. Isso não é uma diferença cosmética de sintaxe — é uma diferença de modelo mental inteira. Com `root`, o diretório declarado precisa espelhar a estrutura de URIs por baixo dele: se o `location` é `/i/`, o conteúdo físico precisa estar mesmo dentro de um subdiretório `i/` dentro do valor de `root`, porque `root` nunca desconta esse prefixo. Com `alias`, o diretório declarado é livre para ter qualquer nome físico, desconectado do prefixo público — é exatamente o caso de uso que motivou o exemplo de abertura desta nota: servir `/static/` a partir de um diretório chamado `assets`, sem precisar renomear nada no disco nem criar um subdiretório `static/` artificial só para satisfazer `root`.

> [!info] Baseline de versão
> O comportamento de `root` e `alias` descrito aqui é estável há muitas versões do Nginx e vale para as versões correntes em 2026 — mainline 1.31.3 (15 jul 2026) e stable 1.30.4.

Vale nomear uma convenção prática que decorre direto dessa diferença de mecanismo, e que vale a pena adotar mesmo quando a configuração é simples o bastante para que qualquer uma das duas diretivas "funcionaria": declarar `root` no nível de `server` — um valor único, herdado por qualquer `location` que não sobrescreva com o seu próprio `root` ou `alias`, cobrindo o caso comum de "a estrutura de diretórios no disco espelha a estrutura de URIs públicas" — e reservar `alias` só para os `location` específicos que precisam **desacoplar** o prefixo público do caminho físico, como o exemplo de abertura desta nota (`/static/` servido de um diretório chamado `assets`, sem relação nominal nenhuma com o prefixo). Misturar as duas convenções sem critério — um `alias` aqui, um `root` ali, cada um por um motivo diferente e não documentado — é o que transforma uma configuração de dez `location` em um quebra-cabeça, porque cada bloco exige que quem lê recalcule mentalmente qual mecanismo está em jogo antes de prever o caminho final.

## A regra da barra final, e por que ela é tão fácil de errar

A armadilha de abertura desta nota — `alias /var/www/assets` sem barra, contra `alias /var/www/assets/` com barra — nasce diretamente do mecanismo de substituição. Como `alias` troca o **trecho de URI casado pelo `location`** pelo **valor literal da diretiva**, qualquer caractere que esteja no fim do valor de `alias` (ou a ausência dele) aparece, sem alteração nenhuma, colado direto no caminho final. Um `location /static/` casa contra URIs que começam com `/static/` — barra incluída, por construção do próprio algoritmo de `location` descrito na nota anterior. Se `alias` termina sem barra, a substituição produz `/var/www/assets` + `logo.png` = `/var/www/assetslogo.png`, uma string sem separador nenhum entre o nome do diretório e o nome do arquivo — um caminho que nunca existe no sistema de arquivos, a menos que por coincidência exista um arquivo ou diretório chamado exatamente `assetslogo.png`.

`root` é, estruturalmente, mais tolerante a esse mesmo deslize, porque a barra que separa o valor de `root` do resto do caminho vem da **URI inteira**, que sempre começa com `/`, não do valor da diretiva em si — `root /var/www` (sem barra final) e uma request para `/static/logo.png` produzem `/var/www` + `/static/logo.png` = `/var/www/static/logo.png`, um caminho válido, porque a URI carrega sua própria barra inicial independente de como `root` termina. É essa assimetria — `root` soma um valor que já tem sua barra garantida pela URI, `alias` soma um valor que só tem barra se alguém a escreveu — que torna o erro de `alias` sem barra final tão mais comum e tão mais silencioso do que qualquer erro equivalente em `root`: a sintaxe das duas diretivas parece intercambiável até o dia em que uma delas é trocada pela outra sem ajustar a barra, e a mensagem de erro que sai do outro lado é só um `404` genérico, sem nenhuma pista de que o problema é um caractere faltando no meio do arquivo de configuração.

```nginx
# root — tolerante à barra final (a URI garante a separação)
location /static/ {
    root /var/www/app;
}
# GET /static/logo.png → /var/www/app/static/logo.png (funciona)

# alias — a barra final decide o caminho inteiro
location /static/ {
    alias /var/www/assets;
}
# GET /static/logo.png → /var/www/assetslogo.png (404 — sem separador)

location /static/ {
    alias /var/www/assets/;
}
# GET /static/logo.png → /var/www/assets/logo.png (funciona)
```

A regra prática, sem exceção: qualquer `alias` cujo `location` termine com `/` precisa, ele mesmo, terminar com `/`. Um `location` sem barra final no prefixo (`location /static { ... }`, sem a barra) muda o cálculo — mas essa variação de prefixo é uma fonte própria de armadilhas de precedência, já coberta na nota 04, e não vale reabrir aqui; a prática recomendada, em qualquer configuração nova, é declarar `location` com barra final quando o `alias` correspondente também tiver barra final, e nunca misturar as duas convenções no mesmo bloco.

> [!info] Segurança do `alias` — CVE-2026-27654
> A versão **1.29.7** (24 mar 2026) corrigiu um buffer overflow no `ngx_http_dav_module` no tratamento de requests **`COPY`** ou **`MOVE`** — os métodos WebDAV de cópia e movimentação de arquivo — dentro de um `location` configurado com `alias`, que permitia a um atacante modificar o caminho de origem ou destino da operação para fora do document root. O detalhe não é anedota: é um lembrete concreto de que `alias`, por reescrever caminho em vez de só concatenar, tem uma superfície de manipulação própria, diferente da de `root` — módulos que processam o valor resultante do `alias` (aqui, o `ngx_http_dav_module`) herdam essa complexidade adicional, e vale rodar em versão corrigida antes de expor qualquer `location` com `alias` combinado a métodos de escrita. O aviso de segurança oficial delimita o alcance: versões **0.5.13 até 1.29.6** são vulneráveis, e a correção entrou na **1.29.7** e na **1.28.3** — ou seja, a falha atravessou quase vinte anos de versões antes de ser encontrada, o que diz algo sobre quão pouco exercitada é a combinação `alias` mais WebDAV.

> [!tip] Vídeo — a barra do `alias` vista pelo lado de quem ataca
> [**It's not my mistake — Path traversal via misconfigured NGINX alias**](https://www.youtube.com/watch?v=IULL46LILrI) (The SecOps Group, ~7 min, EN) pega exatamente a armadilha da seção acima e mostra a consequência que esta nota descreve mas não demonstra: com `location /img` sem barra e `alias /static/images/`, uma requisição para `/img../` sai do diretório servido e passa a ler o que está acima dele. O vídeo monta a configuração vulnerável e percorre a exploração passo a passo, o que torna concreto por que a barra final não é preciosismo de estilo. **O que ele não cobre:** a mecânica de `root` × `alias` em si, nem `try_files` — ele assume tudo isso conhecido e vai direto ao abuso. Trecho de destaque [3:50]: *"the location doesn't end with the directory separator — then this is the misconfiguration."*
>
> 🎬 [Assistir no YouTube](https://www.youtube.com/watch?v=IULL46LILrI)

## `alias` dentro de um `location` de expressão regular

Existe uma variação de `alias` que merece nota própria porque o mecanismo de substituição muda de figura quando o `location` que o envolve não é um prefixo simples, mas uma expressão regular. Quando `alias` é usado dentro de um `location` declarado com `~` ou `~*`, a regra de "descontar o prefixo casado" deixa de fazer sentido literal — não existe um prefixo fixo para descontar, existe um padrão que pode casar partes variáveis da URI em posições diferentes a cada request. Para esse caso, `alias` precisa referenciar explicitamente as **capturas** da regex, o mesmo mecanismo de grupos nomeados ou posicionais que a nota 04 já introduziu para regex de `location`:

```nginx
location ~ ^/usuarios/(?<usuario_id>\d+)/avatar/(?<arquivo>.+)$ {
    alias /var/dados/avatares/$usuario_id/$arquivo;
}
```

Uma request para `/usuarios/482/avatar/foto.png` casa com a regex, captura `482` em `$usuario_id` e `foto.png` em `$arquivo`, e `alias` monta o caminho `/var/dados/avatares/482/foto.png` — não por concatenação nem por substituição de prefixo fixo, mas por interpolação direta das variáveis capturadas dentro do próprio valor da diretiva. Sem as capturas, um `alias` estático dentro de um `location` de regex não tem como saber qual parte da URI variável deveria virar parte do caminho — é por isso que a combinação regex-mais-`alias` exige esse passo extra, que um `location` de prefixo simples nunca precisa dar.

## `try_files`: a sintaxe e o encadeamento

`try_files` roda na fase `PRECONTENT`, a fase 9 do mapa que a nota anterior estabeleceu — depois de todo o controle de acesso, nunca antes. A documentação oficial descreve a diretiva com precisão: *"Checks the existence of files in the specified order and uses the first found file for request processing; the processing is performed in the current context."* Cada parâmetro, exceto o último, é um caminho a testar; o caminho de cada um é montado segundo as regras de `root`/`alias` já descritas nesta nota, aplicadas ao `location` corrente — não a um `location` novo, é por isso que a documentação frisa "no contexto atual".

```nginx
location /downloads/ {
    root /var/www/app;
    try_files $uri $uri.gz =404;
}
```

Nesse exemplo, `$uri` testa se o arquivo pedido existe literalmente; se não existir, `$uri.gz` testa se uma versão pré-comprimida existe (um padrão comum para servir `.gz` estático sem depender de compressão em tempo real, tema que a nota [[03-Dominios/Tecnologia/Infraestrutura/Nginx/11 - Limitar e comprimir|11 — Limitar e comprimir]] trata a fundo); se nenhum dos dois existir, `=404` — o último parâmetro — devolve um código de status fixo em vez de tentar mais um caminho.

Dá para checar a existência de um **diretório**, não só de arquivo, pondo uma barra no fim do parâmetro: `$uri/` testa se a URI corrente, tratada como caminho de diretório, existe no sistema de arquivos — é esse teste que sustenta o comportamento de servir `index.html` de dentro de um diretório sem que o cliente precise digitar o nome do arquivo por completo, combinado com a diretiva `index` que a próxima seção detalha.

Se **nenhum** dos arquivos testados for encontrado, a documentação é explícita sobre o que acontece com o último parâmetro: *"an internal redirect to the URI specified in the last parameter is made"* — um redirecionamento interno, o mesmo mecanismo que a nota anterior já descreveu em detalhe para `error_page` e para o par `SERVER_REWRITE`/`REWRITE`. O último parâmetro de `try_files` não é testado como arquivo, ele é usado como **destino** de um redirecionamento interno — a menos que seja, ele mesmo, um código de status (como `=404`) ou um `location` nomeado, os dois casos especiais que a seção seguinte cobre.

## O fallback de SPA: o uso mais comum hoje

O padrão de configuração mais repetido em qualquer aplicação de página única em produção é este:

```nginx
location / {
    root /var/www/app/dist;
    try_files $uri $uri/ /index.html;
}
```

Uma request para `/dashboard/relatorios` — uma rota que existe só dentro do roteador JavaScript do lado do cliente, sem arquivo físico correspondente nenhum no disco — testa primeiro `$uri` (`/var/www/app/dist/dashboard/relatorios`, que não existe), depois `$uri/` (`/var/www/app/dist/dashboard/relatorios/`, que também não existe, a menos que a aplicação tenha, por coincidência, um diretório com esse nome), e cai no último parâmetro, `/index.html`, tratado como URI de um redirecionamento interno. O Nginx reentra o percurso de fases a partir de `SERVER_REWRITE`, com a URI agora sendo `/index.html`, encontra esse arquivo no mesmo `root`, e o devolve — com status `200`, não `404`, porque tecnicamente um arquivo foi encontrado e servido, só que não o arquivo que a URI original pedia.

O efeito prático é que o Nginx nunca devolve `404` para nenhuma rota da SPA, porque toda URI sem arquivo físico correspondente cai de volta em `index.html`, e é o JavaScript carregado por esse HTML — o roteador do lado do cliente — quem decide, depois, se `/dashboard/relatorios` é uma rota válida ou não. Essa delegação é deliberada: sem `try_files`, um recarregamento de página (`F5`) em qualquer rota que não seja a raiz devolveria `404` do Nginx, porque não existe arquivo físico `/dashboard/relatorios` nenhum — só a rota raiz, servida por `index.html` diretamente, funcionaria com recarregamento; toda navegação profunda dependeria de nunca sair da SPA sem recarregar. `try_files ... /index.html;` fecha exatamente essa lacuna.

Vale nomear a diferença entre esse padrão e o exemplo da seção anterior, com `=404`: os dois usam `try_files`, mas com propósitos opostos. `=404` como último parâmetro é o comportamento certo quando a ausência de arquivo é, de fato, um erro — um download que não existe, um asset que foi removido — e o cliente deveria receber um `404` real, sinalizando que aquele recurso específico não existe. `/index.html` como último parâmetro é o comportamento certo quando a ausência de arquivo físico é **esperada e normal**, porque a URI pertence a um roteador de aplicação, não ao sistema de arquivos. Confundir os dois casos — usar `=404` numa SPA, ou usar `/index.html` num diretório de downloads — produz sintomas opostos: uma SPA que quebra em qualquer recarregamento de rota profunda, ou um diretório de downloads que devolve a página inicial da aplicação para qualquer nome de arquivo digitado errado, em vez de um `404` honesto.

### O erro gêmeo: deixar a API cair no fallback de SPA

Existe uma variação da mesma armadilha, comum o bastante para nomear à parte, que aparece quando a mesma aplicação serve tanto os arquivos estáticos da SPA quanto uma API dentro do mesmo `server` block, e o `location /` de fallback foi declarado de um jeito genérico demais:

```nginx
# Errado — o fallback de SPA também captura URIs de API inexistentes
location / {
    root /var/www/app/dist;
    try_files $uri $uri/ /index.html;
}

location /api/ {
    proxy_pass http://api_upstream;
}
```

Essa configuração parece correta pela tabela de precedência da nota 04 — `/api/` é um prefixo mais específico que `/`, então uma request para `/api/pedidos` cai no bloco de proxy, não no de fallback. O problema aparece numa camada diferente: se o **próprio backend da API** devolver um `404` legítimo para uma rota de API que não existe (`/api/pedidos/99999`, um pedido que não existe no banco), esse `404` vem do backend, passa pelo Nginx sem interferência de `try_files` nenhuma — porque a request nunca saiu do `location /api/`, `try_files` do bloco `/` nunca chega a ser avaliado para ela. O erro real, mais sutil, acontece quando alguém aponta um `error_page 404 /index.html;` **global**, no nível de `server`, esperando cobrir só as rotas de SPA — e esse `error_page` intercepta também os `404` legítimos vindos da API, mascarando um pedido inexistente como se fosse uma navegação de SPA bem-sucedida, com status `200` no lugar de um `404` que o cliente da API esperava para tratar como erro real.

```nginx
# Também errado — error_page global mascara 404 de API como sucesso de SPA
server {
    error_page 404 /index.html;

    location / {
        root /var/www/app/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://api_upstream;
    }
}
```

A correção, nos dois casos, é a mesma: o fallback de SPA — seja via `try_files`, seja via `error_page` — precisa viver **dentro** do `location` que serve os arquivos da SPA, nunca no nível de `server`, onde ele passa a valer também para blocos que não deveriam herdar esse comportamento. `try_files` já resolve isso corretamente por construção, porque roda só dentro do `location` que o declara; `error_page` global é o jeito mais fácil de reintroduzir o mesmo problema por uma porta diferente.

> [!tip] Vídeo — o que o `try_files` faz depois de casar
> [**The surprising ways Nginx try_files actually works**](https://www.youtube.com/watch?v=VPrBA2iZe1c) (Chris Fidao, ~6 min, EN) acrescenta a esta nota o passo que quase todo material omite: quando o `try_files` encontra o arquivo, o Nginx **não serve dali direto** — ele refaz a busca de `location`, e o arquivo pode acabar atendido por um bloco completamente diferente do que continha o `try_files`. É o redirecionamento interno da nota 05 aparecendo no lugar mais cotidiano possível, e explica por que um `.php` encontrado por `try_files` termina no PHP-FPM, e um `.css` termina no bloco de estáticos com `expires`. **O que ele não cobre:** `root` × `alias`, que ele assume resolvido. Trecho de destaque [3:15]: *"it's going to try to find other location blocks that might also handle that file."*
>
> 🎬 [Assistir no YouTube](https://www.youtube.com/watch?v=VPrBA2iZe1c)

## `index` e a interação com `try_files`

A diretiva `index`, do módulo `ngx_http_index_module`, tem valor padrão `index.html` — mesmo sem nenhuma declaração explícita no arquivo de configuração, o Nginx já tenta servir `index.html` de dentro de um diretório quando a URI aponta para ele. `index` roda como um dos handlers registrados na fase `CONTENT` (a mesma fase onde o handler de arquivo estático e `proxy_pass` competem, como a nota anterior já mapeou), e a própria documentação descreve seu efeito como um **redirecionamento interno**: uma request para `/` que resolve `index.html` não é servida diretamente do `location` original — ela é reencaminhada, internamente, para a URI `/index.html`, e pode inclusive acabar processada por um `location` diferente do que recebeu a request original, se esse `location` mais específico existir.

```nginx
location = / {
    index index.html;
}

location / {
    root /var/www/app;
}
```

Nesse par, uma request para `/` bate no primeiro bloco (match exato, decidido no passo mais barato do algoritmo de precedência), `index` resolve `index.html`, e o redirecionamento interno resultante — agora para a URI `/index.html` — é reprocessado pelo segundo `location`, o único que casa com esse novo caminho. `index` e `try_files` não competem pela mesma pergunta: `index` resolve o caso específico de uma URI que aponta para um **diretório**, sem `try_files` nenhum envolvido; `try_files`, quando presente no mesmo `location`, roda antes (fase `PRECONTENT`, 9, contra `CONTENT`, 10, onde `index` atua) e pode nunca deixar a request chegar até `index` — o parâmetro `$uri/` de um `try_files` já cobre boa parte do que `index` resolveria sozinho, e é comum ver os dois convivendo no mesmo bloco só porque `index` é o padrão implícito, não porque a configuração dependa dele de propósito.

`index` aceita mais de um arquivo, testados em ordem — o mesmo princípio de encadeamento que `try_files` usa, aplicado só ao problema mais restrito de "qual arquivo de índice existe dentro deste diretório":

```nginx
location /docs/ {
    root /var/www/app;
    index index.php index.html index.htm;
}
```

Para uma request que resolve num diretório dentro de `/docs/`, o Nginx testa `index.php` primeiro; se não existir, tenta `index.html`; se também não existir, tenta `index.htm`; se nenhum dos três existir, a resposta depende do restante da configuração daquele `location`: o módulo `ngx_http_autoindex_module`, cujo valor padrão é `autoindex off;`, é quem assumiria o handler de conteúdo em seguida, gerando uma listagem do diretório em vez de um erro — mas só se `autoindex on;` estiver declarado explicitamente ali; sem ele, o Nginx localizou um diretório real, sem nenhum arquivo de índice para servir e sem instrução para listar o conteúdo. O último elemento da lista de `index` também pode ser um caminho absoluto — `index index.php /index.html;`, por exemplo —, tratado como fallback final independente do diretório em que a busca começou, o mesmo tipo de padrão de "âncora fixa no fim da lista" que `try_files` também usa para o seu próprio último parâmetro.

## `try_files` com `=404` como último parâmetro

Vale isolar com mais precisão a diferença entre um último parâmetro tratado como **código de status** e um tratado como **URI de fallback**, porque a sintaxe dos dois é visualmente parecida mas o comportamento resultante é oposto:

```nginx
# Último parâmetro como código — nenhum redirecionamento interno acontece
location /arquivos/ {
    try_files $uri =404;
}

# Último parâmetro como URI — redirecionamento interno para essa URI
location /arquivos/ {
    try_files $uri /arquivos/nao-encontrado.html;
}
```

No primeiro caso, `=404` é reconhecido pela sintaxe (o `=` seguido de um número) como um código de resposta fixo — o Nginx nunca tenta montar um caminho de arquivo a partir dele, nunca dispara um redirecionamento interno, e a resposta final tem o código `404` e o corpo de erro padrão (ou o de um `error_page`, se declarado para esse código). No segundo caso, `/arquivos/nao-encontrado.html` é tratado como qualquer outra URI: o Nginx reentra o percurso de fases a partir de `SERVER_REWRITE`, procura um `location` para essa nova URI, e, se encontrar o arquivo, devolve `200` com o conteúdo dessa página — mesmo a intenção sendo comunicar um erro ao usuário. Servir uma página de "não encontrado" customizada com status `200` é uma armadilha própria — que a seção de armadilhas comuns retoma — porque quebra a semântica HTTP que rastreadores, ferramentas de monitoramento e o próprio cliente esperam de uma resposta de erro.

## Locations nomeados como alvo de `try_files`

A nota [[03-Dominios/Tecnologia/Infraestrutura/Nginx/04 - location e a tabela de precedência|04 — location e a tabela de precedência]] já introduziu os `location` nomeados (`@nome`) como uma sexta categoria fora do algoritmo de seleção normal — inalcançáveis por qualquer URI pública, só alcançáveis por redirecionamento interno disparado por outra diretiva. `try_files` é, ao lado de `error_page`, o disparador mais comum desse redirecionamento:

```nginx
location / {
    try_files $uri $uri/ @backend;
}

location @backend {
    proxy_pass http://app_legado;
}
```

Quando nenhum arquivo estático é encontrado para a URI corrente, o último parâmetro de `try_files`, `@backend`, não é tratado como caminho de arquivo nem como URI pública — é tratado como um `location` nomeado, e o Nginx encaminha a request diretamente para o bloco `@backend`, pulando por completo a fase `FIND_CONFIG` (já que o destino é conhecido pelo nome, não precisa ser descoberto por comparação de URI, exatamente como a nota anterior descreveu para o caso geral de redirecionamento a `location` nomeado). O padrão resultante é uma forma comum de coexistência entre estático e dinâmico no mesmo prefixo: sirva do disco tudo que existir fisicamente, e delegue para uma aplicação por trás de proxy tudo que não existir — sem precisar de dois `location` distintos disputando a mesma URI pela tabela de precedência, porque a decisão acontece dentro de um único bloco, via `try_files`, não entre blocos concorrentes.

Vale notar a diferença estrutural entre esse padrão e o fallback de SPA da seção anterior: os dois usam `try_files` com um último parâmetro que não é um arquivo comum, mas um aponta para um recurso estático (`/index.html`, ainda servido do disco, via um novo `location` público) e o outro aponta para um `location` nomeado (`@backend`, inacessível por URI pública, servido por proxy). A sintaxe do `try_files` em si não distingue os dois casos — o que muda é só o que o último parâmetro representa, uma URI pública ou um rótulo `@`.

Vale um segundo exemplo, combinando `location` nomeado com `error_page` em vez de `try_files`, porque as duas diretivas convergem para o mesmo mecanismo de redirecionamento interno por caminhos diferentes — uma página de manutenção que só entra em cena quando o backend estático fica indisponível não é um cenário hipotético em produção com volume relevante de arquivos servidos de uma origem externa (como um bucket montado via rede):

```nginx
location /midia/ {
    root /mnt/bucket-externo;
    try_files $uri =502;
    error_page 502 = @manutencao_midia;
}

location @manutencao_midia {
    root /var/www/paginas-erro;
    rewrite ^ /midia-indisponivel.html break;
}
```

Aqui, `try_files` sozinho só decide entre "o arquivo existe" e "devolve `502`"; é o `error_page 502 = @manutencao_midia;` — com o `=`, trocando a URI, não só o código — quem intercepta esse `502` e o redireciona internamente para o `location` nomeado, que serve uma página estática de aviso em vez do erro cru. As duas diretivas, `try_files` e `error_page`, nunca competem pela mesma decisão: `try_files` decide se um arquivo existe dentro do `location` corrente; `error_page` decide o que fazer com um código de erro específico, depois que a fase `CONTENT` já produziu uma resposta (ou uma falha) — e ambas convergem no mesmo destino possível, um `location` nomeado, cada uma pelo seu próprio gatilho.

## Exemplo trabalhado: um `server` block, cinco requests

Vale seguir uma configuração completa, do tipo que convive em produção com estático puro, SPA e um backend legado no mesmo `server`, e rastrear cinco requests diferentes por ela — o mesmo estilo de exercício que as notas 04 e 05 já usaram para fixar seus respectivos algoritmos.

```nginx
server {
    listen 443 ssl;
    http2 on;
    server_name app.exemplo.com;

    root /var/www/app/dist;

    location ^~ /assets/ {
        alias /var/www/app/build-assets/;
        sendfile on;
        tcp_nopush on;
        try_files $uri =404;
    }

    location /downloads/ {
        alias /var/dados/downloads/;
        try_files $uri $uri.gz =404;
    }

    location /legado/ {
        try_files $uri @backend_legado;
    }

    location @backend_legado {
        proxy_pass http://app_legado_upstream;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

**`GET /assets/app.a1b2c3.js`** — o `location ^~ /assets/` vence a disputa de precedência (a nota 04 já cobre por quê), e dentro dele `alias /var/www/app/build-assets/` substitui o trecho `/assets/` da URI pelo valor da diretiva, produzindo `/var/www/app/build-assets/app.a1b2c3.js`. `try_files $uri =404;` testa esse caminho exato; se o build gerou o arquivo com esse hash, ele existe, e é servido com `sendfile`/`tcp_nopush` ativos — o caminho zero-copy desta nota, aplicado ao caso mais comum de asset versionado por hash de conteúdo.

**`GET /assets/app.velho-hash.js`** — mesmo `location`, mesma montagem de caminho, mas o arquivo com esse hash específico não existe mais (foi substituído por um deploy novo). `try_files` não encontra o único candidato declarado (`$uri`), e cai no último parâmetro, `=404` — um `404` seco, sem redirecionamento interno nenhum, porque um asset versionado por hash que não existe é, de fato, um erro: o cliente está pedindo um build que já não faz parte do deploy corrente.

**`GET /downloads/relatorio-2026.pdf`** — o `location /downloads/` (prefixo puro, sem `^~`, mas sem nenhuma regex concorrente nesta configuração para disputar) casa, e `alias /var/dados/downloads/` substitui `/downloads/` por esse valor, produzindo `/var/dados/downloads/relatorio-2026.pdf`. `try_files $uri $uri.gz =404;` primeiro testa o PDF literal — se existir, é servido direto; só se não existir é que `$uri.gz` seria testado, e só se nenhum dos dois existir é que o `=404` fecharia a busca.

**`GET /legado/pedidos/8821`** — o `location /legado/` casa, mas não existe nenhum arquivo físico chamado `pedidos/8821` dentro do `root` implícito daquele bloco (que, sem `root` nem `alias` próprios declarados ali, herda o `root` do `server`, `/var/www/app/dist`). `try_files $uri @backend_legado;` não encontra o arquivo, e como o último parâmetro é um `location` nomeado, não uma URI comum, o Nginx encaminha a request direto para `@backend_legado`, pulando `FIND_CONFIG` por completo — e esse bloco faz `proxy_pass` para um upstream de aplicação, entregando a rota a um sistema legado que nunca teve seus arquivos publicados no disco do Nginx.

**`GET /painel/configuracoes`** — nenhum dos quatro `location` anteriores casa com esse prefixo; o `location /` (catch-all de prefixo puro) assume, herdando o `root` do `server`. `try_files $uri $uri/ /index.html;` não encontra nem o arquivo nem o diretório, e cai no fallback de SPA já descrito: redirecionamento interno para `/index.html`, servido do mesmo `root`, com status `200` — a rota `/painel/configuracoes` é, para o Nginx, só mais uma URI sem arquivo correspondente; é o roteador client-side, carregado por esse `index.html`, quem decide se aquela rota é válida.

Repare no que essas cinco requests, lado a lado, deixam visível: a mesma diretiva `try_files` aparece quatro vezes na configuração, com o mesmo nome e a mesma posição na fase `PRECONTENT`, mas produz quatro comportamentos completamente diferentes — `404` seco, fallback para `.gz`, redirecionamento para `location` nomeado, fallback de SPA — porque o que muda entre elas nunca é o mecanismo, é só o **último parâmetro** declarado em cada bloco. Entender `try_files` de verdade é entender que a diretiva é um encadeamento genérico de tentativas, e o comportamento de "borda" — o que fazer quando tudo falha — é inteiramente decidido por quem escreve a configuração, não por nenhum padrão implícito do Nginx.

| Request | `location` vencedor | Caminho/candidatos testados | Desfecho |
|---|---|---|---|
| `GET /assets/app.a1b2c3.js` | `^~ /assets/` | `alias` + `$uri`, arquivo existe | `200`, servido via `sendfile`/`tcp_nopush` |
| `GET /assets/app.velho-hash.js` | `^~ /assets/` | `alias` + `$uri`, arquivo não existe | `404` seco (último parâmetro `=404`) |
| `GET /downloads/relatorio-2026.pdf` | `/downloads/` | `alias` + `$uri`, arquivo existe | `200`, servido direto |
| `GET /legado/pedidos/8821` | `/legado/` | `$uri` não existe no `root` herdado | Redirecionamento interno para `@backend_legado` |
| `GET /painel/configuracoes` | `/` (catch-all) | `$uri` e `$uri/` não existem | Redirecionamento interno para `/index.html`, `200` |

A coluna "Desfecho" é a que vale memorizar: três dos cinco casos terminam num `200` normal, mas por três caminhos de fato diferentes — arquivo encontrado direto, redirecionamento para proxy, redirecionamento para fallback de SPA —, e só olhar o código de status final da resposta não distingue os três. É exatamente por isso que a seção de diagnóstico desta nota insiste em confirmar o caminho calculado, não só o código HTTP devolvido.

## `sendfile`, `tcp_nopush` e o caminho zero-copy

Depois que `try_files` decide qual arquivo servir e a fase `CONTENT` assume, resta uma pergunta de mecanismo, não de configuração de roteamento: como o conteúdo do arquivo sai do disco e chega ao socket do cliente? A resposta padrão, sem otimização nenhuma, envolve copiar os bytes do arquivo do espaço do kernel para um buffer no espaço de usuário do worker, e depois copiar esses mesmos bytes de volta do espaço de usuário para o buffer de saída do socket — duas cópias, duas trocas de contexto entre kernel e processo, para um dado que nunca precisou ser interpretado nem transformado por nenhuma lógica de aplicação.

A diretiva `sendfile`, cujo valor padrão é `sendfile off;`, ativa o uso da chamada de sistema `sendfile()`, que permite ao kernel copiar dados diretamente de um descritor de arquivo para um socket, sem que esses bytes precisem passar pelo espaço de usuário em nenhum momento — o chamado caminho **zero-copy**. O ganho não é teórico: cada byte que não precisa atravessar a fronteira kernel/usuário é uma cópia de memória a menos e uma troca de contexto a menos, e para um worker servindo um volume alto de arquivos estáticos, essa economia se multiplica pelo número de requests por segundo.

```nginx
location /static/ {
    root /var/www/app;
    sendfile on;
    tcp_nopush on;
}
```

`tcp_nopush`, cujo valor padrão é `tcp_nopush off;` e que só produz efeito quando `sendfile` está ativo — a própria documentação é explícita: *"the options are enabled only when sendfile is used"* — ativa a opção de socket `TCP_NOPUSH` no FreeBSD ou `TCP_CORK` no Linux. O efeito é enviar o cabeçalho da resposta e o início do arquivo no mesmo pacote TCP, em vez de um pacote pequeno só com o cabeçalho seguido de outro com o começo do corpo — reduzindo o número de pacotes na rede para arquivos pequenos, onde o overhead de cabeçalho de pacote, proporcionalmente, pesa mais.

A interação entre `sendfile` e o pool de threads (`aio threads`), que a nota [[03-Dominios/Tecnologia/Infraestrutura/Nginx/01 - O problema que o Nginx resolve|01 — O problema que o Nginx resolve e o modelo de processos]] introduziu ao explicar por que operações de disco bloqueantes ameaçam o modelo de um worker por núcleo, merece uma precisão: `sendfile` e `aio` **não são mutuamente exclusivos** — a própria documentação mostra os dois ativos ao mesmo tempo. Quando ambos estão habilitados no Linux, o comportamento é dividido por tamanho de arquivo: AIO é usado para arquivos maiores ou iguais ao tamanho especificado em `directio`, e `sendfile` é usado para arquivos menores, ou quando `directio` está desabilitado.

```nginx
location /video/ {
    sendfile       on;
    aio            threads;
    directio       8m;
}
```

O motivo estrutural dessa divisão: `sendfile()`, mesmo copiando dados de forma eficiente dentro do kernel, ainda é uma chamada que pode bloquear o worker enquanto o kernel lê o arquivo do disco — para arquivos pequenos, já em cache de página do sistema operacional na maioria das vezes, esse bloqueio é curto o bastante para não importar. Para arquivos grandes, servidos com `directio` (que contorna o cache de página, forçando leitura direta do disco), a leitura pode ser lenta o bastante para travar o worker por um tempo perceptível — e é exatamente aí que `aio threads`, delegando a leitura bloqueante para uma thread separada do pool, evita que essa lentidão trave o processamento de todas as outras conexões daquele worker. A combinação — `sendfile` para o volume comum de arquivos pequenos e médios, `aio threads` mais `directio` para o excedente de arquivos grandes — é o desenho recomendado para cargas mistas, como um diretório que serve tanto imagens pequenas quanto vídeo.

Vale a ressalva de escopo: a leitura de arquivo bloqueante e por que ela ameaça o modelo de eventos em primeiro lugar é o argumento que a nota 01 já desenvolveu; a mecânica interna do kernel por trás de `O_DIRECT`, do cache de página, e do subsistema de I/O em si pertence a outra camada do vault, coberta em [[03-Dominios/Ciência/Sistemas Operacionais/10 - I-O e o subsistema de entrada e saída|I/O e o subsistema de entrada e saída]] — aqui basta reter que `sendfile` e `aio threads` não competem, cooperam, divididos por tamanho de arquivo.

### Por que isso importa mais para estático do que para `proxy_pass`

Vale nomear, com clareza, por que esta nota — e não a de proxy reverso — é o lugar certo para `sendfile` e `tcp_nopush`. A nota [[03-Dominios/Tecnologia/Infraestrutura/Nginx/01 - O problema que o Nginx resolve|01 — O problema que o Nginx resolve e o modelo de processos]] estabeleceu que o Nginx sustenta um volume alto de conexões simultâneas com um punhado de workers porque cada worker é orientado a eventos, nunca bloqueando numa única conexão enquanto espera I/O de rede. Ler um arquivo do disco, porém, é um tipo de I/O que o modelo de eventos de rede sozinho não cobre — e é exatamente aí que `sendfile`, `aio` e `directio` entram, como o conjunto de peças que estende a mesma filosofia de não-bloqueio para o caso específico de servir bytes que vêm do sistema de arquivos, não da rede.

Quando o `location` faz `proxy_pass` em vez de servir do disco, esse problema simplesmente não existe da mesma forma: o Nginx lê a resposta do backend por um socket, não por uma chamada de leitura de arquivo, e o mesmo laço de eventos que já trata conexões de cliente trata a conexão com o upstream sem precisar de nenhum mecanismo adicional de zero-copy. É por isso que `sendfile` e `tcp_nopush` são diretivas específicas do caminho de arquivo estático, com efeito nulo (mas não erro) num `location` que só faz proxy — declará-las ali não quebra nada, só não tem nenhum arquivo de disco para acelerar.

## Diagnosticando `root`, `alias` e `try_files` na prática

Diante de um `404` inesperado num `location` que serve arquivo, a pergunta produtiva não é reler a diretiva mais uma vez — é reconstruir, explicitamente, o caminho de disco que o Nginx de fato tentou montar, e compará-lo com o que existe de verdade no sistema de arquivos. Um roteiro curto resolve a maioria dos casos:

1. **Identifique se o bloco usa `root` ou `alias`.** Um `grep` simples no arquivo já responde isso; os dois nunca deveriam coexistir no mesmo `location` — declarar ambos é redundante, e o comportamento de qual prevalece não vale a pena memorizar, porque a correção é sempre usar só um dos dois.
2. **Monte o caminho manualmente**, aplicando a regra certa: some a URI inteira ao valor de `root`, ou substitua o trecho casado pelo valor de `alias`. O diagrama desta nota é o roteiro visual para esse cálculo.
3. **Confirme se o caminho calculado existe de fato**, com um `ls` ou `stat` direto no servidor — antes de suspeitar de `try_files`, de permissão de arquivo, ou de qualquer outra causa mais exótica.
4. **Se o caminho existe mas o Nginx ainda devolve `404` ou `403`**, o próximo suspeito é permissão do sistema de arquivos: o usuário sob o qual os workers rodam (tipicamente `nginx` ou `www-data`) precisa ter permissão de leitura no arquivo e de execução (travessia) em cada diretório do caminho até ele — um erro de permissão comum, e fora do escopo de `root`/`alias` em si, mas indistinguível de um erro de caminho sem checar os dois separadamente.

```bash
nginx -T | grep -A3 "location /downloads"
curl -sI https://app.exemplo.com/downloads/relatorio-2026.pdf
ls -la /var/dados/downloads/relatorio-2026.pdf
```

O par `nginx -T` (para confirmar a diretiva de fato ativa naquele bloco, não a que alguém acha que está lá) seguido de um `curl` contra a URI suspeita e um `ls` direto no caminho calculado manualmente é a forma mais rápida de separar três causas que produzem o mesmo sintoma de `404`: caminho mal calculado por confusão entre `root` e `alias`, arquivo genuinamente ausente, ou `try_files` caindo num fallback que ninguém esperava. Para o caso específico de um fallback de SPA mal configurado (armadilha coberta adiante), vale também confirmar o **código de status** da resposta, não só o corpo — um `curl -sI` que devolve `200` para uma URI que deveria ser um `404` real é o sintoma mais direto de um `/index.html` de fallback capturando URIs que não deveriam cair nele.

O mesmo par de ferramentas resolve a variante de `alias` combinado com captura de regex: um `curl -v` contra duas ou três URIs de teste, cobrindo valores distintos que a regex aceita, revela rapidamente se as capturas estão sendo interpoladas do jeito esperado — comparar o corpo da resposta (ou o `404` recebido) contra o caminho que a interpolação manual das capturas produziria é mais confiável do que reler a regex tentando simular o motor de expressão regular de cabeça.

Vale lembrar, por fim, o limite que a nota anterior já cravou para todo redirecionamento interno: **10 por request**. Um `try_files` cujo último parâmetro aponta, direta ou indiretamente, para outro `location` cujo próprio `try_files` redireciona de volta — por exemplo, dois blocos de fallback de SPA mal desenhados, cada um apontando para a URI de fallback do outro — estoura esse teto e devolve `500`, com `rewrite or internal redirection cycle` no log de erro. É o mesmo mecanismo, e o mesmo sintoma, que a nota 05 já descreveu para laços de `rewrite`; `try_files` é só mais uma das portas de redirecionamento interno capaz de produzir esse loop, não uma exceção a ele.

| Sintoma observado | Causa mais provável | Onde checar primeiro |
|---|---|---|
| `404` em todo arquivo de um prefixo com `alias` | Barra final ausente no `alias` | Comparar `location` e `alias` caractere a caractere |
| `404` só em alguns arquivos, não todos | Arquivo genuinamente ausente no disco | `ls`/`stat` no caminho calculado |
| `200` com corpo errado numa URI que deveria ser `404` | Fallback de `try_files` ou `error_page` capturando a URI | Conferir o último parâmetro do `try_files` do bloco |
| `403` num diretório sem arquivo pedido | Ausência de `index` correspondente e `autoindex off` | Confirmar se o diretório tem algum dos arquivos de `index` |
| `500` com `rewrite or internal redirection cycle` no log | Loop de redirecionamento interno entre dois `location` | `error_log ... debug;`, técnica já detalhada na nota 05 |

## O que não cabe aqui

Vale nomear, com a mesma honestidade que qualquer fronteira deste galho exige, o que esta nota deliberadamente não cobre. Cabeçalhos de cache do lado do cliente — `Cache-Control`, `Expires`, `ETag`, `Last-Modified`, e a negociação de revalidação que decide se um navegador reusa uma cópia local em vez de rebaixar a request — pertencem à semântica HTTP, não ao mecanismo de leitura de arquivo do Nginx; o assunto é tratado em profundidade na nota [[03-Dominios/Ciência/Redes e Protocolos/08 - Caching HTTP|Caching HTTP]], e não vale reexplicar aqui o que já tem casa própria. A diretiva `expires`, que aparece de relance em alguns exemplos deste galho anexando um `Cache-Control` calculado à resposta, é só o ponto de configuração — o que aquele cabeçalho de fato significa para o navegador, e as armadilhas de invalidação que ele carrega, é conteúdo daquela nota, não desta.

Da mesma forma, cache do **lado do servidor** — `proxy_cache` guardando a resposta de um backend para reuso entre requests diferentes — é um mecanismo completamente distinto de servir um arquivo estático direto do disco, e é o assunto da nota [[03-Dominios/Tecnologia/Infraestrutura/Nginx/10 - Cache no Nginx|10 — Cache no Nginx]]. E a compressão da resposta antes de sair pela rede — `gzip`, e a interação (às vezes tensa) entre compressão em tempo real e o caminho zero-copy que esta nota acabou de descrever — pertence à nota [[03-Dominios/Tecnologia/Infraestrutura/Nginx/11 - Limitar e comprimir|11 — Limitar e comprimir]]. Servir um arquivo, decidir se ele existe, e entregá-lo do disco ao socket da forma mais barata possível é o escopo inteiro desta nota; o que acontece com esse arquivo antes de chegar ao cliente (compressão) ou depois de já ter chegado uma vez (cache) mora em outro lugar.

## Tabela de referência rápida

Vale fechar o corpo técnico consolidando, numa única tabela, as diretivas desta nota contra o que cada uma decide e a fase (do mapa da nota 05) em que ela atua — útil como consulta rápida quando a dúvida já não é "como funciona", mas "qual diretiva resolve isto":

| Diretiva | O que decide | Fase |
|---|---|---|
| `root` | Caminho = valor + URI inteira (concatena) | — (consultada em `CONTENT`, ao montar o caminho) |
| `alias` | Caminho = valor + resto da URI, sem o prefixo casado (substitui) | — (idem) |
| `try_files` | Qual candidato existe; fallback via código, URI ou `location` nomeado | `PRECONTENT` (9) |
| `index` | Qual arquivo de índice servir dentro de um diretório | `CONTENT` (10) |
| `sendfile` | Se a entrega usa o caminho zero-copy do kernel | — (mecanismo de I/O, não fase de request) |
| `tcp_nopush` | Se cabeçalho e início do arquivo saem no mesmo pacote TCP | — (idem, só produz efeito com `sendfile on`) |
| `aio` / `directio` | Se a leitura bloqueante de arquivos grandes usa thread pool | — (idem) |

## Armadilhas comuns

> [!warning] `alias` sem barra final produzindo caminho inválido
> **O que acontece:** um `location /prefixo/ { alias /caminho/sem/barra; }` devolve `404` para todo arquivo dentro daquele prefixo, mesmo os arquivos existindo de fato no disco. **Por quê:** `alias` substitui o trecho de URI casado pelo `location` (que termina em `/`) pelo valor literal da diretiva; sem barra final em `alias`, a substituição cola o nome do arquivo direto no fim do nome do diretório, sem separador, produzindo um caminho que nunca existe. **Como evitar:** sempre terminar `alias` com `/` quando o `location` correspondente também termina com `/` — tratar os dois como um par que precisa concordar, nunca configurar um sem checar o outro.

> [!warning] Trocar `root` por `alias` (ou vice-versa) sem ajustar o caminho
> **O que acontece:** uma configuração que funcionava com `root` passa a servir do lugar errado, ou a devolver `404`, depois de alguém trocar para `alias` (ou o contrário) sem recalcular o valor da diretiva. **Por quê:** `root` concatena a URI inteira ao seu valor; `alias` substitui só o trecho casado pelo `location`. Os dois exigem valores de diretório diferentes para produzir o mesmo caminho final, mesmo servindo a mesma URI — copiar o valor de um para o outro sem ajustar quase sempre está errado. **Como evitar:** ao migrar entre as duas diretivas, recalcular o caminho manualmente para uma URI de teste, ou consultar o diagrama desta nota, antes de assumir que o valor antigo continua válido.

> [!warning] Usar `/index.html` como fallback num `location` que não é de SPA
> **O que acontece:** um diretório de downloads ou de arquivos públicos, configurado com `try_files $uri $uri/ /index.html;` por hábito copiado de outra configuração, passa a devolver a página inicial da aplicação — com status `200` — para qualquer nome de arquivo inexistente, em vez de um `404` honesto. **Por quê:** o último parâmetro de `try_files`, quando não é um código (`=404`) nem um `location` nomeado (`@algo`), é sempre tratado como URI de redirecionamento interno — o Nginx nunca distingue "isso é uma rota de SPA legítima" de "isso é um erro de digitação no nome do arquivo"; a distinção é só de intenção de quem escreveu a configuração. **Como evitar:** usar `=404` como último parâmetro em qualquer `location` onde a ausência de arquivo é, de fato, um erro a comunicar; reservar o fallback para `/index.html` (ou equivalente) só para os `location`s que servem uma aplicação client-side de rota própria.

> [!warning] Esperar que `index` sozinho resolva o mesmo que `try_files`
> **O que acontece:** alguém remove `try_files` de um `location`, confiando que o valor padrão de `index` (`index.html`) já cobre o comportamento esperado, e passa a receber `404` em URIs que antes caíam no fallback. **Por quê:** `index` só resolve o caso de uma URI que aponta para um diretório existente, tentando servir um arquivo de índice de dentro dele; `try_files` cobre um espaço mais amplo — arquivo literal, diretório, e fallback para qualquer URI, existente ou não, incluindo rotas que não correspondem a nenhum caminho físico no disco. **Como evitar:** tratar `index` como resolução de "qual arquivo dentro deste diretório" e `try_files` como resolução de "o que fazer quando nada existir" — os dois compõem, não se substituem.

> [!warning] Confiar no valor padrão de `sendfile` sem declará-lo
> **O que acontece:** uma configuração nova, copiada de um tutorial que assume `sendfile` ativo, serve arquivos estáticos com desempenho abaixo do esperado sob carga, sem nenhum erro visível de configuração. **Por quê:** o valor padrão de `sendfile` é `off` — o Nginx não ativa o caminho zero-copy sozinho; quem não declara `sendfile on;` explicitamente está copiando cada arquivo estático através do espaço de usuário do worker, mesmo sem saber. **Como evitar:** declarar `sendfile on;` explicitamente em qualquer `http`, `server` ou `location` que sirva arquivo estático de volume relevante, em vez de assumir que já é o comportamento padrão.

> [!warning] Esquecer as capturas ao usar `alias` dentro de `location` de regex
> **O que acontece:** um `location` de expressão regular combinado com `alias` devolve `404` para toda request, mesmo o arquivo existindo no disco no caminho esperado. **Por quê:** dentro de um `location` de regex, `alias` não tem um prefixo fixo para descontar da URI — ele depende inteiramente das variáveis capturadas pela própria regex (`$1`, `$2`, ou grupos nomeados) para montar o caminho; um `alias` escrito como se fosse um valor estático, sem referenciar nenhuma captura, produz um caminho fixo que não reflete a URI variável da request. **Como evitar:** ao combinar `alias` com `location` de regex, sempre nomear os grupos de captura relevantes e referenciá-los explicitamente dentro do valor de `alias`, conferindo o caminho resultante com uma request de teste antes de confiar na configuração.

> [!warning] `error_page 404` global mascarando `404` legítimo de API como sucesso de SPA
> **O que acontece:** um backend de API devolve `404` para um recurso que de fato não existe (um pedido, um usuário, um registro qualquer), e o cliente recebe `200` com o HTML da aplicação no lugar do erro esperado. **Por quê:** um `error_page 404 /index.html;` declarado no nível de `server` intercepta **todo** `404` produzido por qualquer `location` daquele `server`, inclusive os que vêm de um `proxy_pass` para uma API — o redirecionamento interno resultante não distingue "arquivo estático ausente" de "recurso de API inexistente", porque os dois chegam à mesma fase de tratamento de erro do mesmo jeito. **Como evitar:** manter o fallback de SPA dentro do próprio `try_files` do `location` que serve os arquivos estáticos, nunca como `error_page` de escopo `server`; se `error_page` for mesmo necessário, escopá-lo dentro do `location` específico da SPA, nunca no nível que também cobre `/api/`.

## Como explicar em inglês

> "`root` and `alias` both answer the same question — where on disk does this URI live — but they build the path in opposite ways. `root` concatenates: it takes the whole URI and appends it to the directory you declared, so the location prefix survives inside the final path. `alias` substitutes: it replaces exactly the part of the URI that matched the location with the directory you declared, so the prefix disappears from the final path. That difference is the whole reason for the most reproduced nginx mistake there is — an `alias` without a trailing slash glues the filename straight onto the directory name with no separator, and you get a 404 that gives you zero hint about what's actually wrong. `try_files` runs after that path is resolved, in the precontent phase, always after access control — it checks a list of candidates in order, and if none exist, it does an internal redirect to whatever URI you put last. The SPA fallback pattern — `try_files $uri $uri/ /index.html` — depends entirely on that behavior: every route that doesn't map to a real file falls back to `index.html`, and the client-side router takes it from there."

| PT | EN |
|---|---|
| concatenar a URI | append/concatenate the URI |
| substituir o trecho casado | replace the matched segment |
| barra final | trailing slash |
| redirecionamento interno | internal redirect |
| fallback de SPA | SPA fallback |
| caminho zero-copy | zero-copy path |
| arquivo pré-comprimido | pre-compressed file |
| location nomeado | named location |
| valor padrão (da diretiva) | default value (of the directive) |
| leitura bloqueante | blocking read |

## O que vem a seguir

Com o `location` escolhido, o mapa de fases entendido, e agora o caminho completo de servir um arquivo do disco — `root` contra `alias`, `try_files` decidindo o fallback, `sendfile` e `tcp_nopush` entregando os bytes sem cópia redundante —, falta só o outro destino possível da fase `CONTENT`: encaminhar a request para um backend em vez de servir do disco. É aí que o Nginx deixa de ser só um servidor de arquivos e passa a ser o proxy reverso que a maioria das arquiteturas em produção de fato usa.

- [[03-Dominios/Tecnologia/Infraestrutura/Nginx/07 - Proxy reverso|07 — Proxy reverso]] — a barra final do `proxy_pass` (a mesma armadilha de concatenação-versus-substituição desta nota, num disfarce diferente), os cabeçalhos `X-Forwarded-*`, buffers, timeouts.
- [[03-Dominios/Tecnologia/Infraestrutura/Nginx/10 - Cache no Nginx|10 — Cache no Nginx]] — `proxy_cache`, o cache do lado do servidor que esta nota deixou fora de escopo.
- [[03-Dominios/Tecnologia/Infraestrutura/Nginx/11 - Limitar e comprimir|11 — Limitar e comprimir]] — `gzip` e a compressão da resposta, também fora do escopo desta nota.
- [[03-Dominios/Tecnologia/Infraestrutura/Nginx/13 - Tuning e diagnóstico|13 — Tuning e diagnóstico]] — onde o custo de `aio`, `sendfile` e descritores de arquivo abertos reaparece sob a lente de operação e diagnóstico.

## Fontes

- **Nginx Docs** — [*Module ngx_http_core_module*](https://nginx.org/en/docs/http/ngx_http_core_module.html) — a fonte primária desta nota: `root`, `alias`, `try_files`, `sendfile`, `tcp_nopush`, `aio`, `directio`, seus valores padrão e a descrição textual exata de cada mecanismo, incluindo o limite de 10 redirecionamentos internos e a mensagem `rewrite or internal redirection cycle`.
- **Nginx Docs** — [*Module ngx_http_index_module*](https://nginx.org/en/docs/http/ngx_http_index_module.html) — a diretiva `index`, seu valor padrão (`index.html`) e o exemplo de redirecionamento interno entre dois `location`.
- **Nginx Docs** — [*Changes*](https://nginx.org/en/CHANGES) — registro da versão 1.29.7 (24 mar 2026), que corrigiu o buffer overflow no tratamento de `COPY`/`MOVE` em `location` com `alias`; também confirma a baseline mainline 1.31.3 (15 jul 2026) e a depreciação do parâmetro `http2` de `listen` desde a 1.25.1.
- **Nginx** — [*Security advisories*](https://nginx.org/en/security_advisories.html) — a atribuição da CVE-2026-27654 ao `ngx_http_dav_module` e o intervalo de versões afetadas (0.5.13 a 1.29.6; corrigida em 1.29.7 e 1.28.3).
- **Nginx Docs** — [*How nginx processes a request*](https://nginx.org/en/docs/http/request_processing.html) — o texto de referência sobre como `location` e as diretivas de conteúdo se conectam ao restante do ciclo de request, complementar à nota 05 deste galho.
