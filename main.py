from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()

# Static files (CSS + logo)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "gland_size": None})


@app.post("/", response_class=HTMLResponse)
def get_gland_size(
    request: Request,
    category: str = Form(...),
    cable_type: str | None = Form(None),
    subtype: str | None = Form(None),
    outer_diameter: str | None = Form(None),
    inner_diameter: str | None = Form(None),
):

    # 🔧 Convert blank strings to floats or None safely
    try:
        outer_diameter = float(outer_diameter) if outer_diameter not in (None, "") else None
        inner_diameter = float(inner_diameter) if inner_diameter not in (None, "") else None
    except:
        outer_diameter = None
        inner_diameter = None

    conn = sqlite3.connect("cable_glands.db")
    cursor = conn.cursor()

    # ===================== ⭐ UNARMOURED =====================
    if category == "unarmoured":
        if outer_diameter is None:
            result = "Please enter a cable diameter."
        else:
            cursor.execute("""
                SELECT gland_size
                FROM glands
                WHERE ? BETWEEN min_size AND max_size
                ORDER BY max_size DESC
                LIMIT 1
            """, (outer_diameter,))
            row = cursor.fetchone()
            result = row[0] if row else "No matching gland size found."

        conn.close()
        return templates.TemplateResponse("index.html", {"request": request, "gland_size": result})

    # ===================== 🛡️ ARMOURED =====================
    if subtype is None:
        conn.close()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "gland_size": "Please select a subtype."
        })

    gland_family = subtype  # for building output: E1SW-20S

    # ---- E1SW → strict inner + outer validation ----
    if subtype == "E1SW":
        if outer_diameter is None or inner_diameter is None:
            conn.close()
            return templates.TemplateResponse("index.html", {
                "request": request,
                "gland_size": "Enter BOTH outer & inner diameter for E1SW."
            })

        cursor.execute("""
            SELECT gland_size
            FROM armoured_glands
            WHERE gland_type = 'E1SW'
              AND ? BETWEEN inner_min AND inner_max
              AND ? BETWEEN outer_min AND outer_max
            ORDER BY outer_max DESC
            LIMIT 1
        """, (inner_diameter, outer_diameter))

    # ---- C1W & C1X → outer only ----
    else:
        if outer_diameter is None:
            conn.close()
            return templates.TemplateResponse("index.html", {
                "request": request,
                "gland_size": "Enter outer diameter."
            })

        cursor.execute("""
            SELECT gland_size
            FROM armoured_glands
            WHERE gland_type = ?
              AND ? BETWEEN outer_min AND outer_max
            ORDER BY outer_max DESC
            LIMIT 1
        """, (subtype, outer_diameter))

    row = cursor.fetchone()
    conn.close()

    if row:
        gland_size = row[0]
        full_output = f"{gland_family}-{gland_size}"
    else:
        full_output = "No matching armoured gland size found."

    return templates.TemplateResponse("index.html", {
        "request": request,
        "gland_size": full_output
    })
