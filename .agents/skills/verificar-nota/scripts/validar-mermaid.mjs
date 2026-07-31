#!/usr/bin/env node
// Valida blocos ```mermaid rodando o parser real do Mermaid.
// Uso: node validar-mermaid.mjs <arquivo.md | pasta>
// Saída vazia = tudo renderiza. Exit code 1 se houver bloco quebrado.

import fs from 'fs';
import path from 'path';

let JSDOM, mermaid;
try {
  ({ JSDOM } = await import('jsdom'));
  const dom = new JSDOM('<!DOCTYPE html><body></body>', { pretendToBeVisual: true });
  global.window = dom.window;
  global.document = dom.window.document;
  Object.defineProperty(global, 'navigator', { value: dom.window.navigator, configurable: true });
  mermaid = (await import('mermaid')).default;
} catch {
  console.error('Dependências ausentes. Rode:  cd ' + import.meta.dirname + ' && npm install');
  process.exit(2);
}
mermaid.initialize({ startOnLoad: false });

const target = process.argv[2];
if (!target) {
  console.error('Uso: node validar-mermaid.mjs <arquivo.md | pasta>');
  process.exit(2);
}

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === '.git' || e.name === 'node_modules') continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith('.md')) out.push(p);
  }
  return out;
}

const files = fs.statSync(target).isDirectory() ? walk(target) : [target];
let blocks = 0;
const bad = [];

for (const f of files) {
  const text = fs.readFileSync(f, 'utf8');
  for (const m of text.matchAll(/```mermaid\n([\s\S]*?)```/g)) {
    blocks++;
    const startLine = text.slice(0, m.index).split('\n').length;
    try {
      await mermaid.parse(m[1]);
    } catch (e) {
      const msg = String(e.message || e);
      const rel = (msg.match(/line (\d+)/) || [])[1];
      const offending = rel ? (m[1].split('\n')[+rel - 1] || '').trim() : '';
      bad.push({ file: f, line: startLine, msg: msg.split('\n')[0], offending });
    }
  }
}

for (const b of bad) {
  console.log(`${b.file}:${b.line}`);
  console.log(`    ${b.msg}`);
  if (b.offending) console.log(`    → ${b.offending.slice(0, 110)}`);
  console.log();
}
console.log(`${blocks} blocos analisados, ${bad.length} quebrados.`);
process.exit(bad.length ? 1 : 0);
