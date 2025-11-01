from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()

# Mount static folder (for logo + css)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Home route (renders form)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "gland_size": None})

# Handle form submission
@app.post("/", response_class=HTMLResponse)
def get_gland_size(request: Request, cable_size: float = Form(...)):
    conn = sqlite3.connect("cable_glands.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT gland_size FROM glands
        WHERE ? BETWEEN min_size AND max_size
    """, (cable_size,))
    result = cursor.fetchone()

    conn.close()

    if result:
        gland_size = result[0]
    else:
        gland_size = "No matching gland size found."

    return templates.TemplateResponse("index.html", {"request": request, "gland_size": gland_size})
