## Как развернуть однонодовый Kafka-кластер

1. Установить docker и docker-compose для Вашей системы
2. Создать файл docker-compose.yml со следующим содержанием (протокол KRaft):

```yaml
version: "3.9"

services:
  kafka-0:
    image: bitnami/kafka:3.4
    ports:
      - "9094:9094"
    environment:
      - KAFKA_ENABLE_KRAFT=yes
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_CFG_NODE_ID=0
      - KAFKA_CFG_PROCESS_ROLES=broker,controller
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka-0:9093
      - KAFKA_KRAFT_CLUSTER_ID=abcdefghijklmnopqrstuv
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093,EXTERNAL://:9094
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-0:9092,EXTERNAL://127.0.0.1:9094
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,PLAINTEXT:PLAINTEXT
    volumes:
      - kafka_0_data:/bitnami/kafka

  ui:
    image: provectuslabs/kafka-ui:v0.7.0
    ports:
      - "8080:8080"
    environment:
      - KAFKA_CLUSTERS_0_BOOTSTRAP_SERVERS=kafka-0:9092
      - KAFKA_CLUSTERS_0_NAME=kraft 

volumes:
  kafka_0_data: 
```

3. Запустить Kafka и UI при помощи команды `docker-compose up -d`

## Как проверить, что кластер работает

1. `docker ps` должен показывать все запущенные контейнеры как "Up", перезапусков быть не должно
2. в логах `docker compose logs` не должно быть ошибок
3. команда `docker exec -it kafka-kafka-0-1 kafka-topics.sh --list --bootstrap-server kafka-0:9092` должна успешно завершаться и выдавать пустой список
4. в kafka ui по адресу http://localhost:8080/ должен отображаться брокер

## Какие параметры конфигурации использовали и что они означают

* KAFKA_ENABLE_KRAFT=yes

Включение протокола KRaft (без Zookeeper)

* ALLOW_PLAINTEXT_LISTENER=yes

Включение возможности работать без tls

* KAFKA_CFG_NODE_ID=0

ID ноды в кластере

* KAFKA_CFG_PROCESS_ROLES=broker,controller

Включение роли broker и controller для ноды (хранение данных + управление конфигурацией)

* KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER

Указание listener CONTROLLER для связи с другими узлами

* KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka-0:9093

Список контроллеров кластера

* KAFKA_KRAFT_CLUSTER_ID=abcdefghijklmnopqrstuv

ID кластера KRaft

* KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093,EXTERNAL://:9094

Список listeners, на которых kafka слушает соединения

* KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-0:9092,EXTERNAL://127.0.0.1:9094

Listeners, которые Kafka предлагает для подключегния клиентов

* KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,PLAINTEXT:PLAINTEXT

Указание, что все listeners используют протокол без шифрования данных

## Как проверить работу Kafka через Kafka UI

1. В Dashboard должен отображаться один кластер в статусе Online
2. В brokers должен отображаться один брокер с "зелёной галочкой"
