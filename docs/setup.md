# Step 3 — Local setup

## Start the frontend

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Open the local URL shown by Vite, usually `http://localhost:5173`.

## Start the backend

Open a second terminal from the `crop-doctor` folder:

```powershell
backend\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --app-dir backend
```

Open `http://127.0.0.1:8000/api/health`. Expected response:

```json
{"status":"ok","service":"crop-doctor-api"}
```

The interactive API documentation is at `http://127.0.0.1:8000/docs`.
