from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, database

app = FastAPI(title="Гран-при Симрейсинга")

templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=database.engine)


@app.get("/", response_class=HTMLResponse)
def read_gui(request: Request, db: Session = Depends(database.get_db)):
    drivers = db.query(models.Driver).all()
    return templates.TemplateResponse("index.html", {"request": request, "drivers": drivers})


@app.post("/gui/drivers/")
def gui_create_driver(name: str = Form(...), best_lap_time: float = Form(...), db: Session = Depends(database.get_db)):
    new_driver = models.Driver(name=name, best_lap_time=best_lap_time)
    db.add(new_driver)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.get("/gui/delete/{driver_id}")
def gui_delete_driver(driver_id: int, db: Session = Depends(database.get_db)):
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if driver:
        db.delete(driver)
        db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/drivers/")
def list_drivers(db: Session = Depends(database.get_db)):
    return db.query(models.Driver).all()


@app.get("/gui/edit/{driver_id}", response_class=HTMLResponse)
def edit_gui(request: Request, driver_id: int, db: Session = Depends(database.get_db)):
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Гонщик не найден")
    return templates.TemplateResponse("edit.html", {"request": request, "driver": driver})


@app.post("/gui/update/{driver_id}")
def gui_update_driver(
    driver_id: int, 
    name: str = Form(...), 
    best_lap_time: float = Form(...), 
    db: Session = Depends(database.get_db)
):
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if driver:
        driver.name = name
        driver.best_lap_time = best_lap_time
        db.commit()
    return RedirectResponse(url="/", status_code=303)