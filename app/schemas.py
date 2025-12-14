from pydantic import BaseModel

#класс, который ожидает запрос в формате JSON с текстовым полем пути к CSV файлу
class PredictRequest(BaseModel):
    csv_path: str