QRNexa
======

A fast QR generator with both:

- `main.py`: original Python CLI
- `api.py`: FastAPI backend that serves the fullstack app
- `index.html`: browser UI built with HTML, CSS, and JavaScript

Run the fullstack app:

```bash
uvicorn api:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

The frontend calls `/api/generate` to create Text, WiFi, WhatsApp, UPI, Contact, SMS, Email, and Phone QR PNGs on the backend.

Generated files are stored locally in `output/session` for quick downloads while the app is running. FastAPI clears that session folder when the server starts and when it shuts down.

Deploy on Render Free
---------------------

This app is ready for Render with `render.yaml`.

1. Create a GitHub repository.
2. Push this folder to the repository.
3. Open Render and choose **New > Blueprint**.
4. Connect the GitHub repository.
5. Render will detect `render.yaml` and create the free web service.

Manual Render settings, if you do not use Blueprint:

- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
- Health check path: `/api/health`
