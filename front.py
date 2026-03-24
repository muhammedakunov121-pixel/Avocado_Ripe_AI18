import streamlit as st
import requests

st.title('Avocado_ripe')

api_url = 'http://127.0.0.1:8000/predict/'

color_options = ['green', 'dark green', 'purple', 'black']

firmness = st.number_input('firmness', value=1)
hue = st.number_input('hue', step=1)
saturation = st.number_input('saturation', step=1)
brightness = st.number_input('brightness', step=1)
color_category = st.selectbox('color_category', options=color_options)
weight_g = st.number_input('weight_g', value=150, step=1)
size_cm3 = st.number_input('size_cm3', value=200, step=1)
sound_db = 0


avocado_dict = {
    'firmness': firmness,
    'hue': hue,
    'saturation': saturation,
    'brightness': brightness,
    'color_category': color_category,
    'sound_db': sound_db,
    'weight_g': weight_g,
    'size_cm3': size_cm3
}

if st.button('Предсказать на спелость'):
    try:
        with st.spinner('Связываюсь с сервером...'):
            response = requests.post(api_url, json=avocado_dict)

        if response.status_code == 200:
            result = response.json()
            answer = result.get('Answer', 'Нет данных')

            if answer == "Approved":
                st.success(f"Результат: **{answer}** (ripe)")
            else:
                st.success(f"Результат: **{answer}** (not ripe)")
        else:
            st.error(f"Ошибка API (Код {response.status_code})")
            st.json(response.json())  # Покажет детали ошибки от FastAPI

    except requests.exceptions.ConnectionError:
        st.error('Ошибка сервера FastAPI.')
    except Exception as e:
        st.error(f'Произошла непредвиденная ошибка: {e}')
