from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os
import subprocess


class Item(BaseModel):
    link: str

app = FastAPI()

info = '- /chats/ \
        - /reload/\
        - /upload/\
        - /addlink/\
        - body form == {"link": "**filename or chat_link**"}'


@app.get("/")
def root():
    '''
    Get-запрос к корневому каталогу. Возвращает текстовое сообщение с описанием доступных функций
    и порядка их вызова.
    '''
    return {"message": info}


@app.get("/chats/")
def find():
    '''
    Get-запрос для получения содержимого папки Data в корневом каталоге. В папке содержатся
    распарсенные сообщения с метками тональности в csv-формате из отслеживаемых телеграм-чатов.
    Запрос возвращает список всех файлов (распарсенных чатов), лежащих в папке.
    '''
    for files in os.walk('./Data/'):
            return files


@app.get("/reload/")
def reload():
    '''
    Get-запрос для запуска скрипта парсера. При отправке этого запроса стартует асинхронный запуск скрипта,
    который скачивает последние 1000 сообщений из отслеживаемых чатов и склеивает их с файлами, в которых
    сохранены результаты предыдущего парсинга. ЗАПРОС НИЧЕГО НЕ ВОЗВРАЩАЕТ! Так как процедура парсинга и 
    разметки длительная по времени, то для скачивания обновленного файла также необходимо выждать время 
    (в зависимости от количества ссылок в трекере).
    '''
    #os.startfile('test.bat') # for windows
    subprocess.Popen(['python3', 'parsr.py']) # for linux
    return {"message": "chats uploading now. You have to wait some time for search uploading files."}


@app.post("/upload/")
def upload(item: Item):
    '''
    Post-запрос для получения содержимого файла из папки Data (размеченных датафреймов с тестами сообщений из
    отслеживаемых чатов). Запросу необходимо передать в качестве параметра link наименование того файла,
    который необходимо переслать. Передача осуществляется в виде текста.
    '''
    return FileResponse("./Data/" + item.link, 
                        filename=item.link, 
                        media_type="file")


@app.post("/addlink/")
def addlink(item: Item):
    '''
    Post-запрос для добавления ссылки на чат в Telegram для его парсинга. Запросу необходимо передать
    в качестве параметра link ссылку на чат в полном виде 'https://t.me/your_channel'.
    После этого, ссылка добавляется в конец файла со ссылками для отслеживания 
    и при очередном сеансе парсинга происходит чудо.
    '''
    with open('./Data/tracks.txt', 'r+') as tracker:
        
        new_link = item.link + '\n'
        
        if new_link in tracker.readlines():
            return {"message": "This link already exist"}
        
        tracker.write(new_link)

    return {"message": "OK"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
