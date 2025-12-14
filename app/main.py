from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from app.model_service import ModelService
import shutil
import os
from pathlib import Path
from fastapi import HTTPException
from app.schemas import PredictRequest

#создаем приложение и html шаблон
app = FastAPI(title="Heart Attack Prediction API")
templates = Jinja2Templates(directory="app/templates")

#создаем объект с моделью при старте сервера
model_service = ModelService("model/model.joblib")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    #отображение главной страницы с формой загрузки файла
    return templates.TemplateResponse("upload.html", {"request": request})


#вариант с загрузкой CSV файла через форму
@app.post("/upload", response_class=HTMLResponse)
async def upload_csv(request: Request, file: UploadFile = File(...)):
    #сохраняем временный входной файл
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    #получаем предсказания
    predictions_df = model_service.predict_from_csv(temp_path)
    #создаем папку для результатов
    predictions_dir = Path("predictions")
    predictions_dir.mkdir(exist_ok=True)
    #сохраняем CSV с предсказаниями
    output_path = predictions_dir / "predictions.csv"
    predictions_df.to_csv(output_path, index=False)
    #удаляем временный входной файл
    os.remove(temp_path)
    #для HTML преобразуем в список словарей
    predictions = predictions_df.to_dict(orient="records")
    #возвращаем HTML с таблицей предсказаний
    return templates.TemplateResponse(
        "upload.html",
        {"request": request, "predictions": predictions}
    )


#вариант с передачей пути к CSV файлу через JSON
@app.post("/upload/path")
async def upload_csv_by_path(request: PredictRequest):
    csv_path = request.csv_path
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    #получаем предсказания
    predictions_df = model_service.predict_from_csv(csv_path)
    #создаем папку для результатов
    predictions_dir = Path("predictions")
    predictions_dir.mkdir(exist_ok=True)
    #сохраняем CSV с предсказаниями
    output_path = predictions_dir / "predictions.csv"
    predictions_df.to_csv(output_path, index=False)
    #возвращаем JSON
    return {
        "predictions": predictions_df.to_dict(orient="records")
    }


@app.get("/download")
def download_predictions():
    return FileResponse(
        path="predictions/predictions.csv",
        filename="heart_attack_predictions.csv",
        media_type="text/csv"
    )