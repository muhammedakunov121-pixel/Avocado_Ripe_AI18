from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uvicorn

avocado_app = FastAPI()

model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

# Словарь для перевода текста в число (как ты просил в самом начале)
color_map = {
    'green': 1,
    'breaking': 2,
    'turning': 3,
    'pink': 4,
    'light-red': 5,
    'red': 6
}


class SchemaAvocado(BaseModel):
    firmness: float
    hue: int
    saturation: int
    brightness: int
    color_category: str  # Принимаем строку ('red', 'green'...)
    sound_db: int
    weight_g: int
    size_cm3: int
    # Поле ripeness УДАЛЯЕМ из ввода, так как это то, что мы хотим УЗНАТЬ


@avocado_app.post('/predict/')
async def predict(avocado: SchemaAvocado):
    data = avocado.model_dump()

    # 1. Переводим строковую категорию цвета в число (1-6)
    # Если цвета нет в словаре, по умолчанию ставим 1
    color_num = color_map.get(data['color_category'].lower().strip(), 1)

    # 2. Собираем СТРОГО 8 признаков в том порядке, в котором они были в таблице при обучении
    # ВАЖНО: Проверь этот порядок со своей таблицей df!
    features = [
        data['firmness'],
        data['hue'],
        data['saturation'],
        data['brightness'],
        color_num,  # Вот наше 5-е число
        data['sound_db'],
        data['weight_g'],
        data['size_cm3']
    ]

    # Теперь в списке ровно 8 элементов. Ошибка X has 10 features исчезнет.
    scaled_data = scaler.transform([features])
    pred = model.predict(scaled_data)[0]

    final_pred = 'ripe' if pred == 1 else 'not ripe'

    return {'Answer': final_pred}


if __name__ == '__main__':
    uvicorn.run(avocado_app, host='127.0.0.1', port=8000)
