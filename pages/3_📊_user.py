import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import os


st.set_page_config(layout="wide", page_title="User_stats", page_icon="📊")   # Полнооконное представление приложения
st.write("# Просмотр статистики по пользователям")


def find_files():
    for files in os.walk('./Data/'):
        files = files[2]
        files.remove('tracks.txt')
        files = pd.Series(files)
        return files

files = find_files()
uploaded_file = st.selectbox("Выберите файл чата", files) #
uploaded_file = './Data/' + uploaded_file


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep='\t', encoding='utf-8')
    
    idx = False

    act_user = df.groupby('user_id').text.count().sort_values(ascending=False)[:10]  # Делаю выборку сообщений самых болтливых пользователей

    for user in act_user.index:
        idx = idx | (df.user_id == user)
    df_actusers = df[idx]

    user_sent = df_actusers.pivot_table(  # Делаю сводную таблицу положительных/ нейтральных/ отрицательных комментов между пользователями
        values='text',
        index='user_id',
        columns='sentiment',
        aggfunc='count',
    )

    col1, col2 = st.columns(2)
    with col1:
        st.write('Наиболее активные пользователи')
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_axes((1, 1, 1, 1))
        pie = ax.pie(act_user, labels=act_user.index, autopct='%1.1f%%', startangle=90)   # Диаграмма распределения удельной доли сообщений между пользователями
        st.pyplot(fig)

    with col2:
        st.write('Распределение тональности активных пользователей')
        f, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(data=user_sent,           # А это тепловая карта распределения комментов по их окраске
            annot=True,
            cmap="BuPu",
            );
        st.pyplot(f)


    option = st.selectbox('Выберите пользователя:', df.user_id.sort_values().drop_duplicates())
    st.dataframe(df[df.user_id == option].drop('datetime', axis=1), width=1100, height=500)