# Crop Doctor

AI-Based Crop Disease Detection System — SIH trial project.

## Local prerequisites

Install these before running the application:

1. Node.js LTS (includes npm)
2. Python 3.11 or newer
3. Git
4. VS Code (recommended)

## Verify installation

Open a new PowerShell window and run:

```powershell
node --version
npm.cmd --version
py --version
git --version
```

All four commands must print version numbers.

## Run locally

From the `crop-doctor` folder, open two terminals.

```powershell
# Terminal 1 — backend
backend\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --app-dir backend
```

```powershell
# Terminal 2 — frontend
cd frontend
npm.cmd run dev
```

The frontend runs at `http://localhost:5173`; the API documentation is at
`http://127.0.0.1:8000/docs`.
