## Локальная разработка

```bash
poetry install
export PYTHONPATH=.
poetry run python3 src/main.py
```

## Режимы работы

"Обработка" сообщения общая и состоит в выводе десериализованного сообщения из Avro в консоль. Посмотреть можно [тут](src/consumer/service.py) в функции `process_message`

### Режим последовательной обработки

Например, мы хотим последовательно вычитывать сообщения, обрабатывая каждое с автокоммитом

Для этого необходимо выставить параметры так:
```ini
CONSUMER_MESSAGES_BATCH_MIN=1
CONSUMER_MESSAGES_BATCH_MAX=1
CONSUMER_AUTO_COMMIT=true
```

Реализацию последовательной обработки можно посмотреть [тут](src/consumer/service.py) в функции `consume_single`

Приложение в таком режиме будет вычитывать по одному сообщению каждые CONSUMER_POLL_INTERVAL_SECONDS секунд


### Режим пакетной обработки

Например, нам необходимо вычитывать строго по 10 сообщений из каждого топика и коммитить после успешной обработки всех сообщений

Для этого необходимо выставить параметры так:
```ini
CONSUMER_MESSAGES_BATCH_MIN=10
CONSUMER_MESSAGES_BATCH_MAX=10
CONSUMER_AUTO_COMMIT=false
```

Суть реализации пакетной обработки, что приложение перебирает все назначенные партиции каждые CONSUMER_POLL_INTERVAL_SECONDS секунд, и обрабатывает только те из них, где лаг больше, чем CONSUMER_MESSAGES_BATCH_MIN, при этом вычитывает CONSUMER_MESSAGES_BATCH_MAX сообщений.

Реализацию пакетной обработки можно посмотреть [тут](src/consumer/service.py) в функции `consume_batch`