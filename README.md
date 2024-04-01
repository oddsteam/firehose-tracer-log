## Firehose Tracer Log

## Pre-requisites


## Installation

Create visual environment (optional)

```
$ python3 -m venv ~/.virtualenvs/blocktrade
$ source ~/.virtualenvs/blocktrade/bin/activate
```

Use the below command to execute
````
$ pip install -r requirements.txt
$ touch ./logs/log.txt
````

Start RabbitMQ on blocktrade-service
````
$ cd blocktrade-service
$ docker-compose up -d
````

Back to firehose-tracer-log
```
$ python main.py
```

