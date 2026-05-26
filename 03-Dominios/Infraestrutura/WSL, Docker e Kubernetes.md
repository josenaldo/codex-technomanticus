- [[#WSL]]
    - [[#Guia rápido do WSL2 + Docker]]
    - [[#Configurando WSL do Zero: Ambiente perfeito para quem usa Windows]]
    - [[#Tutorial ZSH e Pyenv no Ubuntu]]
- [[#Docker]]
    - [[#APRENDA DOCKER DO ZERO | TUTORIAL COMPLETO COM DEPLOY]]
    - [[#Aprenda Docker do Zero, tutorial passo a passo]]
    - [[#Descomplicando Docker ]]
    - [[#Rodando Docker no WSL 2 sem Docker Desktop]]
    - [[#Entendendo o funcionamento de containers]]
    - [[#Comandos Docker e WSL]]
    - [[#Garanta que um container só seja iniciado quando o outro estiver pronto]]
    - [[#Curso de Docker Completo]]
    - [[#Docker Essencial: Primeiros Passos]]
    - [[#Docker GUI]]
        - [[#Lazy Docker]]
- [[#Kubernetes]]
    - [[#Kubernetes do Zero a Produção]]
    - [[#O que todo Dev precisa saber de Kubernetes. Do zero a produção]]
    - [[#TUTORIAL COMPLETO SOBRE KUBERNETES PARA INICIANTES!]]

# WSL

## **Guia rápido do WSL2 + Docker**

https://github.com/codeedu/wsl2-docker-quickstart

## **Configurando WSL do Zero: Ambiente perfeito para quem usa Windows**

[https://www.youtube.com/watch?v=On_nwfkiSAE](https://www.youtube.com/watch?v=On_nwfkiSAE)

## Tutorial ZSH e Pyenv no Ubuntu

  

[https://www.youtube.com/watch?v=W7-7NJhEfdo&ab_channel=PlanetaPython](https://www.youtube.com/watch?v=W7-7NJhEfdo&ab_channel=PlanetaPython)

# Docker

## **APRENDA DOCKER DO ZERO | TUTORIAL COMPLETO COM DEPLOY**

[https://www.youtube.com/watch?v=DdoncfOdru8](https://www.youtube.com/watch?v=DdoncfOdru8)

## **Aprenda Docker do Zero, tutorial passo a passo**

[https://www.youtube.com/watch?v=caAFYcUcgBc](https://www.youtube.com/watch?v=caAFYcUcgBc)

## Descomplicando Docker

[https://m.youtube.com/playlist?list=PLf-O3X2-mxDn1VpyU2q3fuI6YYeIWp5rR](https://m.youtube.com/playlist?list=PLf-O3X2-mxDn1VpyU2q3fuI6YYeIWp5rR)

## **Rodando Docker no WSL 2 sem Docker Desktop**

[https://www.youtube.com/watch?v=wpdcGgRY5kk](https://www.youtube.com/watch?v=wpdcGgRY5kk)

## Entendendo o funcionamento de containers

[https://www.youtube.com/watch?v=85k8se4Zo70](https://www.youtube.com/watch?v=85k8se4Zo70)

## Comandos Docker e WSL

[[Comandos Docker e WSL]]

[[Docke credential helpers]]

## Garanta que um container só seja iniciado quando o outro estiver pronto

Para garantir que um container só seja iniciado quando outro container estiver pronto, utilizamos duas propriedades importantes no `docker-compose.yml`:

1. `**depends_on**` **com** `**condition: service_healthy**`

1. `**healthcheck**`

Abaixo, veja o exemplo completo e depois a explicação detalhada:

```JavaScript
services:

  keycloak:
    image: quay.io/keycloak/keycloak:26.0.8
    command: start-dev
    ports:
      - 8080:8080
    environment:
      - KEYCLOAK_ADMIN=admin
      - KEYCLOAK_ADMIN_PASSWORD=admin
      - KC_DB=mysql
      - KC_DB_URL=jdbc:mysql://db:3306/keycloak
      - KC_DB_USERNAME=root
      - KC_DB_PASSWORD=root
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:8.0.30-debian
    volumes:
      - ./.docker/dbdata:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=keycloak
    security_opt:
      - seccomp:unconfined
    healthcheck:
      test: [ "CMD", "mysqladmin", "ping", "-h", "localhost" ]
      interval: 5s
      timeout: 10s
      retries: 3
```

## Curso de Docker Completo

> [!info] Curso de Docker Completo  
>  
> [https://www.youtube.com/playlist?list=PLg7nVxv7fa6dxsV1ftKI8FAm4YD6iZuI4](https://www.youtube.com/playlist?list=PLg7nVxv7fa6dxsV1ftKI8FAm4YD6iZuI4)  

## **Docker Essencial: Primeiros Passos**

> [!info] Docker Essencial: Primeiros Passos [Curso de Docker para Iniciantes 2023]  
> Se você é iniciante e busca aprender Docker do zero e não sabe por onde começar, esse curso é ideal para você!  
> [https://www.youtube.com/playlist?list=PLViOsriojeLrdw5VByn96gphHFxqH3O_N](https://www.youtube.com/playlist?list=PLViOsriojeLrdw5VByn96gphHFxqH3O_N)  

## Docker GUI

### Lazy Docker

https://github.com/jesseduffield/lazydocker

# Kubernetes

## **Kubernetes do Zero a Produção**

[https://www.youtube.com/watch?v=oxWEVQP5_Rg](https://www.youtube.com/watch?v=oxWEVQP5_Rg)

## **O que todo Dev precisa saber de Kubernetes. Do zero a produção**

[https://www.youtube.com/watch?v=54Cw3M4k19w](https://www.youtube.com/watch?v=54Cw3M4k19w)

## **TUTORIAL COMPLETO SOBRE KUBERNETES PARA INICIANTES!**

[https://www.youtube.com/watch?v=zEOeukcJl6E](https://www.youtube.com/watch?v=zEOeukcJl6E)

  

https://github.com/badtuxx/DescomplicandoKubernetes