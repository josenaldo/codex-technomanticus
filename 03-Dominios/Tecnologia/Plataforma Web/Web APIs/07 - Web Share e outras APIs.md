---
title: "Web Share e outras APIs"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: adepto
tags:
  - plataforma-web
  - web-apis
  - browser
  - javascript
  - web-share
  - entrevista
publish: true
---

# Web Share e outras APIs

> [!abstract] TL;DR
> Este capítulo cobre um conjunto de APIs utilitárias modernas que completam o arsenal do desenvolvedor web: Web Share API para compartilhar via apps nativos, Web Speech para reconhecimento e síntese de voz, Battery API, Network Information API, e o conjunto de APIs de tela cheia. Cada uma resolve um nicho específico — conhecê-las poupa reinventar soluções que o browser já oferece.

---

## Web Share API

Acionar a caixa de compartilhamento nativa do sistema operacional:

```javascript
// Verificar suporte
if (!navigator.share) {
  console.log('Web Share não suportada — mostrar botões sociais');
}

// Compartilhar texto/URL
async function shareContent() {
  if (!navigator.share) {
    // Fallback: copiar URL para o clipboard
    await navigator.clipboard.writeText(location.href);
    showToast('Link copiado!');
    return;
  }

  try {
    await navigator.share({
      title: document.title,
      text: 'Confira este artigo incrível!',
      url: location.href,
    });
    // Usuário compartilhou com sucesso
  } catch (error) {
    if (error.name !== 'AbortError') {
      // AbortError = usuário cancelou — não é erro real
      console.error('Falha ao compartilhar:', error);
    }
  }
}

// Compartilhar arquivo
async function shareFile(file) {
  if (!navigator.canShare || !navigator.canShare({ files: [file] })) {
    console.log('Compartilhamento de arquivo não suportado');
    return;
  }

  await navigator.share({
    title: 'Minha foto',
    files: [file],
  });
}
```

> [!tip] Disponibilidade
> Web Share API está disponível em iOS Safari (12.0+), Chrome Mobile (61+), e Edge (79+). No desktop, Chrome e Edge suportam a partir de versões mais recentes. Firefox desktop não suporta. Sempre verifique `navigator.share` antes de usar.

---

## Web Speech API — síntese de voz

```javascript
// Text-to-Speech
function speak(text, { lang = 'pt-BR', rate = 1, pitch = 1, volume = 1 } = {}) {
  if (!window.speechSynthesis) return;

  // Cancelar qualquer fala em andamento
  speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = lang;      // 'pt-BR', 'en-US', 'es-ES'
  utterance.rate = rate;      // 0.1 a 10 (1 = normal)
  utterance.pitch = pitch;    // 0 a 2 (1 = normal)
  utterance.volume = volume;  // 0 a 1

  // Selecionar voz específica
  const voices = speechSynthesis.getVoices();
  const ptVoice = voices.find(v => v.lang === 'pt-BR');
  if (ptVoice) utterance.voice = ptVoice;

  utterance.addEventListener('start', () => console.log('Falando...'));
  utterance.addEventListener('end', () => console.log('Terminou'));
  utterance.addEventListener('error', (e) => console.error('Erro:', e.error));

  speechSynthesis.speak(utterance);
}

// Listar vozes disponíveis (pode ser assíncrono)
function getVoices() {
  return new Promise(resolve => {
    const voices = speechSynthesis.getVoices();
    if (voices.length > 0) { resolve(voices); return; }
    
    speechSynthesis.addEventListener('voiceschanged', () => {
      resolve(speechSynthesis.getVoices());
    }, { once: true });
  });
}

speak('Olá, mundo! Bem-vindo ao Codex Technomanticus.');
```

---

## Web Speech API — reconhecimento de voz

```javascript
// Speech-to-Text (suporte limitado: Chrome, Edge; não Firefox)
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
  console.log('Reconhecimento de voz não suportado neste browser');
}

function createSpeechInput(onResult, onError) {
  const recognition = new SpeechRecognition();
  
  recognition.lang = 'pt-BR';
  recognition.interimResults = true; // resultados parciais em tempo real
  recognition.maxAlternatives = 3;   // até 3 alternativas por resultado
  recognition.continuous = false;    // para após primeira frase

  recognition.addEventListener('result', (event) => {
    const results = Array.from(event.results);
    
    results.forEach(result => {
      const transcript = result[0].transcript;
      const confidence = result[0].confidence; // 0 a 1
      const isFinal = result.isFinal;          // false = resultado parcial
      
      onResult({ transcript, confidence, isFinal });
    });
  });

  recognition.addEventListener('error', (event) => {
    onError(event.error);
    // Erros: 'not-allowed', 'no-speech', 'audio-capture', 'network'
  });

  recognition.addEventListener('end', () => {
    console.log('Reconhecimento encerrado');
  });

  return {
    start: () => recognition.start(),
    stop: () => recognition.stop(),
    abort: () => recognition.abort(),
  };
}
```

---

## Fullscreen API

```javascript
// Entrar em tela cheia
async function enterFullscreen(element = document.documentElement) {
  if (!document.fullscreenEnabled) return;
  
  try {
    await element.requestFullscreen();
    // Também: element.webkitRequestFullscreen() para Safari legado
  } catch (err) {
    console.error('Falha ao entrar em tela cheia:', err);
  }
}

// Sair de tela cheia
async function exitFullscreen() {
  if (document.fullscreenElement) {
    await document.exitFullscreen();
  }
}

// Toggle
async function toggleFullscreen(element = document.documentElement) {
  if (document.fullscreenElement) {
    await document.exitFullscreen();
  } else {
    await element.requestFullscreen();
  }
}

// Observar mudanças
document.addEventListener('fullscreenchange', () => {
  if (document.fullscreenElement) {
    console.log('Entrou em fullscreen:', document.fullscreenElement);
    document.querySelector('.fullscreen-btn').textContent = '⛶ Sair';
  } else {
    console.log('Saiu de fullscreen');
    document.querySelector('.fullscreen-btn').textContent = '⛶ Tela cheia';
  }
});
```

---

## Network Information API

```javascript
const connection = navigator.connection ||
                   navigator.mozConnection ||
                   navigator.webkitConnection;

if (connection) {
  connection.effectiveType; // '4g' | '3g' | '2g' | 'slow-2g'
  connection.downlink;       // Mbps estimado
  connection.rtt;            // Round-trip time em ms
  connection.saveData;       // true se usuário ativou data saver
  
  // Adaptar qualidade de mídia à conexão
  function getVideoQuality() {
    if (connection.saveData) return '360p';
    switch (connection.effectiveType) {
      case '4g': return '1080p';
      case '3g': return '720p';
      case '2g': return '480p';
      default:   return '360p';
    }
  }
  
  // Observar mudanças de rede
  connection.addEventListener('change', () => {
    console.log('Rede mudou para:', connection.effectiveType);
    adaptToNetwork();
  });
}
```

---

## Battery API

```javascript
// Obter status da bateria
const battery = await navigator.getBattery?.();

if (battery) {
  battery.charging;       // boolean
  battery.chargingTime;   // segundos até carga completa (Infinity se desconectado)
  battery.dischargingTime; // segundos até descarregar (Infinity se carregando)
  battery.level;           // 0.0 a 1.0

  // Observar mudanças
  battery.addEventListener('chargingchange', () => {
    console.log('Carregando:', battery.charging);
  });
  
  battery.addEventListener('levelchange', () => {
    const percent = Math.round(battery.level * 100);
    document.querySelector('.battery-indicator').textContent = `${percent}%`;
    
    if (battery.level < 0.1 && !battery.charging) {
      enablePowerSavingMode();
    }
  });
}
```

---

## Page Visibility API

```javascript
// Detectar quando a aba está visível ou oculta
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    // Aba em background — pausar operações custosas
    pauseVideo();
    pauseAnimations();
    reducePollingFrequency();
    console.log('Aba oculta — reduzindo atividade');
  } else {
    // Aba voltou ao foco
    resumeVideo();
    resumeAnimations();
    restorePollingFrequency();
    refreshData(); // dados podem estar desatualizados
    console.log('Aba visível — resumindo atividade');
  }
});

// document.visibilityState: 'visible' | 'hidden' | 'prerender'
```

---

> [!question] Para fixar
> 1. O que acontece se o usuário cancelar o dialog do Web Share? Como o código deve tratar isso?
> 2. Qual a diferença entre `SpeechRecognition` com `interimResults: true` e `false`?
> 3. Por que `requestFullscreen()` retorna uma Promise? O que pode rejeitar essa Promise?
> 4. O que `connection.saveData` indica? Como você usaria isso na prática?
> 5. Qual o uso principal de `document.visibilitychange`? Dê dois exemplos concretos.

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/06 - Geolocation e Device APIs|06 — Geolocation e Device APIs]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/08 - Web APIs em entrevista|08 — Web APIs em entrevista]] — próxima e capstone
- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/04 - Clipboard e File API|04 — Clipboard e File API]] — Web Share + Clipboard como alternativas de compartilhamento
