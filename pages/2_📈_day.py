import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
import pymorphy2
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from wordcloud import WordCloud
import os


st.set_page_config(layout="wide", page_title="Day_stats", page_icon="📈")   # Полнооконное представление приложения
st.write("# Просмотр статистики по дате или периоду")


def find_files():
    for files in os.walk('./Data/'):
        files = files[2]
        files.remove('tracks.txt')
        files = pd.Series(files)
        return files

def preprocess(lst):
    '''Функция принимает на вход список сообщений, предобрабатывает его,
       и возвращет в виде мешка слов'''
    # Приводим к нижнему регистру
    bag = ' '.join(lst).lower()
    # Убираем цифры
    numbers = re.compile(r'\d+')
    bag = re.sub(numbers, '', bag)
    # Убираем пунктуацию
    punct = re.compile(r'[^\w\s]')
    bag = re.sub(punct, '', bag)
    # Удаляем ссылки
    url = re.compile(r'((?<=[^a-zA-Z0-9])(?:https?\:\/\/|[a-zA-Z0-9]{1,}\.{1}|\b)(?:\w{1,}\.{1}){1,5}(?:com|co|org|edu|gov|uk|net|ca|de|jp|fr|au|us|ru|ch|it|nl|se|no|es|mil|iq|io|ac|ly|sm){1}(?:\/[a-zA-Z0-9]{1,})*)')
    bag = re.sub(url, '', bag)
    # Убираем спецсимволы:
    symbols = re.compile(r'\n')
    bag = re.sub(symbols, '', bag)
    # Убираем лишние пробелы
    #extra_spaces = re.compile(r'\s{2,}')
    #bag = re.sub(extra_spaces, ' ', bag)
    # Лемматизация и очистка от стопслов
    morph = pymorphy2.MorphAnalyzer()
    stop = stopwords.words('russian')
    stop.extend(['это', 'весь', 'всё', 'наш', 'ваш', 'который', 'почему'])
    bag = [morph.normal_forms(word)[0] for word in bag.split() if word not in stop]
    return ' '.join(bag)

def show_wordcloud(bag):
    '''
    Рисуем облака слов
    '''
    wordcloud = WordCloud(
            width = 800, 
            height = 800,
            background_color ='white',
            min_font_size = 10
        ).generate(bag)

    ff = plt.figure(figsize=(5, 5))
    plt.imshow(wordcloud)
    plt.axis('off')
    st.pyplot(ff) 

def make_clouds(df):
    '''
    Все функции, в которых есть надпись cloud, работают над созданием облаков слов
    Вот именно эта возвращает мешки слов по негативным комментам и по позитивным
    '''
    positive_list = []
    negative_list = []
    positive_texts = df.index[df.loc[:, 'sentiment'] == 'POSITIVE'].tolist()
    for idx in positive_texts:
        positive_list.append(df.loc[idx, 'text'])

    negative_texts = df.index[df.loc[:, 'sentiment'] == 'NEGATIVE'].tolist()
    for idx in negative_texts:
        negative_list.append(df.loc[idx, 'text'])

    positive_bag = preprocess(positive_list)
    negative_bag = preprocess(negative_list)

    return positive_bag, negative_bag


col1, col2 = st.columns(2)
with col1:
    files = find_files()
    uploaded_file = st.selectbox("Выберите файл чата", files) #
    uploaded_file = './Data/' + uploaded_file

with col2:
    dt = st.date_input("Выберите интересующую дату")
    result = st.button('Проанализировать дату')

if result & (uploaded_file is not None):
    df = pd.read_csv(uploaded_file, sep='\t', encoding='utf-8')
    dt = str(dt)
    if dt in df.date.unique():
        idx = df.date == dt

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f'Тональность комментариев {dt}')
            sentiment_data = df[idx].sentiment.value_counts()
            fig = plt.figure(figsize=(4, 4))
            ax = fig.add_axes((1, 1, 1, 1))
            ax.pie(sentiment_data,
                explode = [0.1, 0.1, 0.1],
                autopct='%1.1f%%',
                textprops={'fontsize': 14},
                labels=sentiment_data.index,
                shadow=True)
            #ax.set_title(f'Тональность сообщений {dt}', size=24)
            st.pyplot(fig)

        with col2:
            st.write('Облако слов положительных комментариев')
            show_wordcloud(make_clouds(df[idx])[0])

        with col3:
            st.write('Облако слов негативных комментариев')
            show_wordcloud(make_clouds(df[idx])[1])
        
            dn = df[idx].drop(columns=['datetime', 'date', 'user_id', 'nickname', 'second_name'])    # Для общего графика нам эти столбцы не нужны
            st.write(f'Сообщения чата за {dt}')
            st.dataframe(dn, width=1000, height=500)

    else:
        st.error('Дата вне диапазона', icon="🚨")

