Для закрепления умений по работе с Докером, попрактикуемся в налаживании работы двух отдельных контейнеров, работающих совместно путем общения через интернет

## Шаг 1. Исполняемые файлы приложений

### client.py - 
Простое клиентское приложение получающее get-запрос в цикле каждые 5 секунд
```python
import requests
import json
import time


while True:
    response = requests.get("http://0.0.0.0:1111/")
    print(response.json())
    time.sleep(5)

```

# server
Теперь серверная часть, посылающая запросы
### server.py
```python
from http.server import *
import base64
import time

class Handler(BaseHTTPRequestHandler):
    """ конструируем Get запрос и отправляем"""
    def do_GET(self):
        print("Got request")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"data" : "It\'s working yay"}')
       

class Server(HTTPServer):
    """ инициализируем объект сервера """
    def __init__(self, server_address:  tuple[str, int], RequestHandlerClass, bind_and_activate=...) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)



if __name__ == "__main__":

    print("\n\n")
    server = Server(('0.0.0.0', 1111), Handler)
    print("Starting server %")
    server.serve_forever()
    server.server_close()
```

# Файлы конфигурации контейнеров

### Client Dockerfile
```dockerfile
# Задаем базовый образ. Используем образ python
FROM python:3.10.9
RUN pip3 install requests # устанавливаем библиотеку requests, позволяющую отправлять и получать запросы
ADD client.py /client/ # импортируем файл клиентской программы
WORKDIR /client/ # установим рабочую директорию, откуда будет запущен исполняемый файл
```

### Server Dockerfile
```dockerfile
# Задаем базовый образ. Используем образ python
FROM python:3.10.9
RUN pip3 install requests # устанавливаем библиотеку requests, позволяющую отправлять и получать запросы
ADD server.py /server/ # импортируем файл клиентской программы
WORKDIR /server/ # установим рабочую директорию, откуда будет запущен исполняемый файл
```



# docker-compose.yml
### Финальная часть: тестирование с помощью github actions
```yml
version: "3"

services:

  # Перечислим необходимые сервисы
  # В нашем случае их всего два: сервер и клиент

  server:
 
    # Указываем директорию, содержащую необходимый Dockerfile
    build: server/

    # Сам запуск сервера
    command: python ./server.py

    # Указываем, какие порты пробросить: -[порт компьютера]:[порт контейнера]
    ports:
      - 1111:1111

  # Второй сервис (контейнер): клиент.
  # Этот сервис назван 'client'.

  client:
    build: client/

    command: python ./client.py

    # Указываем тип сети
    # "host" позволяет сервису обращаться к localhost машины
    network_mode: host

    # Буквально задаем зависимости "данного" сервиса от каких-бы то ни было
    # Т.к. клиент без сервера работать не может, то подождем завершения запуска сервера 
    depends_on:
      - server
```
