---
title: "Geolocation e Device APIs"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Adepto
tags:
  - plataforma-web
  - web-apis
  - browser
  - javascript
  - geolocation
  - device
  - entrevista
publish: true
---

# Geolocation e Device APIs

> [!abstract] TL;DR
> A Geolocation API fornece coordenadas GPS/Wi-Fi do dispositivo. A DeviceOrientation e DeviceMotion expõem acelerômetro, giroscópio e bússola. O MediaDevices API acessa câmera e microfone. Todas exigem HTTPS, permissão do usuário e tratamento de erros cuidadoso — o usuário pode negar, o hardware pode não existir, e a posição pode ser imprecisa.

---

## Geolocation API

```javascript
// Verificar suporte
if (!('geolocation' in navigator)) {
  console.error('Geolocation não suportada');
}

// Uma leitura (one-shot)
navigator.geolocation.getCurrentPosition(
  (position) => {
    position.coords.latitude;          // graus decimais, ex: -23.5505
    position.coords.longitude;         // graus decimais, ex: -46.6333
    position.coords.accuracy;          // metros de precisão
    position.coords.altitude;          // metros acima do nível do mar (ou null)
    position.coords.altitudeAccuracy;  // metros de precisão da altitude (ou null)
    position.coords.heading;           // graus (0=Norte, 90=Leste) ou null
    position.coords.speed;             // m/s ou null
    position.timestamp;                // ms desde epoch
  },
  (error) => {
    switch (error.code) {
      case GeolocationPositionError.PERMISSION_DENIED:    // 1
        console.error('Usuário negou a permissão');
        break;
      case GeolocationPositionError.POSITION_UNAVAILABLE: // 2
        console.error('Posição indisponível (GPS sem sinal)');
        break;
      case GeolocationPositionError.TIMEOUT:              // 3
        console.error('Timeout ao obter posição');
        break;
    }
  },
  {
    enableHighAccuracy: true, // GPS em vez de Wi-Fi/cell (mais lento, mais preciso, mais bateria)
    timeout: 10000,           // ms para timeout (padrão: Infinity)
    maximumAge: 60000,        // usar cache de até 1 min (0 = sempre fresco)
  }
);
```

---

## Monitorar posição em tempo real

```javascript
// watchPosition: callback a cada atualização
const watchId = navigator.geolocation.watchPosition(
  (position) => updateMap(position.coords),
  (error) => handleError(error),
  { enableHighAccuracy: true, maximumAge: 5000 }
);

// Parar de monitorar
navigator.geolocation.clearWatch(watchId);
```

---

## Wrappers com Promises

```javascript
// Wrapper promise para getCurrentPosition
function getPosition(options = {}) {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject, options);
  });
}

// Wrapper observable para watchPosition
function watchPosition(options = {}) {
  return {
    subscribe(callback, errorCallback) {
      const id = navigator.geolocation.watchPosition(callback, errorCallback, options);
      return () => navigator.geolocation.clearWatch(id); // unsubscribe
    }
  };
}

// Uso
async function showNearby() {
  try {
    const { coords } = await getPosition({ enableHighAccuracy: false, timeout: 5000 });
    const results = await fetchNearby(coords.latitude, coords.longitude, 5000);
    renderResults(results);
  } catch (error) {
    if (error.code === 1) {
      showMessage('Permita acesso à localização para ver resultados próximos');
    }
  }
}
```

---

## DeviceOrientation API

```javascript
// Orientação do dispositivo no espaço (giroscópio/magnetômetro)
window.addEventListener('deviceorientation', (event) => {
  event.alpha; // rotação ao redor do eixo Z (0-360°, bússola — 0 = Norte)
  event.beta;  // rotação ao redor do eixo X (-180 a 180 — inclinação frente/trás)
  event.gamma; // rotação ao redor do eixo Y (-90 a 90 — inclinação esquerda/direita)
  event.absolute; // true = orientação absoluta (bússola); false = relativa
});

// Bússola digital
function setupCompass(needle) {
  window.addEventListener('deviceorientation', (event) => {
    // alpha: 0 = Norte, 90 = Leste, 180 = Sul, 270 = Oeste
    needle.style.transform = `rotate(${-event.alpha}deg)`;
  });
}

// Experiência de "paralax" por inclinação
function setupParallax(elements) {
  let lastGamma = 0, lastBeta = 0;
  
  window.addEventListener('deviceorientation', (event) => {
    const gamma = event.gamma ?? 0; // -90 a 90
    const beta = event.beta ?? 0;   // -180 a 180
    
    elements.forEach((el, i) => {
      const depth = (i + 1) * 0.5;
      el.style.transform = `translate(${gamma * depth}px, ${beta * 0.3 * depth}px)`;
    });
  });
}
```

---

## DeviceMotion API

```javascript
// Aceleração e velocidade de rotação (acelerômetro + giroscópio)
window.addEventListener('devicemotion', (event) => {
  // Aceleração sem gravidade (m/s²)
  event.acceleration.x;
  event.acceleration.y;
  event.acceleration.z;
  
  // Aceleração com gravidade incluída
  event.accelerationIncludingGravity.x;
  event.accelerationIncludingGravity.y;
  event.accelerationIncludingGravity.z;
  
  // Velocidade de rotação (graus/segundo)
  event.rotationRate.alpha;
  event.rotationRate.beta;
  event.rotationRate.gamma;
  
  event.interval; // ms entre eventos
});

// Detectar shake do dispositivo
function onShake(callback, threshold = 15) {
  let lastX = null, lastY = null, lastZ = null;
  
  window.addEventListener('devicemotion', (event) => {
    const { x, y, z } = event.accelerationIncludingGravity;
    
    if (lastX === null) { lastX = x; lastY = y; lastZ = z; return; }
    
    const delta = Math.abs(x - lastX) + Math.abs(y - lastY) + Math.abs(z - lastZ);
    if (delta > threshold) callback();
    
    lastX = x; lastY = y; lastZ = z;
  });
}

onShake(() => console.log('Dispositivo sacudido!'));
```

> [!warning] Permissões no iOS 13+
> No iOS 13+, `devicemotion` e `deviceorientation` requerem permissão explícita. Chamar `DeviceMotionEvent.requestPermission()` dentro de um gesto do usuário.
> ```javascript
> button.onclick = async () => {
>   if (typeof DeviceMotionEvent.requestPermission === 'function') {
>     const permission = await DeviceMotionEvent.requestPermission();
>     if (permission !== 'granted') return;
>   }
>   startListening();
> };
> ```

---

## MediaDevices — câmera e microfone

```javascript
// Listar dispositivos disponíveis
const devices = await navigator.mediaDevices.enumerateDevices();
const cameras = devices.filter(d => d.kind === 'videoinput');
const microphones = devices.filter(d => d.kind === 'audioinput');

// Capturar stream de vídeo/áudio
const stream = await navigator.mediaDevices.getUserMedia({
  video: {
    width: { ideal: 1280 },
    height: { ideal: 720 },
    facingMode: 'user',          // 'user' = frontal, 'environment' = traseira
    deviceId: cameraId,          // câmera específica
  },
  audio: {
    echoCancellation: true,
    noiseSuppression: true,
    sampleRate: 44100,
  },
});

// Exibir no elemento <video>
const video = document.querySelector('video');
video.srcObject = stream;
video.play();

// Parar todas as tracks quando terminar
function stopStream(stream) {
  stream.getTracks().forEach(track => track.stop());
}

// Capturar screenshot da câmera
function captureFrame(videoEl) {
  const canvas = document.createElement('canvas');
  canvas.width = videoEl.videoWidth;
  canvas.height = videoEl.videoHeight;
  canvas.getContext('2d').drawImage(videoEl, 0, 0);
  return canvas.toDataURL('image/jpeg', 0.9);
}
```

---

## getDisplayMedia — compartilhar tela

```javascript
// Capturar a tela
const screenStream = await navigator.mediaDevices.getDisplayMedia({
  video: { cursor: 'always' }, // 'always' | 'motion' | 'never'
  audio: true,                 // capturar áudio do sistema (suporte limitado)
});

// Combinar câmera + tela (picture-in-picture)
const cameraStream = await navigator.mediaDevices.getUserMedia({ video: true });

const canvas = document.createElement('canvas');
canvas.width = 1280;
canvas.height = 720;
const ctx = canvas.getContext('2d');

function composite(screenVideo, cameraVideo) {
  requestAnimationFrame(() => composite(screenVideo, cameraVideo));
  ctx.drawImage(screenVideo, 0, 0, 1280, 720);
  ctx.drawImage(cameraVideo, 20, 20, 320, 180); // PiP no canto
});
```

---

> [!question] Para fixar
> 1. Qual a diferença entre `getCurrentPosition` e `watchPosition`? Como você cancela o segundo?
> 2. O que o campo `maximumAge` faz nas opções de geolocalização? Quando usar `maximumAge: 0`?
> 3. Qual a diferença entre `acceleration` e `accelerationIncludingGravity`?
> 4. Por que você precisa chamar `stream.getTracks().forEach(t => t.stop())` após usar câmera/microfone?
> 5. O que `facingMode: 'environment'` faz em um dispositivo móvel?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/05 - Notifications e Permissions API|05 — Notifications e Permissions]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/07 - Web Share e outras APIs|07 — Web Share e outras APIs]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/01 - Intersection Observer|01 — Intersection Observer]] — outra API que requer contexto seguro
