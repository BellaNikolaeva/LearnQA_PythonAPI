import json

string_as_json_format = '{"answer": "Hello, User"}' #задаем переменную с типом string
obj = json.loads(string_as_json_format) #с помощью библиотеки JSON парсим строку
key = "answer"

if key in obj:
    print(obj[key])
else:
    print(f"Ключа {key} в JSON нет")