### HTTP server

Simple currency converter REST server for Python (3.6) using no dependencies beyond the Python standard library.

- Supports USD to RUB currency convert
- Currency rates source: www.cbr.ru via https://www.cbr-xml-daily.ru/daily_json.js
- All responses are converted to JSON 
- Supports get and post requests

Get request format: http://127.0.0.1:8080/convert-usd-to-rub?usd=1

Post request format: 

- url: http://127.0.0.1:8080/convert-usd-to-rub

- Header: Content-type, application/json

- Data: 

  {
      "currency_from": "usd",
      "currency_to": "rub",
      "value": 1
  }

Usage in Ubuntu terminal (Ctrl + Alt + T):

```
python server_app.py
```

For test requests you can use curl commands in terminal:

Get request

```
curl http://127.0.0.1:8080/convert-usd-to-rub?usd=1
```

Post request


```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"currency_from":"usd","currency_to":"rub","value": 1}' \
  http://localhost:8080/convert-usd-to-rub
```

Curl install:  sudo apt install curl

Or you can use Postman. Collection of requests for Postman: https://www.getpostman.com/collections/5a97b37c868534f8722f

To run unittests:

```
python server_app_tests.py
```

For tests requests lib is used. Install requests lib:

```
pip install requests
```