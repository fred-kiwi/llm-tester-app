# LLM Tester App

An end-to-end desktop application built with Electron, React, FastAPI, and Llama (via llama.cpp). This project integrates a conversational AI chatbot into a sleek desktop interface, packaged and distributed as an Electron app.

## 🚀 Overview

This application includes:

- **Frontend**: Built using **React**, providing a clean chat interface.
- **Backend**: Built using **FastAPI**, exposing endpoints to interact with the Llama language model.
- **LLM Integration**: Self-hosted AI model (**Llama 2**) via **llama.cpp**.
- **Packaging**: Desktop app packaged with **Electron** and **electron-builder**.

---

## 📂 Project Structure

```
llm-tester-app/
├── backend/            # FastAPI Backend
│   ├── main.py
│   ├── chat.py
│   ├── llama.cpp/
│   │   ├── build/bin/llama-cli
│   │   └── models/*.gguf
│   └── (PyInstaller executable after build)
│
├── frontend/           # React Frontend
│   ├── src/
│   │   ├── components/ChatInterface.tsx
│   │   └── App.tsx
│   └── build/
│
└── electron-app/       # Electron Desktop Wrapper
    ├── main.js
    ├── loading.html
    ├── error.html
    ├── assets/
    └── package.json
```

---

## 🛠️ Tech Stack

- **Electron**: Desktop app container.
- **React**: Frontend UI.
- **FastAPI**: Backend REST API.
- **Llama.cpp**: Self-hosted AI inference.
- **Electron Builder**: Packaging and distribution.

---

## 🧑‍💻 Installation & Setup

### 1. Clone the Repository

```bash
git clone [YOUR_REPOSITORY_URL]
cd llm-tester-app
```

### 2. Set up Llama.cpp (AI Backend)

To set up the Llama.cpp binary:

```bash
cd backend
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
mkdir build
cd build
cmake .. -DLLAMA_METAL=on
cmake --build . --config Release
```

Download your preferred `.gguf` model from [Llama model releases](https://huggingface.co/models) and place it in `llama.cpp/models/`.

Verify your setup by running:

```bash
./bin/llama-cli -m ../models/[MODEL_NAME].gguf --simple-io
```

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Build backend executable
pyinstaller --onefile --target-architecture arm64 --add-data "llama.cpp:llama.cpp" main.py

# Sign the executable (macOS)
codesign --force --deep -s - dist/main
```

### 4. Frontend Setup

```bash
cd ../frontend
npm install
npm run build
```

### 5. Electron App Setup

```bash
cd ../electron-app
npm install
npm run dist  # Builds distributable installers
```

After running this, installers will be generated in the `dist` directory.

---

## 🚀 Running the App (Development)

To run the app locally for development:

- **Backend**:

```bash
cd backend
uvicorn main:app
```

- **Frontend** (if changing React code):

```bash
cd frontend
npm start
```

- **Electron App**:

```bash
cd electron-app
npm start
```

---

## 📦 Packaging for Distribution

To generate an installer for your desktop platform:

```bash
cd electron-app
npm run dist
```

This generates installer files (.dmg for macOS, .exe for Windows) under:

```
electron-app/dist/
```

---

## 🎯 Troubleshooting

- **Backend not starting in packaged Electron app?**

  Ensure paths in `electron-app/package.json` are correct:

  ```json
  "extraResources": [
    {"from": "./backend", "to": "backend"},
    {"from": "./frontend/build", "to": "frontend/build"}
  ]
  ```

- **macOS dyld errors:** Ensure the backend executable is signed and sandbox disabled in Electron (`main.js`):

  ```javascript
  app.commandLine.appendSwitch('no-sandbox');
  app.commandLine.appendSwitch('disable-site-isolation-trials');
  ```

- **Permissions issue on backend executable:**

  Ensure the backend binary has execution permissions:

  ```bash
  chmod +x /path/to/backend/main
  ```

---