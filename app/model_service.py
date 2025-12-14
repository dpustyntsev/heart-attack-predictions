from joblib import load
import pandas as pd

class ModelService:
    def __init__(self, model_path: str):
        #загрузка модели из указанного пути
        self.model = load(model_path)
        #список колонок для удаления, которых не было в обучении
        self.drop_columns = ['gender', 'unnamed:_0', 'obesity',
                             'diabetes', 'ck-mb', 'troponin']
        #дискретные колонки для заполнения пропусков модой
        self.discrete_cols = ['family_history', 'smoking', 'alcohol_consumption',
                              'diet', 'previous_heart_problems', 'medication_use',
                              'stress_level', 'physical_activity_days_per_week']

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        #приводим имена колонок к общепринятому виду
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        #удаляем все лишние колонки (drop_columns), если они есть
        df = df.drop(columns=[c for c in self.drop_columns if c in df.columns])
        #назначаем id индексом, если есть
        if 'id' in df.columns:
            df = df.set_index('id')
        #заполняем пропуски модой для дискретных признаков
        existing_discrete_cols = [c for c in self.discrete_cols if c in df.columns]
        if existing_discrete_cols:
            df[existing_discrete_cols] = df[existing_discrete_cols].fillna(
                df[existing_discrete_cols].mode().iloc[0]
            )
        #изменяем тип дискретных признаков с float на int
        df[existing_discrete_cols] = df[existing_discrete_cols].astype(int)
        return df

    def predict_from_csv(self, csv_path: str):
        #получаем данные из csv файла
        data = pd.read_csv(csv_path)
        #обрабатываем данные
        data = self.preprocess(data)
        #сохраняем id из индекса
        ids = data.index.tolist()
        #делаем предсказания
        predictions = self.model.predict(data)
        #возвращаем датафрейм с id и предсказанием
        result_df = pd.DataFrame({
            "id": ids,
            "prediction": predictions.astype(int)
        })
        return result_df