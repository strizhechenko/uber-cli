[![Code Health](https://landscape.io/github/strizhechenko/uber-cli/master/landscape.svg?style=flat)](https://landscape.io/github/strizhechenko/uber-cli/master)

# Как выглядит

## Утилита

``` shell
$ uber-cli --help
Usage: uber-cli [options]

Options:
  -h, --help            show this help message and exit
  -i SECONDS            delay between queries
  -w, --watch           run query loop
  -o, --one-line        writer format
  -d, --dict            writer format
  --influxdb-format     writer format
  --influxdb-url=URL    Example: http://127.0.0.1:8086/write?db=my_db
  -f FAIR_PRICE, --fair-price=FAIR_PRICE
                        defines fair price that ok to order taxi
$ uber-cli -w "New bar" "Jawsspot"
Time                       : Product      : Min   : Max
2017-05-09 16:10:49.298236 : uberSTART    :  66.0 :  82.0
2017-05-09 16:11:21.143715 : uberSTART    :  66.0 :  82.0
2017-05-09 16:11:52.638423 : uberSTART    :  66.0 :  82.0
```

## Графики

![Скриншот](/images/screenshot_grafana.png)

# Установка

``` shell
pip install uber-cli
```

# Конфигурация

В `$HOME/.uberrc` можно определить несколько переменных

```
DEFAULT_CITY: "Екатеринбург"
DEFAULT_TYPE: "uberSTART"
SERVER_TOKEN: "PUT-YOUR-SERVER-TOKEN-HERE"
PHRASE: "Yo-ho-ho, uber is cheap"
```

- DEFAULT_CITY - чтобы лучше определялась геопозиция лучше указать город в котором закзаываем. Он будет автоматом добавляться при запросе геопозиции.
- DEFAULT_TYPE - тариф убера, который используется там, где показывается только один тариф.
- SERVER_TOKEN - токен, полученный при регистрации приложения в Uber.
- PHRASE - сообщение которое произносится/выводится в случае, если цена на такси подходит вам.

# Регистрация на Uber API

На сайте Uber: https://developer.uber.com/products/ride-requests
