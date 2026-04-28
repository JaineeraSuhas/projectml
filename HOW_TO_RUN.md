# How to Run IDCFSS

## One-Time Setup

Open a terminal and run:

```bash
cd C:\Users\ASUS\.gemini\antigravity\scratch\porjectml\backend
pip install -r requirements.txt
```

---

## Run the App (Every Time)

Just **one command**:

```bash
cd C:\Users\ASUS\.gemini\antigravity\scratch\porjectml\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open your browser and go to:

```
http://localhost:8000
```

That's it — frontend + backend served from the **same server**.

---

## What Each Part Does

| URL | What it serves |
|-----|---------------|
| `http://localhost:8000` | The web app (frontend UI) |
| `http://localhost:8000/static/*` | CSS, JS assets |
| `http://localhost:8000/docs` | Auto-generated API docs (Swagger UI) |
| `http://localhost:8000/upload` | API: upload dataset |
| `http://localhost:8000/clean` | API: apply cleaning |
| `http://localhost:8000/features` | API: feature selection |

---

## Stop the Server

Press `Ctrl + C` in the terminal.

---

## Run Tests

```bash
cd C:\Users\ASUS\.gemini\antigravity\scratch\porjectml\backend
pytest ../tests/test_modules.py -v
```
