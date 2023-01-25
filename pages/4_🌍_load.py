import streamlit as st
import subprocess
import requests


st.set_page_config(layout="wide", page_title="Load_chat", page_icon="🌍")   # Полнооконное представление приложения
st.write("# Загрузка сообщений из чата Telegram по ссылке")


def check_link(link):
    '''
    '''
    if link == '':
        st.error('Ты не прошёл тест на внимательность. Но можешь попытаться ещё раз', icon="🚨")
        return False
    
    if link[0:13] != 'https://t.me/':
        st.error(f'Неправильный формат ссылки {link[0:13]}', icon="🚨")
        return False
    
    if link[0:12] == 'https://t.me/':
        if requests.get(link).status_code != requests.codes.ok: 
            st.error('Нету такого чата...', icon="🚨")
        return False

    if requests.get(link).status_code == requests.codes.ok:
        return True


col1, col2 = st.columns(2)
with col1:
    link = st.text_input('Укажите ссылку на чат Telegramm: ')

with col2:
    number = st.number_input('Укажите количество сообщений, которые нужно проанализировать:', min_value=100, max_value=500000)

col1, col2 = st.columns(2)
with col1:
    filename = st.text_input('Укажите название файла для записи: ', value='my_messages_file.csv')

with col2:
    st.write('Жмакай кнопку только после ввода всего')
    result = st.button('Загрузить сообщения: ')


if result:
    if check_link(link):
        st.success(f'***Ссылка на чат {link} направлена в загрузчик***. \
                    Ожидайте окончания обработки {number} сообщений и появления в папке /Data файла {filename}', icon="✅")
        
        subprocess.Popen(['python', '../parsr.py', link, f'number={number}', filename])