import streamlit as st
import pandas as pd
import altair as alt
import os


def find_files():
    for files in os.walk('./Data/'):
        files = files[2]
        files.remove('tracks.txt')
        files = pd.Series(files)
        return files


st.set_page_config(layout="wide", page_title="Main_diag", page_icon="🏠")   # Полнооконное представление приложения
alt.themes.enable('streamlit')      # Эта срань сильно меняет цветовую раскладку, но почему-то без неё не запускается интерактив

st.write("# Приложение для анализа тональности сообщений в чатах Telegram")
st.sidebar.success("Выберите интересующую отчётность")

files = find_files()

uploaded_file = st.selectbox("Выберите файл чата", files) #
uploaded_file = './Data/' + uploaded_file

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep='\t', encoding='utf-8')
    dn = df.drop(columns=['datetime', 'user_id', 'nickname', 'second_name'])    # Для общего графика нам эти столбцы не нужны
    #dn.sort_values(by='date', ascending=True, inplace=True)
    dn = dn.groupby(['date', 'sentiment']).text.count()     # Группируем для отрисовки каждой тональности отдельной линией
    dn = dn.to_frame().reset_index()    # Альтаировская (да и другая) отрисовка криво работает с Series, переводим в Frame

    chart = (
        alt.Chart(dn)
        #.mark_area(opacity=0.3)    # Здесь можно поставить отрисовку площадями
        .mark_line()                # Или отрисовку линиями, как здесь
        .encode(
            x="date:T",
            y=alt.Y("text:Q", stack=None),
            color="sentiment:N",
        )
        .interactive()              # Эта хрень для того, чтобы показывала дату при наведении на пик на графике
    )
    st.altair_chart(chart.interactive(), use_container_width=True)
