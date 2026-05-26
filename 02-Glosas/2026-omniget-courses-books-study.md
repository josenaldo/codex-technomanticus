---
title: "OmniGet — Download courses and books, then actually study them"
aliases: ["OmniGet — Download courses and books, then actually study them"]
source: https://github.com/tonhowtf/omniget
author: tonhowtf
site: GitHub
published: 2026-02-11
read: 2026-05-06
type: glosa
status: lido
tags: [desktop-app, course-downloader, study-tool, open-source, tauri]
lang: en
publish: false
---

# OmniGet — Download courses and books, then actually study them — tonhowtf

## TL;DR

OmniGet é um app desktop open-source que combina download e estudo num único fluxo: baixa cursos online (Hotmart, Udemy, Kiwify, etc.) e livros (PDF, EPUB, CBZ) e depois oferece player de vídeo e leitor com notas atadas a timestamps, flashcards SM2, Pomodoro e modo foco — tudo offline, com os arquivos vivendo no computador do usuário.

## Pontos-chave

- Funciona como downloader de plataformas de cursos pagos (Hotmart, Udemy, Kiwify, Gumroad, Teachable, Kajabi, Skool, Wondrium, Thinkific, Rocketseat) e como player com notas atadas a timestamps, retomada automática no segundo exato, suporte a legendas `.vtt` e painel de anexos com preview de PDFs e código.
- Tem leitor nativo de PDF, EPUB, CBZ, TXT e HTML, com outline/sumário, bookmarks, highlights coloridos com notas, busca interna, modo paginado vs. scroll, modo manga (RTL) para CBZ e session timer que registra quanto tempo se leu por dia.
- Inclui ferramentas auxiliares de estudo: Pomodoro que pausa o player ao final da sessão, flashcards com algoritmo SM2 do Anki (importa `.apkg`, sincroniza com AnkiWeb), notes app com links bidirecionais e knowledge graph, e dashboard de progresso com heatmap estilo GitHub.
- Suporta download de praticamente qualquer site coberto pelo `yt-dlp` (~1000 sites), incluindo plataformas asiáticas (Douyin, Xiaohongshu, Kuaishou, iQiyi, Tencent Video), mais torrents/magnet links e transferência P2P direta entre dois computadores com código de 4 palavras.
- Construído com Tauri (Rust + Svelte), distribuído como `.exe` portátil no Windows, Flatpak no Linux e `.dmg` no macOS, licença GPL-3.0 e tradução comunitária via Weblate em 8 idiomas (incluindo português).
- Anotações e progresso ficam em SQLite local; arquivos do curso/livro permanecem intactos no disco e podem ser abertos por outros apps (VLC, Calibre) ou movidos sem quebrar a biblioteca interna.
- Oferece extensão de browser (Chrome/Firefox) e hotkey global `Ctrl+Shift+D` que baixa o que estiver no clipboard sem precisar abrir a janela do app.

## Citações

> "OmniGet started as a downloader. It still does that, but the bigger half is what happens after the download: a video player for course videos, a book reader for PDFs and EPUBs, with notes, flashcards and progress tracking, all working on files that live on your computer."

> "Notes pinned to timestamps. Write a note at 12:34, click it later, the player jumps to that second. Markdown supported."

> "The reader is the part most people don't expect. OmniGet has a full document reader built in, for PDF, EPUB, CBZ, TXT and HTML. You don't need Calibre, you don't need Adobe, and nothing is uploaded anywhere."

> "Spaced repetition flashcards (SM2, the Anki algorithm), with `.apkg` import and AnkiWeb sync."

## Meu comentário

Sinceramente, achei a ideia bacana, mas parece um cinto de utilidades que tenta atender a 8 super-hérois diferentes.

Vou ficar de olho pois tem boas ideias. 
## Ver também

-
