const { app, BrowserWindow } = require("electron");
const path = require("path");
const { spawn } = require("child_process");
const axios = require("axios");

let backendProcess;
let mainWindow;

function createLoadingWindow() {
    mainWindow = new BrowserWindow({
        width: 900,
        height: 700,
        frame: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    mainWindow.loadFile(path.join(__dirname, "loading.html"));
}

async function waitForBackend(url, interval = 1000, timeout = 30000) {
    const start = Date.now();
    while (Date.now() - start < timeout) {
        try {
            await axios.get(url);
            return true;
        } catch (e) {
            await new Promise(resolve => setTimeout(resolve, interval));
        }
    }
    throw new Error("Backend did not start within timeout.");
}

function startBackend() {
    const backendExecutable = getBackendPath();

    backendProcess = spawn(backendExecutable, [], {
        cwd: path.dirname(backendExecutable),
        env: { ...process.env, PORT: "8000" },
        stdio: ['ignore', 'pipe', 'pipe'],
    });

    backendProcess.stdout.on("data", (data) => {
        console.log(`Backend: ${data}`);
    });

    backendProcess.stderr.on("data", (data) => {
        console.error(`Backend Error: ${data}`);
    });

    backendProcess.on('error', (err) => {
        console.error('Failed to start backend:', err);
    });
}

function getBackendPath() {
    if (app.isPackaged) {
        // Path when packaged by Electron Builder
        return path.join(process.resourcesPath, "backend", "main");
    } else {
        // Development path
        return path.join(__dirname, "backend", "main");
    }
}

async function createMainAppWindow() {
    try {
        await waitForBackend("http://localhost:8000");
        if (app.isPackaged) {
            mainWindow.loadFile(path.join(process.resourcesPath, "frontend", "build", "index.html"));
        } else {
            mainWindow.loadURL(`file://${path.join(__dirname, "frontend/build/index.html")}`);
        }
    } catch (error) {
        mainWindow.loadFile(path.join(__dirname, "error.html"));
        console.error("Backend failed to load in time:", error);
    }
}

app.commandLine.appendSwitch('no-sandbox');
app.commandLine.appendSwitch('disable-site-isolation-trials');

app.whenReady().then(() => {
    startBackend();
    createLoadingWindow();
    createMainAppWindow();
});

app.on("before-quit", () => {
    if (backendProcess) backendProcess.kill();
});