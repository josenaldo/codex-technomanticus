---
title: "Clipboard e File API"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Adepto
tags:
  - plataforma-web
  - web-apis
  - browser
  - javascript
  - clipboard
  - file
  - entrevista
publish: true
---

# Clipboard e File API

> [!abstract] TL;DR
> A Clipboard API (`navigator.clipboard`) permite ler e escrever texto e imagens de forma assíncrona e com permissão do usuário — substituindo o antigo `document.execCommand('copy')`. A File API (`FileReader`, `File`, `Blob`) permite ler arquivos selecionados pelo usuário sem enviá-los ao servidor. Ambas têm restrições de segurança: clipboard exige contexto seguro (HTTPS) e interação do usuário; File API é somente leitura (não acessa o sistema de arquivos arbitrariamente).

---

## Clipboard API — escrita

```javascript
// Copiar texto
async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    console.log('Copiado!');
  } catch (err) {
    console.error('Falha ao copiar:', err);
  }
}

// Copiar conteúdo rich (texto + HTML + imagem)
async function copyRich(text, html) {
  const item = new ClipboardItem({
    'text/plain': new Blob([text], { type: 'text/plain' }),
    'text/html': new Blob([html], { type: 'text/html' }),
  });
  await navigator.clipboard.write([item]);
}

// Copiar imagem
async function copyImage(imageUrl) {
  const response = await fetch(imageUrl);
  const blob = await response.blob();
  const item = new ClipboardItem({ [blob.type]: blob });
  await navigator.clipboard.write([item]);
}
```

---

## Clipboard API — leitura

Requer permissão do usuário (prompt do browser):

```javascript
// Ler texto
async function pasteText() {
  try {
    const text = await navigator.clipboard.readText();
    document.getElementById('editor').value = text;
  } catch (err) {
    // Usuário negou permissão ou não há texto
    console.error('Sem acesso ao clipboard:', err);
  }
}

// Ler itens do clipboard (texto, HTML, imagem)
async function pasteAny() {
  const items = await navigator.clipboard.read();
  
  for (const item of items) {
    for (const type of item.types) {
      const blob = await item.getType(type);
      
      if (type === 'text/plain') {
        const text = await blob.text();
        console.log('Texto:', text);
      } else if (type === 'image/png') {
        const url = URL.createObjectURL(blob);
        document.getElementById('preview').src = url;
      }
    }
  }
}
```

---

## Padrão: botão "Copiar código"

```javascript
function addCopyButtons() {
  document.querySelectorAll('pre code').forEach(code => {
    const button = document.createElement('button');
    button.textContent = 'Copiar';
    button.className = 'copy-btn';
    
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(code.textContent);
        button.textContent = 'Copiado!';
        button.classList.add('copied');
        setTimeout(() => {
          button.textContent = 'Copiar';
          button.classList.remove('copied');
        }, 2000);
      } catch {
        // Fallback para browsers antigos ou sem HTTPS
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(code);
        selection.removeAllRanges();
        selection.addRange(range);
        document.execCommand('copy'); // deprecated mas funciona como fallback
        selection.removeAllRanges();
      }
    });
    
    code.parentElement.style.position = 'relative';
    code.parentElement.appendChild(button);
  });
}
```

---

## File API

O browser expõe arquivos selecionados pelo usuário como objetos `File` (que herdam de `Blob`):

```javascript
const input = document.querySelector('input[type="file"]');

input.addEventListener('change', (event) => {
  const files = event.target.files; // FileList
  
  for (const file of files) {
    file.name;          // 'photo.jpg'
    file.size;          // 1048576 (bytes)
    file.type;          // 'image/jpeg'
    file.lastModified;  // timestamp em ms
    
    // File herda de Blob — pode usar as mesmas operações
    const url = URL.createObjectURL(file); // URL temporária
    const slice = file.slice(0, 1024);    // primeiros 1024 bytes
  }
});
```

---

## Lendo arquivos com FileReader

```javascript
function readFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (event) => resolve(event.target.result);
    reader.onerror = (event) => reject(event.target.error);
    
    // Diferentes métodos de leitura:
    reader.readAsText(file);              // string UTF-8
    reader.readAsDataURL(file);           // data:image/png;base64,...
    reader.readAsArrayBuffer(file);       // ArrayBuffer (dados binários)
    reader.readAsBinaryString(file);      // deprecated — use readAsArrayBuffer
  });
}

// Uso com text
async function displayFile(file) {
  const text = await readFile(file);
  document.getElementById('output').textContent = text;
}
```

> [!tip] API moderna: `file.text()` e `file.arrayBuffer()`
> Como `File` herda de `Blob`, você pode usar os métodos modernos diretamente:
> ```javascript
> const text = await file.text();            // equivalente a readAsText
> const buffer = await file.arrayBuffer();    // equivalente a readAsArrayBuffer
> const url = URL.createObjectURL(file);     // não precisa de FileReader
> ```
> Use `FileReader` apenas quando precisar de progresso (`reader.onprogress`) ou suporte a browsers muito antigos.

---

## Preview de imagem

```javascript
const input = document.querySelector('input[type="file"]');
const preview = document.querySelector('img#preview');

input.addEventListener('change', () => {
  const file = input.files[0];
  if (!file || !file.type.startsWith('image/')) return;
  
  // Criar URL temporária que aponta para o arquivo local
  const url = URL.createObjectURL(file);
  preview.src = url;
  
  // Liberar memória quando não precisar mais
  preview.onload = () => URL.revokeObjectURL(url);
});
```

---

## Drag and drop de arquivos

```javascript
const dropzone = document.getElementById('dropzone');

dropzone.addEventListener('dragover', (event) => {
  event.preventDefault(); // necessário para permitir o drop
  dropzone.classList.add('drag-over');
});

dropzone.addEventListener('dragleave', () => {
  dropzone.classList.remove('drag-over');
});

dropzone.addEventListener('drop', async (event) => {
  event.preventDefault();
  dropzone.classList.remove('drag-over');
  
  const files = event.dataTransfer.files;
  
  for (const file of files) {
    if (file.type.startsWith('image/')) {
      const url = URL.createObjectURL(file);
      addPreview(url);
    }
    
    // Verificar tamanho antes de processar
    const MAX_SIZE = 10 * 1024 * 1024; // 10MB
    if (file.size > MAX_SIZE) {
      alert(`${file.name} é muito grande (máx 10MB)`);
      continue;
    }
    
    await uploadFile(file);
  }
});
```

---

## Upload com progresso

```javascript
async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  // XMLHttpRequest para progresso (fetch não expõe progresso nativo ainda)
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    
    xhr.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable) {
        const percent = (event.loaded / event.total) * 100;
        updateProgressBar(percent);
      }
    });
    
    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.response));
      } else {
        reject(new Error(`Upload falhou: ${xhr.status}`));
      }
    });
    
    xhr.addEventListener('error', () => reject(new Error('Erro de rede')));
    xhr.open('POST', '/api/upload');
    xhr.send(formData);
  });
}
```

> [!info] fetch + ReadableStream para progresso
> O fetch com `ReadableStream` pode monitorar progresso de download, mas progresso de upload ainda não é bem suportado. Para upload com progresso, XHR é a opção mais robusta em 2024.

---

## Validação de tipo de arquivo

```javascript
const ALLOWED_TYPES = new Set(['image/jpeg', 'image/png', 'image/webp', 'image/gif']);
const MAX_SIZE = 5 * 1024 * 1024; // 5MB

function validateFile(file) {
  // Verificar tipo pelo MIME type (pode ser falsificado — verificar no servidor também)
  if (!ALLOWED_TYPES.has(file.type)) {
    return { valid: false, error: 'Tipo de arquivo não permitido. Use JPEG, PNG, WebP ou GIF.' };
  }
  
  // Verificar extensão como segunda camada (para browsers que não expõem MIME)
  const extension = file.name.split('.').pop()?.toLowerCase();
  const ALLOWED_EXTENSIONS = new Set(['jpg', 'jpeg', 'png', 'webp', 'gif']);
  if (!ALLOWED_EXTENSIONS.has(extension)) {
    return { valid: false, error: 'Extensão de arquivo não permitida.' };
  }
  
  if (file.size > MAX_SIZE) {
    return { valid: false, error: `Arquivo muito grande. Máximo: ${MAX_SIZE / 1024 / 1024}MB.` };
  }
  
  return { valid: true };
}
```

---

> [!question] Para fixar
> 1. Por que `navigator.clipboard.writeText` é assíncrono? O que pode dar errado?
> 2. Qual a diferença entre `FileReader.readAsDataURL()` e `URL.createObjectURL()`? Quando usar cada um?
> 3. Por que é importante chamar `URL.revokeObjectURL()` após usar? O que acontece se não chamar?
> 4. Por que validar o tipo de arquivo no cliente não é suficiente de segurança? O que deve ser feito também?
> 5. Por que usar XHR em vez de fetch para upload com barra de progresso?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/03 - History API e SPA routing|03 — History API]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/05 - Notifications e Permissions API|05 — Notifications e Permissions]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/07 - Padrões avançados|Eventos 07 — Drag and Drop nativo]] — context do evento dragover/drop
