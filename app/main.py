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
def plottingRoute(
    request: Request,
    x: str = None,
    y: str = None,
    x_label: str = "X",
    y_label: str = "Y",
    download: int = 0
):
    if download and x is not None and y is not None:
        x_vals = parse_values(x)
        y_vals = parse_values(y)
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=1000)
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png", headers={
            "Content-Disposition": "attachment; filename=plot.png"
        })
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
    plt.savefig(buf, format='png', dpi = 1000)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
@app.get("/data_correlation")
def dataCorrelationRoute(
    request: Request,
    x: str = None,
    y_first: str = None,
    y_second: str = None,
    x_label: str = "X",
    y_first_label: str = "Y1",
    y_second_label: str = "Y2",
    download: int = 0
):
    if x is not None and y_first is not None and y_second is not None:
        x_vals = parse_values(x)
        y_first_vals = parse_values(y_first)
        y_second_vals = parse_values(y_second)
        fig, ax = plt.subplots()
        ax.scatter(x_vals, y_first_vals, label=y_first_label)
        ax.scatter(x_vals, y_second_vals, label=y_second_label)
        ax.set_xlabel(x_label)
        correlation = np.corrcoef(y_first_vals, y_second_vals)[0, 1]
        ax.set_title(f"Correlation: {correlation:.2f}")
        ax.legend()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=1000)
        buf.seek(0)
        headers = {}
        if download:
            headers["Content-Disposition"] = "attachment; filename=correlation_plot.png"
        return StreamingResponse(buf, media_type="image/png", headers=headers)
    # Render HTML page if not all data provided
    return templates.TemplateResponse("data_correlation.html", {"request": request})

@app.get("/data_correlation")
def drawCorrelationRoute(x:str, y_first:str, y_second:str,x_label:str, y_first_label: str, y_second_label: str):
    x = parse_values(x)
    y_first = parse_values(y_first)
    y_second = parse_values(y_second)
    fig, ax = plt.subplots()
    ax.scatter(x, y_first)
    ax.scatter(x, y_second)
    ax.set_xlabel(x_label)
    correlation = np.corrcoef(y_first, y_second)[0, 1]
    ax.set_title(f"Correlation: {correlation:.2f}")
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi = 1000)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
@app.get("/data_correlation")
def downloadCorrelationRoute(x:str, y_first:str, y_second:str, x_label:str, y_first_label: str, y_second_label: str):
    x = parse_values(x)
    y_first = parse_values(y_first)
    y_second = parse_values(y_second)
    fig, ax = plt.subplots()
    ax.scatter(x, y_first)
    ax.scatter(x, y_second)
    ax.set_xlabel(x_label)
    correlation = np.corrcoef(y_first, y_second)[0, 1]
    ax.set_title(f"Correlation: {correlation:.2f}")
    buf = io.BytesIO()
def parse_values(raw):
    items = raw.split(",")
    try:
        return [float(item) for item in items]
    except ValueError:
        return items  
if __name__ == "__main__":
    uvicorn.run("main:app")