from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uvicorn

avocado_app = FastAPI()

model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

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
    color_category: str
    sound_db: int
    weight_g: int
    size_cm3: int


@avocado_app.post('/predict/')
async def predict(avocado: SchemaAvocado):
    data = avocado.model_dump()


    color_num = color_map.get(data['color_category'].lower().strip(), 1)


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

    scaled_data = scaler.transform([features])
    pred = model.predict(scaled_data)[0]

    final_pred = 'ripe' if pred == 1 else 'not ripe'

    return {'Answer': final_pred}


if __name__ == '__main__':
    uvicorn.run(avocado_app, host='127.0.0.1', port=8000)
