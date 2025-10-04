from fastapi import FastAPI, Request, Form
import matplotlib.pyplot as plt
import numpy as np
import uvicorn
import io
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def homepageRoute(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/plotting")
def plottingRoute(request: Request, x: str = None, y: str = None, x_label: str = "X", y_label: str = "Y", download: int = 0):
    if x is not None and y is not None and download:
        x = parse_values(x)
        y = parse_values(y)
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=1000)
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png", headers={
            "Content-Disposition": "attachment; filename=plot.png"
        })
    # Render HTML page if not a download request
    return templates.TemplateResponse("plotting.html", {"request": request})

@app.post("/plotting")
def buildPlot(x: str = Form(...), y: str = Form(...), x_label: str = Form(...), y_label: str = Form(...)):
    x = parse_values(x)
    y = parse_values(y)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=1000)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

def parse_values(raw):
    items = raw.split(",")
    try:
        return [float(item) for item in items]
    except ValueError:
        return items  # оставляем как строки

if __name__ == "__main__":
    uvicorn.run("main:app")