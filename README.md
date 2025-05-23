## Практическая работа 1

Результаты описаны в [README-kafka.md](README-kafka.md)

## Практическая работа 2

### Архитектура проекта

Архитектура продьюсера и консьюмера схожая. Здесь опишем общие для обоих приложений положения.

* Зависимости управляются и устанавливаются при помощи poetry
* Приложения написаны с использованием фреимворка FastAPI, реализующего обработку запросов при помощи asyncio. 
* FastAPI запускается при помощи сервера Uvicorn. 
* Для непосредственной работы с Kafka используется библиотека aiokafka, для (де)сериализации и работы с Schema Registry используется библиотека confluent-kafka
* Как основа для сериализации и валидации данных выбран фреимворк pydantic, c библиотекой pydantic-avro для генерации Avro-схемы из классов Pydantic
* За подключение и валидацию настроек также отвечает Pydantic, при помощи библиотеки pydantic-settings он считывает информацию из .env-файлов
* Логгирование осуществляется при помощи библиотеки loguru

### Структура проекта

* Исходный код обоих приложений находится в папках src в папках consumer/producer
* Для запуска приложения используется файл src/main.py
    * В нём происходит объявление FastAPI и структур, необходимых для запуска. Клиенты kafka и schema registry хранятся в структуре app FastAPI, которая доступна при каждом запросе, чтобы не запускать консьюмер/продьюсер каждый раз.
* Конфигурация объявляется в файле src/config.py
    * В нём происходит объявление необходимых переменных для работы приложения и их типа
* В файле src/(consumer|producer)/schemas.py находится схема Pydantic для валидации запросов FastAPI и сообщений Kafka 
* В файле src/(consumer|producer)/routers.py подключаются маршруты FastAPI
* В каталоге src/(consumer|producer)/endpoints хранятся методы, которые вызываются FastAPI. У обоих приложений есть хелсчеки

Про реализацию отдельных приложений можно почитать в соответствующих readme:
* producer: [producer/README.md](producer/README.md)
* consumer: [producer/README.md](consumer/README.md)

### Проверка работы приложения

Поднимем kafka и создадим топик

* `docker compose up -d kafka-0 kafka-1 kafka-2`
* `docker compose exec kafka-0 kafka-topics.sh --create --topic practicum --bootstrap-server localhost:9092 --partitions 3 --replication-factor 2`

Поднимем все окружения и отправим 1000 сообщений в kafka через producer

* `docker compose up -d`
* `for i in $(seq 1 1000); do curl -vv -XPOST -d '{"text": "message"}' -H "Content-Type: application/json" localhost:9000/api/v1/kafka/send; done`
* `docker compose logs -f`

В логах должна выводиться обработка отправленных сообщений консьюмерами