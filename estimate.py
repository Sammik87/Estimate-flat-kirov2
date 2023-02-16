import streamlit as st
import numpy as np
import pickle
import catboost
from catboost import CatBoostRegressor
import datetime
from streamlit_folium import folium_static
import folium

model = pickle.load(open("cat_model.pkl", "rb"))
now = datetime.datetime.now()

#streamlit run estimate.py

#Метки
so = 0 
sk = 0 
sj = 0 
dol = 0 
sh = 0

#Заголовок
st.markdown('<p style="font-size:30px; color:green;">Оценка стоимости квартир в городе Кирове</p', unsafe_allow_html=True)

#Общая площадь
input_1 = st.number_input(label = '**Общая площадь:**')
if input_1 == 0:
    so = 1 #метка
    st.write('<p style="font-size:14px; color:red;">Введите значение общей площади квартиры!</p', unsafe_allow_html=True)
else:
    #input_1 = float(input_1.replace(',', '.'))
    if ((input_1 < 12) or (input_1 > 317)):
        so = 1 #метка
        st.write('<p style="font-size:14px; color:red;">Общая площадь квартиры должна находиться в диапазоне от 12 кв.м до 317 кв.м!</p', unsafe_allow_html=True)
    else:
        so = 0 #метка
        input_s = np.log(input_1) #логарифм общей площадь
        st.write(input_s)

#Площадь кухни
input_2 = st.number_input(label = '**Площадь кухни:**')
if input_2 == 0:
    sk = 1 #метка
    st.write('<p style="font-size:14px; color:red;">Введите значение площади кухни квартиры!</p', unsafe_allow_html=True)
else:    
    #input_2 = float(input_2.replace(',', '.'))
    if ((input_2 < 2) or (input_2 > 61)):
        sk = 1 #метка
        st.write('<p style="font-size:14px; color:red;">Площадь кухни должна находиться в диапазоне от 2 кв.м до 61 кв.м!</p', unsafe_allow_html=True)
    else:
        sk = 0 #метка
        input_2 = input_2 #площадь кухни
        st.write(input_2)

#Жилая площадь
input_3 = st.number_input(label = '**Жилая площадь:**')
if input_3 == 0:
    sj = 1 #метка
    st.write('<p style="font-size:14px; color:red;">Введите значение жилой площади квартиры!</p', unsafe_allow_html=True)
else:    
    #input_3 = float(input_3.replace(',', '.'))
    if ((input_3 < 4) or (input_3 > 90)):
        sj = 1 #метка
        st.write('<p style="font-size:14px; color:red;">Жилая площадь должна находиться в диапазоне от 4 кв.м до 90 кв.м!</p', unsafe_allow_html=True)
    else:
        sj = 0 #метка
        input_3 = input_3 #площадь кухни
        st.write(input_3)

#Этажность дома
input_4 = int(st.slider('**Этажность дома:**', 1, 27, 5))
st.write(input_4)

#Хронологический возраст дома
input_5 = int(st.slider('**Год постройки дома:**', 1890, now.year, 2000))
input_5 = now.year - input_5 + 1 #хронологический возраст дома
st.write('Хронологический возраст дома:', input_5)

#Долгота
input_6 = st.number_input(label = '**Долгота:**', format = "%.6f")
if input_6 == 0:
    dol = 1 #метка
    st.write('<p style="font-size:14px; color:red;">Введите значение долготы, например, - 49,628919!</p', unsafe_allow_html=True)
else:    
    if len(str(input_6)) < 8:
        dol = 1 #метка
        st.write('<p style="font-size:14px; color:red;">Значение долготы должно содержать не менее 8 символов, например, - 49,628919!</p', unsafe_allow_html=True)
    else:
        dol = 0 #метка
        input_6 = input_6 #долгота
        st.write(input_6)

#Широта
input_7 = st.number_input(label = '**Широта:**', format = "%.6f")
if input_7 == 0:
    sh = 1 #метка
    st.write('<p style="font-size:14px; color:red;">Введите значение долготы, например, - 58,606375!</p', unsafe_allow_html=True)
else:    
    if len(str(input_7)) < 8:
        sh = 1 #метка
        st.write('<p style="font-size:14px; color:red;">Значение долготы должно содержать не менее 8 символов, например, - 58,606375!</p', unsafe_allow_html=True)
    else:
        sh = 0 #метка
        input_7 = input_7 #широта
        st.write(input_7)
        map = folium.Map(location = [58.603595, 49.668023], zoom_start = 10)
        popup = [input_7, input_6]
        folium.Marker(location = [input_7, input_6], popup = popup, icon=folium.Icon(color = 'red')).add_to(map)
        folium_static(map)

#Тип санузла
input_8 = st.selectbox('**Укажите тип санузла:**', 
                      ('совмещенный', 'раздельный'))
#st.write(input_8)
if input_8 == "совмещенный":
    d8 = 1
else: 
    d8 = 0

#Количество комнат
input_9 = st.selectbox('**Укажите количество комнат:**', 
                      ('1к', '2к', '3к', '4к и более', 'студия'))
#st.write(input_9)
if input_9 == "1к":
    d9_1 = 1
    d9_2 = 0
    d9_3 = 0
    d9_4 = 0
    d9_5 = 0
elif input_9 == "2к":
    d9_1 = 0
    d9_2 = 1
    d9_3 = 0
    d9_4 = 0
    d9_5 = 0
elif input_9 == "3к":
    d9_1 = 0
    d9_2 = 0
    d9_3 = 1
    d9_4 = 0
    d9_5 = 0
elif input_9 == "4к и более":
    d9_1 = 0
    d9_2 = 0
    d9_3 = 0
    d9_4 = 1
    d9_5 = 0
else:
    d9_1 = 0
    d9_2 = 0
    d9_3 = 0
    d9_4 = 0
    d9_5 = 1

#Этаж
input_10 = st.selectbox('**Укажите этаж расположения:**', 
                       ('первый', 'последний', 'средний'))
#st.write(input_10)
if input_10 == "первый":
    d10_1 = 1
    d10_2 = 0
    d10_3 = 0
elif input_10 == "последний":
    d10_1 = 0
    d10_2 = 1
    d10_3 = 0
else:
    d10_1 = 0
    d10_2 = 0
    d10_3 = 1

#Материал стен
input_11 = st.selectbox('**Укажите материал стен:**', 
                       ('деревянный', 'кирпичный', 'монолитный', 'панельный'))
#st.write(input_11)
if input_11 == "деревянный":
    d11_1 = 1
    d11_2 = 0
    d11_3 = 0
    d11_4 = 0
elif input_11 == "кирпичный":
    d11_1 = 0
    d11_2 = 1
    d11_3 = 0
    d11_4 = 0
elif input_11 == "монолитный":
    d11_1 = 0
    d11_2 = 0
    d11_3 = 1
    d11_4 = 0
else:
    d11_1 = 0
    d11_2 = 0
    d11_3 = 0
    d11_4 = 1

#Уровень отделки
input_12 = st.selectbox('**Укажите уровень отделки:**', 
                       ('дизайнерский', 'евроремонт', 'стандартный', 'требует ремонта'))
#st.write(input_12)
if input_12 == "дизайнерский":
    d12_1 = 1
    d12_2 = 0
    d12_3 = 0
    d12_4 = 0
elif input_12 == "евроремонт":
    d12_1 = 0
    d12_2 = 1
    d12_3 = 0
    d12_4 = 0
elif input_12 == "стандартный":
    d12_1 = 0
    d12_2 = 0
    d12_3 = 1
    d12_4 = 0
else:
    d12_1 = 0
    d12_2 = 0
    d12_3 = 0
    d12_4 = 1

result = st.button('Определить стоимость')
if result:
    t = so + sk + sj + dol + sh
    if t == 0:
        arr = np.array([[input_s, input_2, input_3, input_4, input_5, input_6, input_7, d8, d9_1, d9_2, d9_3, d9_4, d9_5, 
                         d10_1, d10_2, d10_3, d11_1, d11_2, d11_3, d11_4, d12_1, d12_2, d12_3, d12_4]])
        pred = np.round(np.exp(model.predict(arr)), -3)
        pred_kv = np.round(pred[0]/input_1, 2) #input_1 - площадь
        pred_kv = '{0:,}'.format(pred_kv).replace(',', ' ') #округление и разрядность
        pred = '{0:,}'.format(pred[0]).replace(',', ' ') #округление и разрядность
        st.write('**Стоимость квартиры (руб.):**', pred)
        st.write('**Стоимость квартиры (руб./кв.м):**', pred_kv) 
    else:
        st.write('<p style="font-size:14px; color:red;">Поля выше заполнены не корректно!</p', unsafe_allow_html=True)