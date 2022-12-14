# Приложение для определения тональности сообщений чатов телеграм-каналов

[![Tests](https://github.com/YaRoLit/Fast-api-app/actions/workflows/python-app.yml/badge.svg)](https://github.com/YaRoLit/Fast-api-app/actions/workflows/python-app.yml)

Программа состоит из двух связанных модулей:

1. Модуль ***parsr.py*** предназначен для скачивания интересующего чата Telegram, его предобработки (разметки каждого из сообщений в чате по тональности с помощью используемой предобученной модели, добавлении к цифровому идентификатору пользователя его никнеймов и т.п.). ***Parsr.py*** может использоваться как автономно (и в таком случае выполняет однократное скачивание отслеживаемых чатов и их обогащение при каждом запуске), так и в качестве подгружаемого модуля в другом скрипте, для чего его код разбит на ряд логически обособленных функций (загрузки сообщений, их предобработки, разметки, сохранения и т.п.). В качестве финальной реализации предусматривается автономная работа модуля, его регулярный запуск по расписанию (несколько раз в сутки) на виртуальной машине, в результате чего будет осуществляться скачивание сообщений по отслеживаемым чатам, их разметка и сохранение.

2. Модуль ***fst_api.py*** является вспомогательным по отношению к ***parsr.py*** и предназначен для работы с ним удалённо при помощи GET и POST запросов. Функции модуля позволяют получать список файлов, содержащих сообщения из отслеживаемых чатов, а также скачивать сообщения из конкретного файла при POST указании его наименования. С помощью модуля можно добавлять ссылки для отслеживания и инициировать запуск процедуры парсинга и разметки тональностью, с последующим сохранением в файл. Запуск загрузки осуществляется с помощью вызова ***parsr.py*** через bat.файл, таким образом эмулируется асинхронное выполнение этой процедуры, так как она очень длительная.

> **ВНИМАНИЕ!!!** Из модуля ***parsr.py*** удалены персональные данные, необходимые для активации Telegram клиента (указание на них есть в коде после загрузки библиотек). Для проверки работоспособности и запуска модулей необходимо получить в Telegram и указать свои персональные данные. При необходимости работоспособность модулей может быть продемонстрирована участниками проекта со своими персональными данными дистанционно (скоро запустим виртуальную машину на Яндексе).

Для корректной работы приложения, необходима установка библиотек из файла requirements:

    !pip install -r requirements.txt

Участники проекта:

- Анисимова Татьяна Александровна
- Литаврин Ярослав Игоревич
- Охотников Павел Юрьевич
