# Предсказание риска сердечного приступа API

## Описание
Приложение на FastAPI для предсказания риска сердечного приступа на основе CSV-файлов с данными пациентов. API принимает путь к CSV-файлу и возвращает предсказания для каждой строки данных.

## Требования
- Python 3.9.21
- Все зависимости указаны в `requirements.txt`

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/dpustyntsev/heart-attack-predictions.git
cd heart_attack
```

2. Создайте и активируйте окружение Conda:

   Официальный сайт: `https://www.anaconda.com/products/distribution`
```bash
conda create -n practicum python=3.9.21
conda activate practicum
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск приложения

1. Запустите сервер FastAPI:
```bash
uvicorn app.main:app --reload
```

2. После запуска приложение c HTML страницей будет доступно по адресу:
`http://127.0.0.1:8000`

3. Вариант взаимодействия через интерфейс Swagger (json записи):
    - Перейдите по ссылке `http://127.0.0.1:8000/docs`
    - Выберите эндпоинт POST /upload/path
    - Нажмите "Try it out", введите json с путем к CSV-файлу, например:
        ```json
        {
        "csv_path": "heart_test.csv"
        }
        ```
    - Нажмите Execute и получите предсказания в json-формате.

4. Вариант взаимодействия через терминал (curl):

    Для Anaconda Prompt / Git Bash
    ```bash
    curl -X POST "http://127.0.0.1:8000/upload/path" -H "Content-Type: application/json" -d "{\"csv_path\": \"heart_test.csv\"}"
    ```
    Для Windows Powershell
    ```bash
    Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:8000/upload/path" -ContentType "application/json" -Body '{"csv_path": "heart_test.csv"}'
    ```

---
## Исследование и модель
Помимо самого API, проект включает исследование данных, поиск и обучение модели (heart_attack.ipynb).

Используемая модель и результаты:
- Модель: CatBoost
- Метрика ROC-AUC на кросс-валидации: 0.606
- Метрика ROC-AUC на валидационной выборке: 0.577