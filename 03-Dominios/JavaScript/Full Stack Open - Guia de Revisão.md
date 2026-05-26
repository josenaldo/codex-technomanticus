---
title: "Full Stack Open — Guia de Revisão"
created: 2026-04-11
updated: 2026-04-11
type: how-to
status: evergreen
tags:
  - javascript
  - typescript
  - react
  - nodejs
  - revisao
publish: true
---

# Full Stack Open — Guia de Revisão

Resumo comprehensive em português do curso **[Full Stack Open](https://fullstackopen.com/en/)** da **Universidade de Helsinki** (Department of Computer Science). Um dos melhores cursos gratuitos de desenvolvimento fullstack do mundo, focado em React, Node.js, Express, MongoDB, GraphQL, TypeScript, Redux/Zustand, testes, CI/CD e containers.

Esta nota serve como **guia de consulta rápida para revisão** — organizada parte a parte, com os conceitos essenciais de cada tópico, exemplos de código, armadilhas comuns e conexões com as outras notas técnicas do notebook.

Para fundamentos da linguagem, ver [[JavaScript Fundamentals]]. Para TypeScript, ver [[TypeScript]]. Para React, ver [[React]]. Para testes, ver [[Testes em JavaScript]]. Para Node.js, ver [[Node.js]].

## Sobre o curso

**Criado pela Universidade de Helsinki**, parte do departamento de Computer Science. Gratuito, em inglês (e português/outros idiomas), certificado pela universidade. Reconhecido internacionalmente como uma das melhores introduções práticas a desenvolvimento fullstack moderno.

**Estrutura:** 14 partes (0-13), cada uma equivale a ~1 semana de estudo intenso (10+ horas). Combina teoria, prática guiada e exercícios obrigatórios. Os exercícios constroem uma aplicação completa que evolui ao longo do curso.

**Tecnologias cobertas (2026):**

- React 18+/19 (hooks, componentes, Suspense)
- TypeScript
- Node.js + Express 5
- MongoDB + Mongoose
- Jest / Vitest + React Testing Library
- Playwright (E2E)
- Zustand (state management, substituiu Redux como principal)
- React Query (Tanstack Query)
- GraphQL + Apollo Server 5 / Client 4
- React Native (Parte 10)
- CI/CD (Parte 11, plataforma externa)
- Docker e containers (Parte 12, plataforma externa)
- PostgreSQL + Sequelize (Parte 13, plataforma externa)

**Características únicas:**

- **Exercícios incrementais** — você constrói um app ("Phonebook", "Bloglist") que evolui ao longo de todo o curso
- **Deploy real** — aplicações vão para produção (Render, Fly.io)
- **Práticas modernas** — segue as melhores práticas do ecossistema, atualizado constantemente
- **Sem hand-holding** — incentiva lidar com erros e debugging real

**Como este guia foi organizado:**

Cada parte tem: **objetivo**, **conceitos essenciais**, **exemplos resumidos**, **armadilhas comuns**, e **conexões com outras notas**. O que você não encontra aqui: exercícios (esses ficam no curso em si).

---

# Parte 0 — Fundamentos de aplicações web

**Objetivo:** entender como a web funciona antes de começar a codar. Um bom refresher para devs que aprenderam a usar frameworks sem entender o básico.

## 0.a — General info

Informações sobre o curso, como fazer os exercícios, regras de submissão.

## 0.b — Fundamentos de aplicações web

### Modelo cliente-servidor

```
Client (browser)           Server
      │                      │
      │─── HTTP request ────►│
      │                      │
      │◄── HTTP response ────│
      │                      │
```

Browser envia HTTP request, servidor processa e devolve HTML/CSS/JS. JS executa no browser e pode fazer mais requests.

### DevTools — Network tab

Aprenda a inspecionar requests:

- **Status code** — 200, 301, 404, 500
- **Method** — GET, POST, PUT, DELETE
- **Headers** — Content-Type, Authorization, Cookie
- **Payload** — body da request/response
- **Timing** — quanto tempo cada fase levou

### Traditional multi-page vs SPA

**Multi-page (tradicional):**

- Cada clique → novo HTML do servidor
- Servidor renderiza tudo
- Simples mas lento

**Single Page Application (SPA):**

- Uma página HTML, JavaScript manipula o DOM
- Fetch dados via API (JSON)
- Mais responsivo, experiência de app nativo
- React é SPA por default

### Diagrams importantes

O curso introduz **sequence diagrams** (UML) para visualizar fluxos de request/response. Exercícios iniciais pedem para você desenhar esses diagramas — prática valiosa.

```
Browser                          Server
   │                                │
   ├── GET /notes ─────────────────►│
   │                                │
   │◄────── HTML ───────────────────┤
   │                                │
   ├── GET /style.css ─────────────►│
   │                                │
   │◄────── CSS ────────────────────┤
   │                                │
   ├── GET /script.js ─────────────►│
   │                                │
   │◄────── JS ─────────────────────┤
   │                                │
   ├── GET /api/notes ─────────────►│
   │                                │
   │◄────── JSON ───────────────────┤
```

### HTTP methods idempotência

- **GET** — idempotente, sem side effects
- **POST** — **não** idempotente (cria novo)
- **PUT** — idempotente (substitui)
- **DELETE** — idempotente (remove)

**Armadilha comum:** usar GET para ações que modificam dados (não faça).

### Conexões

- Para aprofundar HTTP: [[Redes e Protocolos]]
- Para aprofundar REST: [[API Design]]

---

# Parte 1 — Introdução ao React

**Objetivo:** primeiros passos com React, componentes, state, eventos, debugging.

## 1.a — Introduction to React

### Setup com Vite (2024+)

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev
```

Vite substituiu Create React App (deprecated). É mais rápido, usa ESM, HMR instantâneo.

### Estrutura mínima

```jsx
// App.jsx
const App = () => {
    const now = new Date();
    const a = 10;
    const b = 20;

    return (
        <div>
            <p>Hello world, it is {now.toString()}</p>
            <p>{a} plus {b} is {a + b}</p>
        </div>
    );
};

export default App;
```

### JSX básico

```jsx
const Header = ({ course }) => <h1>{course}</h1>;

const Content = ({ parts }) => (
    <>
        {parts.map(part => (
            <p key={part.name}>{part.name}: {part.exercises}</p>
        ))}
    </>
);
```

**Regras:** retornar elemento único (ou fragment `<>...</>`), keys em listas, atributos em camelCase, expressões em `{}`.

### Props

```jsx
const Hello = ({ name, age }) => (
    <div>
        <p>Hello {name}, you are {age}</p>
    </div>
);

const App = () => <Hello name="Maria" age={26 + 10} />;
```

## 1.b — JavaScript essencial

O curso faz um **refresher em JavaScript moderno** — arrow functions, destructuring, spread, map/filter/reduce, objetos, classes. Ver [[JavaScript Fundamentals]] para deep dive.

## 1.c — Component state, event handlers

### useState

```jsx
import { useState } from 'react';

const App = () => {
    const [counter, setCounter] = useState(0);

    return (
        <div>
            <p>{counter}</p>
            <button onClick={() => setCounter(counter + 1)}>Plus</button>
            <button onClick={() => setCounter(0)}>Reset</button>
        </div>
    );
};
```

**Regra:** nunca mute state diretamente — sempre crie novo valor.

```jsx
// RUIM
counter = counter + 1;  // não faz nada

// BOM
setCounter(counter + 1);
```

### Event handlers

```jsx
const [value, setValue] = useState('');

<input value={value} onChange={(e) => setValue(e.target.value)} />
```

Input controlado — state React é a source of truth.

### Rendering com state

Quando state muda, React re-renderiza o componente. Todo o código do componente executa de novo (menos os hooks que preservam state).

## 1.d — A more complex state, debugging

### State complexo

```jsx
const [clicks, setClicks] = useState({ left: 0, right: 0 });

const handleLeftClick = () => {
    setClicks({ ...clicks, left: clicks.left + 1 });
};
```

**Regra:** spread para criar novo objeto, nunca mute.

### Array state

```jsx
const [allClicks, setAll] = useState([]);

const handleClick = () => {
    setAll(allClicks.concat('L'));  // concat retorna novo array
    // ou
    setAll([...allClicks, 'L']);
};
```

**Não use** `.push` — `push` muta o array original.

### React DevTools

Instale a extensão do browser. Veja hierarquia de componentes, props, state. Essencial para debug.

### Rules of Hooks

1. Só chame hooks no top level do componente
2. Só chame hooks dentro de função React (componente ou outro hook)
3. Nome de hooks customizados começa com `use`

ESLint plugin `eslint-plugin-react-hooks` ajuda a verificar.

### Conexões

- Deep dive em React: [[React]]
- State management avançado: [[React]] (seção state management)

### Armadilhas comuns parte 1

- **Mutar state** — React não re-renderiza
- **Key duplicada em lista** — comportamento imprevisível
- **Function em vez de valor em setState** quando depende do anterior — use updater function
- **Múltiplos `useState` quando poderia ser um objeto** — ok, não é erro; mas agrupe state relacionado

---

# Parte 2 — Comunicando com o servidor

**Objetivo:** renderizar listas, manipular formulários, buscar dados de API REST, adicionar estilos.

## 2.a — Rendering a collection, modules

### map + key

```jsx
const notes = [
    { id: 1, content: 'HTML is easy', important: true },
    { id: 2, content: 'Browser can execute JS', important: false },
];

<ul>
    {notes.map(note => (
        <li key={note.id}>{note.content}</li>
    ))}
</ul>
```

**Key deve ser:** única entre irmãos, estável (não use index), preferencialmente ID do domínio.

### Extraindo componentes

```jsx
const Note = ({ note }) => <li>{note.content}</li>;

const Notes = ({ notes }) => (
    <ul>
        {notes.map(note => <Note key={note.id} note={note} />)}
    </ul>
);
```

## 2.b — Forms

### Input controlado

```jsx
const App = () => {
    const [notes, setNotes] = useState(initialNotes);
    const [newNote, setNewNote] = useState('');

    const addNote = (event) => {
        event.preventDefault();
        const noteObject = {
            id: notes.length + 1,
            content: newNote,
            important: Math.random() < 0.5
        };
        setNotes(notes.concat(noteObject));
        setNewNote('');
    };

    return (
        <form onSubmit={addNote}>
            <input
                value={newNote}
                onChange={e => setNewNote(e.target.value)}
            />
            <button type="submit">save</button>
        </form>
    );
};
```

**Pontos importantes:**

- `event.preventDefault()` — previne reload da página
- Input controlado — `value` + `onChange`
- Limpar input após submit — `setNewNote('')`

### Filtros dinâmicos

```jsx
const [filter, setFilter] = useState('');

const filteredNotes = notes.filter(note =>
    note.content.toLowerCase().includes(filter.toLowerCase())
);
```

## 2.c — Getting data from server

O curso usa **json-server** para simular um backend REST durante as primeiras partes.

```bash
npx json-server --port 3001 db.json
```

### Axios

```bash
npm install axios
```

```jsx
import axios from 'axios';
import { useState, useEffect } from 'react';

const App = () => {
    const [notes, setNotes] = useState([]);

    useEffect(() => {
        axios
            .get('http://localhost:3001/notes')
            .then(response => setNotes(response.data));
    }, []);  // array vazio — executa 1x no mount
};
```

### useEffect

- **1º argumento:** função (o efeito)
- **2º argumento:** array de dependências
  - `[]` — executa 1x após primeiro render
  - `[valor]` — executa quando `valor` muda
  - sem array — executa após CADA render (raro)

### Fetch vs Axios

Ambos funcionam. Em 2026, `fetch` é nativo em Node e browser. Axios adiciona:

- Transformação JSON automática
- Interceptors (request/response middleware)
- Cancelation (também em fetch via AbortController)
- Request timeout nativo
- Sintaxe mais conveniente

**Escolha do curso:** axios. Na prática moderna, `fetch` + React Query é mais comum.

## 2.d — Altering data in server

### POST, PUT, DELETE

```jsx
// Criar
axios.post('http://localhost:3001/notes', noteObject)
    .then(response => setNotes(notes.concat(response.data)));

// Atualizar
axios.put(`http://localhost:3001/notes/${id}`, changedNote)
    .then(response => {
        setNotes(notes.map(n => n.id !== id ? n : response.data));
    });

// Deletar
axios.delete(`http://localhost:3001/notes/${id}`)
    .then(() => {
        setNotes(notes.filter(n => n.id !== id));
    });
```

### Extraindo para service

```jsx
// services/notes.js
import axios from 'axios';
const baseUrl = 'http://localhost:3001/notes';

const getAll = () => axios.get(baseUrl).then(r => r.data);
const create = (newObject) => axios.post(baseUrl, newObject).then(r => r.data);
const update = (id, newObject) => axios.put(`${baseUrl}/${id}`, newObject).then(r => r.data);

export default { getAll, create, update };

// App.jsx
import noteService from './services/notes';

useEffect(() => {
    noteService.getAll().then(setNotes);
}, []);
```

### Error handling

```jsx
noteService
    .update(id, changedNote)
    .then(returnedNote => { ... })
    .catch(error => {
        setErrorMessage(`Note '${note.content}' was already removed`);
        setTimeout(() => setErrorMessage(null), 5000);
        setNotes(notes.filter(n => n.id !== id));
    });
```

## 2.e — Adding styles to React app

### CSS tradicional

```jsx
// index.css
.note { padding: 10px; }

// App.jsx
import './index.css';

<div className="note">...</div>
```

### Inline styles

```jsx
const style = {
    color: 'red',
    fontSize: '14px',  // camelCase
    padding: 10          // número → px automático
};

<div style={style}>...</div>
```

### Mais moderno (não coberto no curso)

- **Tailwind CSS** — utility-first, padrão em 2026
- **CSS Modules** — scoping automático
- **styled-components/Emotion** — CSS-in-JS (menos popular hoje)

Ver [[HTML e CSS]] para deep dive.

### Conexões

- Fetch e APIs: [[API Design]]
- Estilos: [[HTML e CSS]]
- React Query (melhor que useEffect+fetch): [[React]]

---

# Parte 3 — Programando servidor com Node.js e Express

**Objetivo:** construir o backend em Node.js com Express, persistir dados no MongoDB.

## 3.a — Node.js and Express

### Setup mínimo

```bash
mkdir backend && cd backend
npm init -y
npm install express
```

```javascript
// index.js
const express = require('express');
const app = express();

app.use(express.json());  // parse JSON body

let notes = [
    { id: 1, content: 'HTML is easy', important: true },
    // ...
];

app.get('/', (req, res) => {
    res.send('<h1>Hello World!</h1>');
});

app.get('/api/notes', (req, res) => {
    res.json(notes);
});

const PORT = 3001;
app.listen(PORT, () => console.log(`Server on ${PORT}`));
```

### REST endpoints

```javascript
// GET single
app.get('/api/notes/:id', (req, res) => {
    const id = Number(req.params.id);
    const note = notes.find(n => n.id === id);
    if (note) {
        res.json(note);
    } else {
        res.status(404).end();
    }
});

// POST
app.post('/api/notes', (req, res) => {
    const body = req.body;
    if (!body.content) {
        return res.status(400).json({ error: 'content missing' });
    }
    const note = {
        id: generateId(),
        content: body.content,
        important: body.important || false
    };
    notes = notes.concat(note);
    res.status(201).json(note);
});

// DELETE
app.delete('/api/notes/:id', (req, res) => {
    const id = Number(req.params.id);
    notes = notes.filter(n => n.id !== id);
    res.status(204).end();
});
```

### HTTP status codes

- **200** — OK (GET com body)
- **201** — Created (POST)
- **204** — No Content (DELETE, PUT sem body)
- **400** — Bad Request (payload inválido)
- **401** — Unauthorized
- **403** — Forbidden
- **404** — Not Found
- **500** — Internal Server Error

Ver [[API Design]] para deep dive.

### Middleware

```javascript
// Custom logger
const requestLogger = (req, res, next) => {
    console.log('Method:', req.method);
    console.log('Path:', req.path);
    console.log('Body:', req.body);
    next();
};

app.use(requestLogger);

// Error handler — deve ter 4 args
const errorHandler = (error, req, res, next) => {
    console.error(error.message);
    if (error.name === 'CastError') {
        return res.status(400).json({ error: 'malformatted id' });
    }
    next(error);
};

app.use(errorHandler);  // depois das rotas
```

### CORS

```javascript
const cors = require('cors');
app.use(cors());
```

CORS é mecanismo do browser que bloqueia requests de origens diferentes. O backend precisa permitir explicitamente.

Ver [[API Design]] para deep dive em CORS.

## 3.b — Deploying app to internet

### Build e serve static files

Frontend React é build (`npm run build`) e servido pelo backend:

```javascript
app.use(express.static('dist'));
```

### Deploy (Render, Fly.io)

O curso cobre deploy gratuito. Em produção real, considerar Vercel, Netlify, Railway, Fly.io.

## 3.c — Saving data to MongoDB

### MongoDB + Mongoose

```bash
npm install mongoose
```

```javascript
const mongoose = require('mongoose');

mongoose.connect(url);

const noteSchema = new mongoose.Schema({
    content: String,
    important: Boolean
});

// Transform — remove __v, convert _id to id
noteSchema.set('toJSON', {
    transform: (doc, returnedObject) => {
        returnedObject.id = returnedObject._id.toString();
        delete returnedObject._id;
        delete returnedObject.__v;
    }
});

const Note = mongoose.model('Note', noteSchema);

// Uso
Note.find({}).then(notes => res.json(notes));

const note = new Note({ content: 'Hello', important: true });
note.save().then(saved => res.json(saved));

Note.findById(id).then(note => ...);
Note.findByIdAndUpdate(id, update, { new: true }).then(...);
Note.findByIdAndDelete(id).then(...);
```

### Environment variables

```bash
npm install dotenv
```

```javascript
require('dotenv').config();
const url = process.env.MONGODB_URI;
```

Em Node 20.6+, você pode usar `node --env-file=.env app.js` sem dotenv.

## 3.d — Validation and ESLint

### Mongoose validation

```javascript
const noteSchema = new mongoose.Schema({
    content: {
        type: String,
        minlength: 5,
        required: true
    },
    important: Boolean
});
```

### ESLint

```bash
npm install -D eslint @eslint/js
```

O curso usa a nova flat config (`eslint.config.js`) em vez de `.eslintrc`.

```javascript
// eslint.config.js
import js from '@eslint/js';

export default [
    js.configs.recommended,
    {
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'commonjs'
        },
        rules: {
            'eqeqeq': 'error',
            'no-console': 'warn'
        }
    }
];
```

### Conexões

- Deep dive em Node.js: [[Node.js]]
- REST: [[API Design]]
- Banco de dados: [[Banco de dados]]

### Armadilhas comuns parte 3

- **Esquecer `express.json()`** — `req.body` fica undefined
- **Callbacks dentro de callbacks** — use Promises/async-await
- **CORS não configurado** — browser bloqueia
- **Senha do MongoDB no código** — use env vars
- **Não tratar erros** — app crasha em produção

---

# Parte 4 — Testando servidor Express, administração de usuários

**Objetivo:** organizar o backend em módulos, escrever testes (Jest/Node test runner), implementar autenticação JWT.

## 4.a — Structure of backend application, intro to testing

### Estrutura recomendada

```
backend/
├── controllers/
│   ├── notes.js
│   └── users.js
├── models/
│   ├── note.js
│   └── user.js
├── utils/
│   ├── config.js
│   ├── logger.js
│   └── middleware.js
├── tests/
├── app.js          # express setup
├── index.js        # starts server
└── package.json
```

```javascript
// app.js
const express = require('express');
const app = express();
const cors = require('cors');
const mongoose = require('mongoose');
const config = require('./utils/config');
const notesRouter = require('./controllers/notes');

mongoose.connect(config.MONGODB_URI);

app.use(cors());
app.use(express.json());
app.use('/api/notes', notesRouter);

module.exports = app;

// index.js
const app = require('./app');
const config = require('./utils/config');

app.listen(config.PORT, () => {
    console.log(`Server on ${config.PORT}`);
});
```

### Router

```javascript
// controllers/notes.js
const notesRouter = require('express').Router();
const Note = require('../models/note');

notesRouter.get('/', async (req, res) => {
    const notes = await Note.find({});
    res.json(notes);
});

notesRouter.post('/', async (req, res, next) => {
    try {
        const note = new Note(req.body);
        const saved = await note.save();
        res.status(201).json(saved);
    } catch (e) {
        next(e);
    }
});

module.exports = notesRouter;
```

### express-async-errors (pre Express 5)

Para Express 4, precisa `express-async-errors` para propagar erros async ao error handler:

```javascript
require('express-async-errors');
```

Em Express 5 (default em 2026), async errors são propagados automaticamente.

## 4.b — Testing the backend

### Node.js test runner (nativo)

```javascript
const { test, after, beforeEach, describe } = require('node:test');
const assert = require('node:assert');
const mongoose = require('mongoose');
const supertest = require('supertest');
const app = require('../app');

const api = supertest(app);

beforeEach(async () => {
    await Note.deleteMany({});
    await Note.insertMany(initialNotes);
});

test('notes are returned as json', async () => {
    await api
        .get('/api/notes')
        .expect(200)
        .expect('Content-Type', /application\/json/);
});

test('a specific note can be added', async () => {
    const newNote = { content: 'async/await is cool', important: true };

    await api
        .post('/api/notes')
        .send(newNote)
        .expect(201);

    const response = await api.get('/api/notes');
    assert.strictEqual(response.body.length, initialNotes.length + 1);
});

after(async () => {
    await mongoose.connection.close();
});
```

**Regra essencial:** use banco de teste dedicado (não produção). O curso configura via `NODE_ENV=test`.

### Supertest

Biblioteca para testar APIs HTTP. Monta o app Express em memória, sem servir porta.

```javascript
const supertest = require('supertest');
const api = supertest(app);

await api.get('/api/notes').expect(200);
await api.post('/api/notes').send(data).expect(201);
```

## 4.c — User administration

### Modelo de User

```javascript
const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true, minlength: 3 },
    name: String,
    passwordHash: String,
    notes: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Note' }]
});

userSchema.set('toJSON', {
    transform: (doc, returned) => {
        returned.id = returned._id.toString();
        delete returned._id;
        delete returned.__v;
        delete returned.passwordHash;  // nunca expor!
    }
});
```

### Password hashing com bcrypt

```bash
npm install bcrypt
```

```javascript
const bcrypt = require('bcrypt');

usersRouter.post('/', async (req, res) => {
    const { username, name, password } = req.body;

    const saltRounds = 10;
    const passwordHash = await bcrypt.hash(password, saltRounds);

    const user = new User({ username, name, passwordHash });
    const saved = await user.save();
    res.status(201).json(saved);
});
```

**Nunca** salve senha em plain text. Sempre use bcrypt (ou argon2).

### Populate — resolver references

```javascript
const users = await User.find({}).populate('notes', { content: 1, important: 1 });
```

Substitui os ObjectIds referenciados pelos documentos completos (JOIN em MongoDB).

## 4.d — Token authentication

### JWT

```bash
npm install jsonwebtoken
```

**Login:**

```javascript
const jwt = require('jsonwebtoken');

loginRouter.post('/', async (req, res) => {
    const { username, password } = req.body;

    const user = await User.findOne({ username });
    const passwordCorrect = user === null
        ? false
        : await bcrypt.compare(password, user.passwordHash);

    if (!passwordCorrect) {
        return res.status(401).json({ error: 'invalid username or password' });
    }

    const userForToken = { username: user.username, id: user._id };
    const token = jwt.sign(userForToken, process.env.SECRET, { expiresIn: 60 * 60 });

    res.status(200).json({ token, username, name: user.name });
});
```

**Middleware de autenticação:**

```javascript
const tokenExtractor = (req, res, next) => {
    const auth = req.get('authorization');
    if (auth && auth.startsWith('Bearer ')) {
        req.token = auth.substring(7);
    }
    next();
};

const userExtractor = async (req, res, next) => {
    const decoded = jwt.verify(req.token, process.env.SECRET);
    req.user = await User.findById(decoded.id);
    next();
};

app.use(tokenExtractor);
```

**Usar em rotas:**

```javascript
notesRouter.post('/', userExtractor, async (req, res) => {
    const user = req.user;
    const note = new Note({ ...req.body, user: user._id });
    const saved = await note.save();
    user.notes = user.notes.concat(saved._id);
    await user.save();
    res.status(201).json(saved);
});
```

**Armadilhas JWT:**

- Nunca expor SECRET
- Expiração curta (1h a 24h)
- `alg: none` é vulnerabilidade
- Validar `iss`, `aud`, `exp`

Ver [[Spring Security]] para deep dive em JWT (os conceitos valem para qualquer stack).

### Conexões

- Testing deep dive: [[Testes em JavaScript]]
- API Design e auth: [[API Design]]
- JWT security: [[Spring Security]] (seção JWT)

### Armadilhas comuns parte 4

- **Senha em plain text** — sempre hash
- **JWT sem expiração** — problema de segurança
- **Tests sem cleanup** — banco acumula lixo
- **Uncaught async errors** — use try/catch ou express-async-errors
- **SECRET no git** — env vars

---

# Parte 5 — Testing React apps, React Router

**Objetivo:** login no frontend, testes de componentes React, E2E com Playwright, roteamento, UI frameworks.

## 5.a — Login in frontend

### Form de login

```jsx
const [username, setUsername] = useState('');
const [password, setPassword] = useState('');
const [user, setUser] = useState(null);

const handleLogin = async (event) => {
    event.preventDefault();
    try {
        const user = await loginService.login({ username, password });
        window.localStorage.setItem('loggedUser', JSON.stringify(user));
        noteService.setToken(user.token);
        setUser(user);
        setUsername('');
        setPassword('');
    } catch (error) {
        setErrorMessage('Wrong credentials');
    }
};
```

### Persistir login com localStorage

```jsx
useEffect(() => {
    const loggedUserJSON = window.localStorage.getItem('loggedUser');
    if (loggedUserJSON) {
        const user = JSON.parse(loggedUserJSON);
        setUser(user);
        noteService.setToken(user.token);
    }
}, []);
```

**Armadilha:** localStorage é acessível via XSS. Em 2026, considere **HttpOnly cookies** para tokens sensíveis (requer backend cooperando).

### Token no header

```javascript
// services/notes.js
let token = null;

const setToken = (newToken) => {
    token = `Bearer ${newToken}`;
};

const create = async (newObject) => {
    const config = { headers: { Authorization: token } };
    const res = await axios.post(baseUrl, newObject, config);
    return res.data;
};
```

## 5.b — props.children and component refs

### children

```jsx
const Togglable = ({ children, buttonLabel }) => {
    const [visible, setVisible] = useState(false);
    return (
        <div>
            {!visible && (
                <button onClick={() => setVisible(true)}>{buttonLabel}</button>
            )}
            {visible && (
                <div>
                    {children}
                    <button onClick={() => setVisible(false)}>cancel</button>
                </div>
            )}
        </div>
    );
};

// Uso
<Togglable buttonLabel="new note">
    <NoteForm createNote={addNote} />
</Togglable>
```

### useImperativeHandle + forwardRef

Expor métodos do child para o parent:

```jsx
const Togglable = forwardRef((props, ref) => {
    const [visible, setVisible] = useState(false);

    useImperativeHandle(ref, () => ({
        toggleVisibility: () => setVisible(!visible)
    }));

    return (...);
});

// Parent
const noteFormRef = useRef();
<Togglable ref={noteFormRef} buttonLabel="new note">
    <NoteForm createNote={addNote} />
</Togglable>

// Usar
noteFormRef.current.toggleVisibility();
```

**Em React 19+:** `forwardRef` está sendo gradualmente desnecessário — ref vira prop normal.

## 5.c — Testing React apps

### React Testing Library (Jest ou Vitest)

```jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Note from './Note';

test('renders content', () => {
    const note = { content: 'test content', important: true };

    render(<Note note={note} />);

    expect(screen.getByText('test content')).toBeDefined();
});

test('clicking the button calls event handler', async () => {
    const note = { content: 'test', important: true };
    const mockHandler = vi.fn();

    render(<Note note={note} toggleImportance={mockHandler} />);

    const user = userEvent.setup();
    const button = screen.getByText('make not important');
    await user.click(button);

    expect(mockHandler.mock.calls).toHaveLength(1);
});
```

### userEvent vs fireEvent

- **userEvent** — simula interação real (keyboard focus, hover, múltiplos eventos por ação)
- **fireEvent** — dispara evento único

Use userEvent por default. Ver [[Testes em JavaScript]] para deep dive.

## 5.d — End to end testing

### Playwright

```bash
npm init playwright@latest
```

```javascript
// tests/login.spec.js
const { test, expect } = require('@playwright/test');

test('login shows form', async ({ page }) => {
    await page.goto('http://localhost:5173');
    await expect(page.getByText('login')).toBeVisible();
});

test('user can login', async ({ page }) => {
    await page.goto('http://localhost:5173');
    await page.getByTestId('username').fill('testuser');
    await page.getByTestId('password').fill('testpass');
    await page.getByRole('button', { name: 'login' }).click();
    await expect(page.getByText('testuser logged in')).toBeVisible();
});
```

### Cypress foi removido do curso

O curso migrou de Cypress para Playwright em 2025. Playwright tem:

- Multi-browser nativo (Chromium, Firefox, WebKit)
- API mais moderna (async/await)
- Trace viewer para debugging
- Paralelização nativa

Ver [[Testes em JavaScript]] para deep dive.

### Reset do banco entre testes E2E

O backend expõe endpoint `/api/testing/reset` (apenas em NODE_ENV=test) que limpa o banco.

```javascript
test.beforeEach(async ({ request, page }) => {
    await request.post('http://localhost:3001/api/testing/reset');
    // ... setup
});
```

## 5.e — React Router, UI frameworks

### React Router

```jsx
import { BrowserRouter, Routes, Route, Link, useParams, Navigate } from 'react-router-dom';

const App = () => (
    <BrowserRouter>
        <Link to="/">home</Link>
        <Link to="/notes">notes</Link>

        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/notes" element={<NoteList />} />
            <Route path="/notes/:id" element={<NoteDetail />} />
            <Route path="/login" element={user ? <Navigate to="/" /> : <Login />} />
        </Routes>
    </BrowserRouter>
);

// Dentro de NoteDetail
const { id } = useParams();
```

### UI frameworks

Curso menciona Bootstrap, Material UI, Tailwind. Em 2026, **Tailwind CSS + shadcn/ui** é a stack mais popular. Ver [[HTML e CSS]] e [[React]].

### Conexões

- React deep dive: [[React]]
- Testing JS deep dive: [[Testes em JavaScript]]
- HTML/CSS: [[HTML e CSS]]

### Armadilhas comuns parte 5

- **Token em localStorage** — XSS vulnerability
- **Tests sem limpeza** — state vaza
- **E2E lentos** — use Playwright parallelization
- **`act()` warning no React 18+** — use `async`/`await` em userEvent

---

# Parte 6 — Advanced state management

**Objetivo:** gerenciamento de estado mais robusto que useState. Flux/Zustand, Context API, React Query, Redux (legacy).

**Importante:** em 2025+ o curso **substituiu Redux por Zustand** como principal. Redux continua como referência legacy.

## 6.a — Flux architecture and Zustand

### Zustand

```bash
npm install zustand
```

```javascript
import { create } from 'zustand';

const useCounterStore = create((set) => ({
    count: 0,
    increment: () => set((state) => ({ count: state.count + 1 })),
    decrement: () => set((state) => ({ count: state.count - 1 })),
    reset: () => set({ count: 0 })
}));

// Uso em componente
const Counter = () => {
    const count = useCounterStore((state) => state.count);
    const increment = useCounterStore((state) => state.increment);

    return (
        <div>
            <p>{count}</p>
            <button onClick={increment}>+</button>
        </div>
    );
};
```

### Store pattern

```javascript
const useNotesStore = create((set, get) => ({
    notes: [],

    setNotes: (notes) => set({ notes }),

    addNote: (note) => set((state) => ({
        notes: [...state.notes, note]
    })),

    toggleImportant: (id) => set((state) => ({
        notes: state.notes.map(n =>
            n.id === id ? { ...n, important: !n.important } : n
        )
    })),

    importantCount: () => get().notes.filter(n => n.important).length
}));
```

### Por que Zustand substituiu Redux

|                | Redux                               | Zustand     |
| -------------- | ----------------------------------- | ----------- |
| Boilerplate    | Alto (actions, reducers, selectors) | Mínimo      |
| Provider       | Obrigatório                         | Não precisa |
| Async          | Via thunks/sagas                    | Nativo      |
| TypeScript     | Verboso                             | First-class |
| Bundle         | ~10KB                               | ~1KB        |
| Learning curve | Alta                                | Baixa       |

## 6.b — Complex state, fetch, testing

Testando Zustand stores e componentes com state global.

## 6.c — React Query, Context API with useReducer

### React Query (@tanstack/react-query)

```bash
npm install @tanstack/react-query
```

```jsx
import { useQuery, useMutation, useQueryClient, QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

const App = () => (
    <QueryClientProvider client={queryClient}>
        <NoteList />
    </QueryClientProvider>
);

const NoteList = () => {
    const { data: notes, isLoading } = useQuery({
        queryKey: ['notes'],
        queryFn: () => axios.get('/api/notes').then(r => r.data)
    });

    const queryClient = useQueryClient();
    const newNoteMutation = useMutation({
        mutationFn: (newNote) => axios.post('/api/notes', newNote),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['notes'] })
    });

    if (isLoading) return <div>loading...</div>;

    return (
        <ul>
            {notes.map(n => <li key={n.id}>{n.content}</li>)}
        </ul>
    );
};
```

**Grande insight do curso:** separar **server state** (React Query) de **client state** (Zustand, useState, useReducer). São coisas diferentes.

### useReducer + useContext

```jsx
const notesReducer = (state, action) => {
    switch (action.type) {
        case 'SET':    return action.payload;
        case 'ADD':    return [...state, action.payload];
        case 'TOGGLE': return state.map(n => n.id === action.payload
            ? { ...n, important: !n.important }
            : n
        );
        default: return state;
    }
};

const NotesContext = createContext();

const NotesProvider = ({ children }) => {
    const [notes, dispatch] = useReducer(notesReducer, []);
    return (
        <NotesContext.Provider value={[notes, dispatch]}>
            {children}
        </NotesContext.Provider>
    );
};
```

**Quando usar Context vs Zustand:** Context é built-in mas causa re-render de todos consumers. Zustand é mais performático e ergonômico para state global real.

## 6.d — Redux (legacy)

Material preservado como referência. Redux Toolkit simplifica muito o Redux clássico:

```javascript
import { createSlice, configureStore } from '@reduxjs/toolkit';

const notesSlice = createSlice({
    name: 'notes',
    initialState: [],
    reducers: {
        addNote: (state, action) => { state.push(action.payload); },  // Immer permite
        toggleImportant: (state, action) => {
            const note = state.find(n => n.id === action.payload);
            if (note) note.important = !note.important;
        }
    }
});

const store = configureStore({ reducer: { notes: notesSlice.reducer } });
```

Em 2026, Redux ainda é comum em projetos legacy e equipes grandes. Para novo código, Zustand é simples e suficiente.

### Conexões

- State management deep dive: [[React]]

### Armadilhas comuns parte 6

- **Server state em client store** — use React Query
- **Context para state que muda muito** — re-render em cascata
- **Redux com 50 arquivos para 1 feature** — use Zustand
- **`queryKey` não consistente** — cache bagunçado no React Query

---

# Parte 7 — Mais sobre React hooks e Vite

**Objetivo:** hooks customizados, Vite internals, class components (legacy), error boundaries.

## 7.a — More about React hooks

### Custom hooks

```jsx
// useCounter.js
import { useState } from 'react';

export const useCounter = (initial = 0) => {
    const [value, setValue] = useState(initial);

    return {
        value,
        increment: () => setValue(v => v + 1),
        decrement: () => setValue(v => v - 1),
        zero: () => setValue(0)
    };
};

// Component
const App = () => {
    const counter = useCounter();
    return <button onClick={counter.increment}>{counter.value}</button>;
};
```

### useField hook

```jsx
export const useField = (type) => {
    const [value, setValue] = useState('');
    const onChange = (e) => setValue(e.target.value);
    return { type, value, onChange };
};

// Component
const App = () => {
    const name = useField('text');
    const born = useField('date');

    return (
        <form>
            <input {...name} />
            <input {...born} />
        </form>
    );
};
```

### useResource — API generic

```jsx
export const useResource = (baseUrl) => {
    const [resources, setResources] = useState([]);

    useEffect(() => {
        axios.get(baseUrl).then(r => setResources(r.data));
    }, [baseUrl]);

    const create = async (resource) => {
        const res = await axios.post(baseUrl, resource);
        setResources([...resources, res.data]);
    };

    return [resources, { create }];
};
```

## 7.b — Vite internals and esbuild

### Por que Vite

- **HMR instantâneo** — hot module replacement em ms
- **ESM nativo em dev** — sem bundle no desenvolvimento
- **esbuild** em dev (Go, muito rápido), **Rollup/Rolldown** em produção
- **Zero config** — funciona out of the box

### esbuild vs webpack

|            | webpack      | esbuild             |
| ---------- | ------------ | ------------------- |
| Velocidade | Lento        | 10-100x mais rápido |
| Linguagem  | JS           | Go                  |
| Plugins    | Muito maduro | Crescendo           |
| Maturidade | 2014         | 2020                |

Em 2026, Vite/esbuild é o padrão para React SPAs.

### Configuração Vite

```javascript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,
        proxy: {
            '/api': 'http://localhost:3001'  // evita CORS em dev
        }
    }
});
```

## 7.c — Miscellaneous

### Class components (legacy)

```jsx
class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = { count: 0 };
    }

    handleClick = () => this.setState({ count: this.state.count + 1 });

    render() {
        return <button onClick={this.handleClick}>{this.state.count}</button>;
    }
}
```

**Em 2026:** não escreva class components. Use hooks. Class components são legacy.

### Error boundaries

```jsx
class ErrorBoundary extends React.Component {
    state = { hasError: false };

    static getDerivedStateFromError() {
        return { hasError: true };
    }

    componentDidCatch(error, info) {
        console.error(error, info);
    }

    render() {
        if (this.state.hasError) return <h1>Something went wrong.</h1>;
        return this.props.children;
    }
}

// Uso
<ErrorBoundary>
    <App />
</ErrorBoundary>
```

**Limitações:** não pega erros em event handlers, async, SSR.

**`react-error-boundary`** — biblioteca com API hook-based. Preferível.

### Conexões

- Hooks deep dive: [[React]]

---

# Parte 8 — GraphQL

**Objetivo:** construir servidor GraphQL com Apollo Server 5 e client com Apollo Client 4.

## 8.a — GraphQL server

### GraphQL vs REST

|                | REST                       | GraphQL       |
| -------------- | -------------------------- | ------------- |
| Endpoints      | Múltiplos                  | Um único      |
| Over-fetching  | Comum                      | Mínimo        |
| Under-fetching | Comum (múltiplas requests) | Mínimo        |
| Caching        | HTTP nativo                | Complexo      |
| Typing         | OpenAPI (add-on)           | Schema nativo |

### Schema

```graphql
type Person {
    name: String!
    phone: String
    street: String!
    city: String!
    id: ID!
}

type Query {
    personCount: Int!
    allPersons: [Person!]!
    findPerson(name: String!): Person
}

type Mutation {
    addPerson(name: String!, phone: String, street: String!, city: String!): Person
}
```

### Apollo Server 5

```javascript
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

const typeDefs = `...`;

const resolvers = {
    Query: {
        personCount: () => persons.length,
        allPersons: () => persons,
        findPerson: (root, args) => persons.find(p => p.name === args.name)
    },
    Mutation: {
        addPerson: (root, args) => {
            const person = { ...args, id: uuid() };
            persons.push(person);
            return person;
        }
    }
};

const server = new ApolloServer({ typeDefs, resolvers });
const { url } = await startStandaloneServer(server, { listen: { port: 4000 } });
console.log(`Server ready at: ${url}`);
```

## 8.b — React and GraphQL (Apollo Client 4)

```jsx
import { ApolloClient, InMemoryCache, ApolloProvider, gql, useQuery, useMutation } from '@apollo/client';

const client = new ApolloClient({
    uri: 'http://localhost:4000',
    cache: new InMemoryCache()
});

const ALL_PERSONS = gql`
    query {
        allPersons {
            name
            phone
            id
        }
    }
`;

const App = () => {
    const result = useQuery(ALL_PERSONS);
    if (result.loading) return <div>loading...</div>;
    return <Persons persons={result.data.allPersons} />;
};

// Mutation
const CREATE_PERSON = gql`
    mutation createPerson($name: String!, $street: String!, $city: String!, $phone: String) {
        addPerson(name: $name, street: $street, city: $city, phone: $phone) {
            name
            phone
            id
        }
    }
`;

const [createPerson] = useMutation(CREATE_PERSON, {
    refetchQueries: [{ query: ALL_PERSONS }]
});
```

## 8.c — Database and user administration

Integração com MongoDB via Mongoose, auth com JWT.

## 8.d — Login and updating cache

Cache updates — `refetchQueries` vs `update` function.

## 8.e — Fragments and subscriptions

### Fragments

```graphql
fragment PersonDetails on Person {
    name
    phone
    address { street city }
}

query {
    allPersons {
        ...PersonDetails
    }
}
```

### Subscriptions (WebSocket)

```graphql
type Subscription {
    personAdded: Person!
}
```

Real-time updates via WebSocket.

### Conexões

- REST vs GraphQL: [[API Design]]
- WebSocket: [[Redes e Protocolos]]

### Armadilhas comuns parte 8

- **N+1 no backend** — use DataLoader
- **Over-fetching no client** — use fragments inteligentemente
- **Cache inconsistente** — configure Apollo cache
- **Queries muito profundas sem depth limit** — DoS vector

---

# Parte 9 — TypeScript

**Objetivo:** TypeScript em projetos React e Express.

## 9.a — Background and introduction

TypeScript é superset tipado de JavaScript. Ver [[TypeScript]] para deep dive.

## 9.b — First steps with TypeScript

### Tipos básicos

```typescript
let name: string = 'Maria';
let age: number = 30;
let isActive: boolean = true;
let hobbies: string[] = ['reading', 'coding'];
let tuple: [string, number] = ['Maria', 30];

type Status = 'active' | 'inactive';
let status: Status = 'active';

interface User {
    name: string;
    age: number;
    email?: string;
}
```

### Funções

```typescript
const sum = (a: number, b: number): number => a + b;

const logAndReturn = (value: string): void => {
    console.log(value);
};
```

## 9.c — Typing an Express app

### tsconfig.json

```json
{
    "compilerOptions": {
        "target": "ES2022",
        "module": "commonjs",
        "strict": true,
        "esModuleInterop": true,
        "outDir": "./build"
    },
    "include": ["src"]
}
```

### Express tipado

```typescript
import express, { Request, Response } from 'express';

const app = express();
app.use(express.json());

interface CreateUser {
    name: string;
    age: number;
}

app.post('/users', (req: Request<{}, {}, CreateUser>, res: Response) => {
    const { name, age } = req.body;
    res.json({ name, age });
});
```

### Type narrowing e guards

```typescript
const parseName = (name: unknown): string => {
    if (!name || typeof name !== 'string') {
        throw new Error('invalid name');
    }
    return name;
};
```

## 9.d — React with types

### Componentes tipados

```tsx
interface NoteProps {
    note: {
        id: number;
        content: string;
        important: boolean;
    };
    onToggle: (id: number) => void;
}

const Note = ({ note, onToggle }: NoteProps) => (
    <li>
        {note.content}
        <button onClick={() => onToggle(note.id)}>toggle</button>
    </li>
);
```

### Hooks tipados

```tsx
const [notes, setNotes] = useState<Note[]>([]);
const [user, setUser] = useState<User | null>(null);

const ref = useRef<HTMLInputElement>(null);

// Reducer
type Action = { type: 'ADD'; payload: Note } | { type: 'REMOVE'; id: number };
const [state, dispatch] = useReducer(reducer, initialState);
```

## 9.e — Grande Finale: Patientor

Projeto prático — aplicação de clínica médica em React + Express + TypeScript. Exercita tudo.

### Conexões

- Deep dive TypeScript: [[TypeScript]]
- React com TS: [[React]]

---

# Parte 10 — React Native

**Objetivo:** apps mobile nativos com React Native.

## 10.a — Introduction

### React Native vs Web

- Mesmo conceito (componentes, hooks, state)
- Componentes diferentes: `<View>` em vez de `<div>`, `<Text>` em vez de `<p>`
- Estilização via JavaScript (StyleSheet), não CSS
- Runs em iOS, Android via Metro bundler

### Expo

```bash
npm create expo-app my-app
```

Expo simplifica desenvolvimento — sem precisar de Xcode/Android Studio para muitos casos.

## 10.b — React Native basics

```tsx
import { View, Text, StyleSheet, Pressable } from 'react-native';

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center'
    },
    text: {
        fontSize: 18
    }
});

const App = () => (
    <View style={styles.container}>
        <Text style={styles.text}>Hello React Native!</Text>
        <Pressable onPress={() => alert('clicked')}>
            <Text>Click me</Text>
        </Pressable>
    </View>
);
```

### Flexbox por default

Layout em React Native usa Flexbox **por default** (`display: flex` sempre, `flex-direction: column` sempre).

## 10.c — Communicating with server

Similar a React web — axios ou fetch. Apollo Client funciona também para GraphQL.

## 10.d — Testing and extending

Jest + React Native Testing Library.

### Conexões

- React base: [[React]]
- Async Storage, navegação (React Navigation), push notifications são tópicos abordados mas não na profundidade de uma aula tradicional.

---

# Parte 11 — CI/CD

**Nota:** material movido para plataforma externa (MOOC.fi Continuous Integration course).

**Tópicos principais:**

- **Introdução a CI/CD** — por que automatizar
- **GitHub Actions** — workflows, jobs, steps, triggers
- **Linting, testing, building no CI**
- **Deploy automático**
- **Versionamento semântico**
- **Monitoramento e rollback**

### Exemplo — GitHub Actions

```yaml
name: CI

on:
    push:
        branches: [main]
    pull_request:
        branches: [main]

jobs:
    test:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - uses: actions/setup-node@v4
              with:
                  node-version: '22'
            - run: npm ci
            - run: npm run lint
            - run: npm test
            - run: npm run build

    deploy:
        needs: test
        runs-on: ubuntu-latest
        if: github.ref == 'refs/heads/main'
        steps:
            - uses: actions/checkout@v4
            - run: flyctl deploy
```

---

# Parte 12 — Containers

**Nota:** material movido para plataforma externa (MOOC.fi Containers course).

**Tópicos principais:**

- **Docker fundamentals** — images, containers, volumes, networks
- **Dockerfile** — construir imagens
- **Docker Compose** — orquestrar múltiplos containers
- **Multi-stage builds** — imagens menores
- **Containers para desenvolvimento e produção**

### Exemplo — Dockerfile para Node

```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./
RUN npm ci --production
EXPOSE 3001
CMD ["node", "build/index.js"]
```

### docker-compose.yml

```yaml
services:
    app:
        build: .
        ports:
            - "3001:3001"
        environment:
            - MONGODB_URI=mongodb://mongo:27017/app
        depends_on:
            - mongo

    mongo:
        image: mongo:7
        volumes:
            - mongo-data:/data/db

volumes:
    mongo-data:
```

---

# Parte 13 — Bancos relacionais (PostgreSQL)

**Nota:** material movido para plataforma externa (MOOC.fi Relational Databases course).

**Tópicos principais:**

- **PostgreSQL setup**
- **SQL básico** — SELECT, INSERT, UPDATE, DELETE, JOIN
- **Sequelize ORM**
- **Migrations**
- **Relacionamentos** — 1-1, 1-N, N-N
- **Validações e constraints**
- **Índices e performance**

### Exemplo — Sequelize model

```javascript
const { DataTypes } = require('sequelize');
const { sequelize } = require('../util/db');

const Note = sequelize.define('note', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    content: {
        type: DataTypes.TEXT,
        allowNull: false
    },
    important: {
        type: DataTypes.BOOLEAN,
        defaultValue: false
    },
    date: {
        type: DataTypes.DATE
    }
});

module.exports = Note;
```

### Migrations

```javascript
const { DataTypes } = require('sequelize');

module.exports = {
    up: async ({ context: queryInterface }) => {
        await queryInterface.createTable('notes', {
            id: {
                type: DataTypes.INTEGER,
                primaryKey: true,
                autoIncrement: true
            },
            content: { type: DataTypes.TEXT, allowNull: false },
            important: { type: DataTypes.BOOLEAN, defaultValue: false }
        });
    },
    down: async ({ context: queryInterface }) => {
        await queryInterface.dropTable('notes');
    }
};
```

### Conexões

- Banco de dados: [[Banco de dados]]
- ORM vs raw SQL: [[Spring Data JPA]] (conceitos universais)

---

# Dicas gerais para fazer o curso

## Ordem recomendada

Faça sequencialmente — cada parte depende da anterior.

**Parte 0 → 1 → 2** — React básico
**Parte 3 → 4** — Node.js + Express + MongoDB + testes + auth
**Parte 5 → 6 → 7** — React avançado (testing, state management, hooks custom)
**Parte 8** — GraphQL (opcional se o foco é REST)
**Parte 9** — TypeScript (**essencial** para 2026)
**Parte 10** — React Native (opcional, só se for mexer com mobile)
**Partes 11-13** — CI/CD, Containers, PostgreSQL (em plataformas externas)

## Como estudar efetivamente

1. **Faça os exercícios** — não pule. A aprendizagem vem da prática.
2. **Não copie código** — digite tudo, erre, corrija.
3. **Leia a documentação** — MDN, React docs, Express docs
4. **Use o debugger** — React DevTools, Chrome DevTools
5. **Git commits pequenos** — acostume-se a commitar cada exercício
6. **Deploy real** — Parte 3 pede deploy. Faça, aprenda.
7. **Não pule testes** — testing é fundamental em 2026

## Armadilhas comuns gerais

- **Pular exercícios** — faltam conceitos nas partes seguintes
- **Copiar da internet** — você não aprende
- **Não fazer deploy** — perde uma das melhores partes
- **Parar no meio** — o curso é longo, mas vale cada minuto
- **Ignorar os linters** — ESLint ensina boas práticas
- **Não estudar testes** — testing é parte obrigatória do curso

## O que o curso NÃO cobre (e você deveria estudar depois)

- **Server Components** — Next.js 14+ (React moderno)
- **Arquitetura avançada** — Clean Architecture, DDD → ver [[Arquitetura de Software]]
- **System Design** → ver [[System Design]]
- **Microserviços** → ver [[Arquitetura de Software]]
- **Tailwind CSS** — mencionado, mas não deep dive
- **Mensageria** (Kafka, RabbitMQ) → ver [[Mensageria]]
- **CI/CD real-world** (profundo) — Parte 11 é introdutório

## Depois do curso

1. **Construa um projeto próprio** — aplique o que aprendeu em algo que importa pra você
2. **Contribua em open source** — ache projetos Node/React que aceitam PRs
3. **Aprofunde** — ver [[React]], [[Node.js]], [[TypeScript]], [[Testes em JavaScript]]
4. **Trilha de arquitetura** → [[System Design]], [[Arquitetura de Software]], [[API Design]]
5. **Interview prep** — LeetCode, System Design interviews

---

# Recursos complementares

## Oficial

- [Site do curso](https://fullstackopen.com/en/)
- [GitHub do curso](https://github.com/fullstack-hy2020)
- [Discord oficial](https://fullstackopen.com/en/part0/general_info#parts-and-completion)

## Em português

Parte do material do curso está traduzido para português, mas a recomendação é estudar em inglês — é a língua franca de tecnologia.

## Complementares

### React

- [React.dev](https://react.dev/) — docs oficiais novas
- [Josh Comeau](https://www.joshwcomeau.com/) — tutorials visuais
- [Kent C. Dodds](https://kentcdodds.com/) — Testing Library e patterns
- Ver [[React]] para lista completa

### JavaScript

- [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript) — referência canônica
- [JavaScript.info](https://javascript.info/) — tutorial completo e profundo
- [You Don't Know JS Yet](https://github.com/getify/You-Dont-Know-JS) — Kyle Simpson, gratuito
- Ver [[JavaScript Fundamentals]]

### TypeScript

- [Total TypeScript](https://www.totaltypescript.com/) — Matt Pocock
- [Type Challenges](https://github.com/type-challenges/type-challenges)
- Ver [[TypeScript]]

### Node.js

- [Node.js Docs](https://nodejs.org/docs/)
- Ver [[Node.js]]

### Testing

- [Testing Library Docs](https://testing-library.com/)
- [Playwright Docs](https://playwright.dev/)
- [Vitest Docs](https://vitest.dev/)
- Ver [[Testes em JavaScript]]

---

## Veja também

- [[JavaScript Fundamentals]] — linguagem base
- [[TypeScript]] — sistema de tipos
- [[Testes em JavaScript]] — Vitest, Testing Library, Playwright
- [[React]] — framework UI
- [[Node.js]] — runtime backend
- [[HTML e CSS]] — fundação do frontend
- [[API Design]] — REST, GraphQL, JWT
- [[Banco de dados]] — MongoDB, PostgreSQL, modelagem
- [[Spring Security]] — JWT e auth (conceitos transferíveis)
- [[System Design]] — arquitetura de sistemas
- [[Arquitetura de Software]] — patterns, DDD, Clean Architecture
- [[Helsinki MOOC - Guia de Revisão]] — Java course equivalente (mesma universidade)
