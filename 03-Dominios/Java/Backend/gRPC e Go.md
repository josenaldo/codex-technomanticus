# Protocol Buffers

> [!info] O que é e como utilizar protocol buffers - Aprenda Golang  
> Protocol buffers, protobuf ou simplesmente proto, é uma linguagem criada pela Google para serialização de dados.  
> [https://aprendagolang.com.br/2023/06/22/o-que-e-e-como-utilizar-protocol-buffers/](https://aprendagolang.com.br/2023/06/22/o-que-e-e-como-utilizar-protocol-buffers/)  

## Documentação

> [!info] Protocol Buffers  
> Protocol Buffers are language-neutral, platform-neutral extensible mechanisms for serializing structured data.  
> [https://protobuf.dev/](https://protobuf.dev/)  

## Repositório

> [!info] Protocol Buffers  
> A language-neutral, platform-neutral extensible mechanism for serializing structured data.  
> [https://github.com/protocolbuffers](https://github.com/protocolbuffers)  

# gRPC

## Documentação

> [!info] Documentation  
> A high-performance, open source universal RPC framework  
> [https://grpc.io/docs/](https://grpc.io/docs/)  

## Youtube

> [!info] gRPC  
> This is a channel for all videos related to gRPC.  
> [https://www.youtube.com/@grpcio](https://www.youtube.com/@grpcio)  

# Instalação

Instale o `protobuf-compiler`

```Bash
sudo apt install -y protobuf-compiler
```

No arquivo `~/zshrc`, atualize o path, de modo a permitir que o `protoc` encontre os plugins.

```Bash
export PATH="$PATH:$(go env GOPATH)/bin"
```

1. Instale os plugins do `protocol compiler` para Go

```Bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```