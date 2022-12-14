from xmlrpc.client import DateTime
from telethon.sync import TelegramClient
 
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
 
import pandas as pd

from transformers import pipeline



classifier = pipeline('sentiment-analysis',
                      model='blanchefort/rubert-base-cased-sentiment',  # Используемая для классификации модель и её параметры
                      truncation=True,
                      max_length=512)



# В этом блоке ничего трогать не надо, это настроенный блок активации телеграм клиента
api_id = ****
api_hash = '***'            # !!!!! ВНИМАНИЕ !!!!!
phone = '***'               # Для запуска программы здесь нужно указать свои персональные данные клиента telegram

client = TelegramClient(phone, api_id, api_hash)
client.start()
#-------------------------------------------------------------------------------------



def get_participants(link):
    '''
    Функция принимает в качестве аргумента название телеграм-канала в формате 'https://t.me/your_channel',
    осуществляет поиск всех участников в нём и
    возвращает список его участников (user.id, user.username, user.first_name, user.last_name)
    '''
    if not link:
        raise('Empty link')

    all_participants = []
    all_participants = client.get_participants(link)
    users = []

    for user in all_participants:
        one_user = (user.id, user.username, user.first_name, user.last_name)
        users.append(one_user)

    return users


def get_messages(link, msg_limit=10000):
    '''
    Функция принимает в качестве аргумента название телеграм-канала в формате 'https://t.me/your_channel'
    и глубину парсинга (количество считываемых сообщений, по умолчанию 10000),
    осуществляет поиск сообщений всех участников данного канала и
    возвращает список сообщений (message.date, message_user.id, message.text)
    '''
    if not link:
        raise('Empty link')

    all_messages = []

    for message in client.get_messages(link, msg_limit):
        one_mes = (message.date, message.sender_id, message.text)
        all_messages.append(one_mes)

    return all_messages


def read_chat(link, msg_lim=500):
        '''
        Функция читает из чата по переданной ссылке список участников и msg_limit сообщений в датафреймы пандас.
        Потом соединяет эти два датафрейма.
        '''
        users = pd.DataFrame(get_participants(link), columns=['user_id', 'nickname', 'first_name', 'second_name'])
        
        messages = pd.DataFrame(get_messages(link, msg_limit=msg_lim), columns=['datetime', 'user_id', 'text'])
        
        messages.insert(1, 'date', messages.datetime.dt.date)
        
        messages = pd.merge(messages, users, how='left')
        
        return messages


def sentiment_labeling(df):
        '''
        Функция принимает на вход датафрейм с текстами сообщений и размечает тексты тональностью
        (POSITIVE / NEGATIVE / NEUTRAL).
        '''
        sentiment_labels = []

        for text in df.text.values:
                sentiment = classifier(str(text))
                sentiment_labels.append(sentiment[0]['label'])
        
        df.insert(df.shape[1], 'sentiment', sentiment_labels)

        return df


def save_results(df, link):
        '''
        Функция записывает обновленный датафрейм в csv-файл.
        Если чат парсится впервые -- будет создан новый файл, если же чаты уже парсились ранее,
        то в датафрейм будут добавлены новые строки в конец.
        '''
        db_name = './Data/' + link[13:-1] + '.csv'
        print(db_name)
        
        try:
            fd = pd.read_csv(db_name, sep='\t', encoding='utf-8')
            df = pd.concat((fd, df), axis=0)
            df = df.drop_duplicates()
            df.to_csv(db_name, sep='\t', index=False, encoding='utf-8')
        
        except:
            df.to_csv(db_name, sep='\t', index=False, encoding='utf-8')


def json_out(link, msg_limit=10):
        '''
        Функция выводит тональность сообщения через API в формате json.
        '''
        messages = read_chat(link, msg_lim=msg_limit)
        sent_mess = sentiment_labeling(messages)
        return sent_mess.to_json(orient='columns')



#--------------------------------------------------------------------------------------

if __name__ == "__main__":
    with open('./Data/tracks.txt', 'r') as tracker:
        for link in tracker.readlines():
            messages = read_chat(link, msg_lim=10)
            sent_mess = sentiment_labeling(messages)
            save_results(sent_mess, link)
