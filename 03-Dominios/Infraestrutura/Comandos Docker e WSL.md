- [[#Docker]]
    - [[#docker ps]]
    - [[#docker ps -a]]
    - [[#docker run]]
    - [[#docker run hello-world]]
    - [[#docker run -it ubuntu bash]]
    - [[#docker run -it --rm ubuntu bash]]
    - [[#docker run nginx]]
    - [[#docker run -p 9090:80 nginx]]
    - [[#docker run -d -p 9090:80 nginx]]
    - [[#docker stop [id do container] ]]
    - [[#docker rm [id do container] ]]
    - [[#docker rm [nome do container] ]]
    - [[#docker rm [nome do container] -f]]
    - [[#docker run -d --name nginx nginx]]
    - [[#docker run --name nginx -p 8080:80 -d nginx]]
    - [[#docker exec nginx ls]]
    - [[#docker exec nginx bash]]
    - [[#docker exec -it nginx bash]]
    - [[#docker start nginx]]
    - [[#docker stop nginx]]
    - [[#docker run -d -v "$(pwd)"/html:/usr/share/nginx/html nginx]]
    - [[#docker run -d --name nginx -p 8080:80 —mount type=bind,source=”$(pwd)”/html,target=/usr/share/nginx/html nginx]]
    - [[#docker run -d -v "$(pwd)"/html/x:/usr/share/nginx/html nginx]]
    - [[#docker run -d --name nginx -p 8080:80 —mount type=bind,source=”$(pwd)”/html/x,target=/usr/share/nginx/html nginx]]
    - [[#docker volume ls]]
    - [[#docker volume create meuvolume]]
    - [[#docker volume inspect meuvolume]]
- [[#WSL]]
    - [[#wsl -l -v]]
    - [[#wsl --shutdown]]
    - [[#wsl --export “Ubuntu” c:\\Users\\josen\\backup\\wsl.tar]]
    - [[#wsl --import “Ubuntu” c:\\distributions\\Ubuntu c:\\Users\\josen\\backup\\wsl.tar]]

# Docker

## `docker ps`

O comando `docker ps` é usado para listar todos os contêineres Docker que estão atualmente em execução no sistema. Ele fornece uma visão rápida dos contêineres ativos, mostrando informações como o ID do contêiner, a imagem de base, os comandos que estão sendo executados dentro do contêiner, quando foram criados, seu status, portas expostas e nomes.

Exemplo de uso:

```Shell
docker ps
```

## `docker ps -a`

O comando `docker ps -a` (onde `-a` significa `--all`) expande a funcionalidade do comando `docker ps` ao listar todos os contêineres Docker no sistema, independentemente de seu estado (em execução, parado, pausado, etc.). Isso é útil para visualizar todos os contêineres existentes, permitindo que os usuários gerenciem ou inspecionem contêineres que não estão ativamente em execução.

Exemplo de uso:

```Shell
docker ps -a
```

## `docker run`

O comando `docker run` é usado para criar e iniciar um contêiner Docker a partir de uma imagem especificada. Este comando combina as etapas de criação do contêiner (`docker create`) e de inicialização do contêiner (`docker start`). Ele possui várias opções que permitem configurar o comportamento do contêiner, como mapeamento de portas, variáveis de ambiente, volumes e muito mais.

Exemplo de uso:

```Shell
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

## `docker run hello-world`

Este comando é um exemplo específico do `docker run`, utilizado para executar o contêiner da imagem `hello-world`. É frequentemente usado como um teste simples para verificar se o Docker está instalado e funcionando corretamente no sistema. Ao executá-lo, o Docker baixa a imagem `hello-world` (se ainda não estiver disponível localmente), cria um contêiner e executa um aplicativo que imprime uma mensagem no terminal.

Exemplo de uso:

```Shell
docker run hello-world
```

## `docker run -it ubuntu bash`

Este comando inicia um contêiner Docker baseado na imagem `ubuntu` e executa o `bash` dentro dele de forma interativa (`-i` para interativo, `-t` para alocar um pseudo-TTY). Isso permite que o usuário interaja com o bash do contêiner, tornando-o útil para exploração ou depuração.

Exemplo de uso:

```Shell
docker run -it ubuntu bash
```

## `docker run -it --rm ubuntu bash`

Este comando é uma extensão do anterior, com a adição da opção `--rm`, que instrui o Docker a remover automaticamente o contêiner quando ele é encerrado. Isso é útil para manter o sistema limpo, especialmente durante testes ou desenvolvimento, já que contêineres temporários não precisarão ser removidos manualmente após o uso.

Exemplo de uso:

```Shell
docker run -it --rm ubuntu bash
```

## `docker run nginx`

Este comando é usado para criar e iniciar um contêiner a partir da imagem do `nginx`, que é um servidor web leve e de alto desempenho. Ao executar este comando, o Docker procura a imagem do `nginx` no seu sistema local. Se não a encontrar, ele tentará baixá-la do Docker Hub, um repositório público de imagens Docker. Uma vez baixada a imagem, o Docker criará e iniciará um contêiner baseado nessa imagem.

Por padrão, o servidor web dentro do contêiner estará escutando na porta 80. No entanto, sem especificar mapeamento de portas (veremos isso nos próximos comandos), você não conseguirá acessar o servidor nginx do seu host.

Exemplo de uso:

```Shell
docker run nginx
```

## `docker run -p 9090:80 nginx`

Este comando é uma extensão do anterior com a adição do argumento `-p 9090:80`, que é usado para mapear a porta 9090 do host para a porta 80 do contêiner. Isso significa que se você acessar `http://localhost:9090` no navegador do seu computador, o Docker encaminhará essa solicitação para a porta 80 do contêiner nginx, permitindo que você visualize a página web servida pelo nginx.

O mapeamento de portas é crucial para acessar serviços rodando dentro de contêineres a partir do host ou da rede.

Exemplo de uso:

```Shell
docker run -p 9090:80 nginx
```

## `docker run -d -p 9090:80 nginx`

Este comando combina o mapeamento de portas do comando anterior com a opção `-d`, que significa "detached" (ou "desanexado"). Ao usar `-d`, o Docker iniciará o contêiner em segundo plano (background), permitindo que você continue usando o terminal para outros comandos enquanto o contêiner do nginx permanece em execução.

A combinação de `-d` com `-p` é muito comum quando você quer iniciar serviços web em contêineres, como o nginx, sem manter o terminal ocupado. Assim, você pode acessar o serviço web através da porta mapeada e o contêiner continuará rodando em segundo plano.

Exemplo de uso:

```Shell
docker run -d -p 9090:80 nginx
```

Aqui estão explicações para os comandos Docker que você forneceu:

## `**docker stop [id do container]**`

O comando `**docker stop**` é usado para parar a execução de um contêiner Docker. Ele requer o ID do contêiner como argumento. Quando você para um contêiner, ele mantém seu estado atual, permitindo que seja reiniciado posteriormente.

Exemplo de uso:

```Shell
docker stop <id_do_container>
```

## `**docker rm [id do container]**`

O comando `**docker rm**` é utilizado para remover um contêiner Docker. Ele requer o ID do contêiner como argumento. Ao remover um contêiner, você está excluindo permanentemente sua instância, e todos os dados associados a ele (a menos que você tenha usado volumes).

Exemplo de uso:

```Shell
docker rm <id_do_container>
```

## `**docker rm [nome do container]**`

Este comando é semelhante ao anterior, mas usa o nome do contêiner em vez do ID. No Docker, você pode atribuir nomes significativos aos contêineres para facilitar a identificação e a execução de comandos. Este comando remove o contêiner com o nome especificado.

Exemplo de uso:

```Shell
bashCopy code
docker rm <nome_do_container>

```

## `**docker rm [nome do container] -f**`

A opção `**-f**` (force) é adicionada ao comando `**docker rm**` para forçar a remoção do contêiner, mesmo se estiver em execução. Por padrão, o Docker não permite a remoção de contêineres em execução para evitar a perda de dados acidental. O uso de `**-f**` ignora essa restrição e remove o contêiner, encerrando-o primeiro, se necessário.

Exemplo de uso:

```Shell
bashCopy code
docker rm -f <nome_do_container>

```

Lembre-se de substituir `**<id_do_container>**` ou `**<nome_do_container>**` pelos valores reais do ID ou nome do seu contêiner Docker. Esses comandos são úteis para gerenciar o ciclo de vida dos contêineres, seja parando, removendo ou forçando a remoção quando necessário.

## `docker run -d --name nginx nginx`

Este comando cria e inicia um contêiner Docker chamado "nginx" a partir da imagem oficial do nginx, utilizando a opção `-d` para executar o contêiner em segundo plano (modo detached).

Exemplo de uso:

```Shell
docker run -d --name nginx nginx
```

## `docker run --name nginx -p 8080:80 -d nginx`

Este comando cria e inicia um contêiner Docker chamado "nginx", expondo a porta 80 do contêiner para a porta 8080 do host. A opção `-p` permite o mapeamento de portas entre o host e o contêiner.

Exemplo de uso:

```Shell
docker run --name nginx -p 8080:80 -d nginx
```

## `docker exec nginx ls`

O comando `docker exec` é usado para executar comandos dentro de um contêiner em execução. Neste caso, o comando `ls` está sendo executado dentro do contêiner "nginx", listando o conteúdo do diretório atual dentro do contêiner.

Exemplo de uso:

```Shell
docker exec nginx ls
```

## `docker exec nginx bash`

Este comando inicia um shell interativo (`bash`) dentro do contêiner "nginx", permitindo que você interaja com o ambiente do contêiner.

Exemplo de uso:

```Shell
docker exec nginx bash
```

## `docker exec -it nginx bash`

Similar ao comando anterior, o `-it` permite a interatividade com o shell dentro do contêiner "nginx". Essa abordagem é frequentemente usada para acessar a linha de comando interativa do contêiner.

Exemplo de uso:

```Shell
docker exec -it nginx bash
```

## `docker start nginx`

O comando `docker start` é utilizado para iniciar um contêiner Docker que está parado. Neste caso, ele inicia o contêiner chamado "nginx".

Exemplo de uso:

```Shell
docker start nginx
```

## `docker stop nginx`

O comando `docker stop` é utilizado para interromper um contêiner Docker em execução. Neste caso, ele para o contêiner chamado "nginx".

Exemplo de uso:

```Shell
docker stop nginx
```

## `docker run -d -v "$(pwd)"/html:/usr/share/nginx/html nginx`

Este comando cria e inicia um contêiner Docker com a imagem do nginx. A opção `-d` indica que o contêiner deve ser executado em segundo plano (modo detached). A opção `-v` (volume) é usada para montar um volume entre o sistema de arquivos do host e o contêiner. Neste caso, o diretório atual (`$(pwd)`) com a pasta "html" é montado no diretório `/usr/share/nginx/html` dentro do contêiner. Isso permite que você compartilhe arquivos entre o host e o contêiner.

Exemplo de uso:

```Shell
docker run -d -v "$(pwd)"/html:/usr/share/nginx/html nginx
```

## `docker run -d --name nginx -p 8080:80 —mount type=bind,source=”$(pwd)”/html,target=/usr/share/nginx/html nginx`

Este comando faz a mesma coisa que o anterior, mas utiliza uma forma diferente de montagem de volumes. Ele utiliza a opção `--mount` com o tipo `bind` para criar um vínculo direto entre o diretório do host e o diretório do contêiner. A porta 8080 do host é mapeada para a porta 80 do contêiner com a opção `-p`.

Exemplo de uso:

```Shell
docker run -d --name nginx -p 8080:80 --mount type=bind,source="$(pwd)"/html,target=/usr/share/nginx/html nginx
```

## `docker run -d -v "$(pwd)"/html/x:/usr/share/nginx/html nginx`

Este comando cria e inicia um contêiner Docker com a imagem do nginx. Ele usa a opção `-v` para montar um volume, mas desta vez o diretório `html/x` do host é montado no diretório `/usr/share/nginx/html` dentro do contêiner. Isso cria um volume específico para o contêiner.

Neste caso, como o diretório x não existe no host, ele é criado

Exemplo de uso:

```Shell
docker run -d -v "$(pwd)"/html/x:/usr/share/nginx/html nginx
```

## `docker run -d --name nginx -p 8080:80 —mount type=bind,source=”$(pwd)”/html/x,target=/usr/share/nginx/html nginx`

Este comando é semelhante ao anterior, mas usando a opção `--mount` para montar um volume do tipo `bind`. Ele cria um volume específico para o contêiner onde o diretório `html/x` do host é montado no diretório `/usr/share/nginx/html` dentro do contêiner.  
Neste caso, como o diretório x não existe no host, o comando dá um erro.  
  
A diferença entre o as opções --mount e -v é que a opção -v cria os diretórios inexistentes no host e a opção --mount lança um erro para diretórios inexistentes.

Exemplo de uso:

```Shell
docker run -d --name nginx -p 8080:80 --mount type=bind,source="$(pwd)"/html/x,target=/usr/share/nginx/html nginx
```

## `docker volume ls`

O comando `docker volume ls` é usado para listar todos os volumes Docker presentes no sistema. Isso inclui volumes que estão sendo usados por contêineres ou volumes que foram criados manualmente.

Exemplo de uso:

```Shell
docker volume ls
```

## `docker volume create meuvolume`

Este comando cria um novo volume Docker com o nome "meuvolume". Os volumes são usados para armazenar dados persistentes que podem ser compartilhados entre contêineres.

Exemplo de uso:

```Shell
docker volume create meuvolume
```

## `docker volume inspect meuvolume`

O comando `docker volume inspect` é usado para obter informações detalhadas sobre um volume específico. Ao executar esse comando, você obterá informações sobre o volume "meuvolume", incluindo o caminho no host onde os dados do volume são armazenados.

Exemplo de uso:

```Shell
docker volume inspect meuvolume
```

  

```Bash
docker run --name nginx -d --mount type=volume,source=meuvolume,target=/app nginx

docker run --name nginx2 -d --mount type=volume,source=meuvolume,target=/app nginx

docker run --name nginx3 -d -v meuvolume:/app

docker volume prune

docker pull ubuntu

docker images

docker pull php:rc-alpine

docker rmi php:latest

docker build -t josenaldo/nginx-com-vim:latest .

docker run -it josenaldo/nginx-com-vim bash

docker run --name josenaldo -d -p 8080:80 josenaldo/nginx-com-vim

docker restart josenaldo

docker stop josenaldo

docker rm $(docker ps -a -q) -f

docker logout

docker login

docker push josenaldo/nginx-com-vim

docker network create --diver bridge minharede

docker network ls

docker network prune

docker network inspect minharede

docker network connect minharede ubuntu3

docker attach ubuntu1

docker run -dit --name ubuntu1 --network minharede bash

docker run --rm -d --name nginx --network host nginx
```

  

# WSL

## `wsl -l -v`

Este comando é utilizado para listar todas as distribuições Linux instaladas no WSL, juntamente com informações adicionais sobre cada uma delas. O `-l` significa "list" (listar) e o `-v` significa "verbose" (detalhado). Quando usado, este comando exibirá o nome de cada distribuição Linux instalada, o estado (por exemplo, em execução ou parado), e a versão do WSL (1 ou 2) que cada distribuição está utilizando.

Exemplo de uso:

```Shell
wsl -l -v
```

## `wsl --shutdown`

O comando `wsl --shutdown` é utilizado para desligar completamente todas as instâncias do WSL que estão em execução. Isso pode ser útil para liberar recursos do sistema, reiniciar todas as distribuições do WSL por qualquer motivo, ou resolver problemas específicos que podem surgir durante o uso do WSL. Após executar este comando, todas as instâncias do WSL serão encerradas, e você precisará reiniciá-las manualmente ao acessar novamente.

Exemplo de uso:

```Shell
wsl --shutdown
```

## `wsl --export “Ubuntu” c:\\Users\\josen\\backup\\wsl.tar`

Este comando é usado para exportar a distribuição Linux especificada (neste caso, “Ubuntu”) para um arquivo tar. Isso é particularmente útil para fazer backup da sua distribuição WSL, permitindo que você restaure ou mova a distribuição para outro sistema mais tarde. O comando `--export` toma dois argumentos principais: o nome da distribuição a ser exportada e o caminho do arquivo para onde a distribuição será exportada.

Exemplo de uso:

```Shell
wsl --export “Ubuntu” c:\\Users\\josen\\backup\\wsl.tar
```

## `wsl --import “Ubuntu” c:\\distributions\\Ubuntu c:\\Users\\josen\\backup\\wsl.tar`

Este comando é usado para importar uma distribuição Linux para o WSL a partir de um arquivo de backup tar. O comando `--import` requer três argumentos principais:

1. **Nome da Distribuição**: O nome que você deseja dar à distribuição Linux importada no WSL. Neste caso, é “Ubuntu”.

1. **Diretório de Destino**: O local no sistema de arquivos do Windows onde os arquivos da distribuição importada serão armazenados. Aqui, é especificado como `c:\\distributions\\Ubuntu`. Se o diretório não existir, o WSL tentará criá-lo durante o processo de importação.

1. **Caminho do Arquivo de Backup**: O local do arquivo tar que contém o backup da distribuição Linux que você deseja importar. No exemplo, é `c:\\Users\\josen\\backup\\wsl.tar`.

O comando completo, corrigido e formatado corretamente para o Windows, seria:

```Shell
wsl --import Ubuntu c:\\distributions\\Ubuntu c:\\Users\\josen\\backup\\wsl.tar
```

Certifique-se de substituir os caminhos e nomes de arquivos conforme necessário para corresponder à sua configuração e preferências específicas.

Esse comando é particularmente útil para restaurar uma distribuição WSL a partir de um backup, migrar distribuições entre máquinas ou simplesmente criar uma nova instância de uma distribuição Linux no WSL sem a necessidade de baixá-la novamente da Internet.