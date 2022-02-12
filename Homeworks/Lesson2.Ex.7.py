import requests

#выполнение http-запросов без параметра method
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Response_post: %s"%response.text)
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Response_get: %s"%response.text)
response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Response_put: %s"%response.text)
response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Response_delete: %s"%response.text)

#выполнение http-запроса не из списка
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("Response_notInTheList: %s"%response.text)
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":'HEAD'})
print("Response_notInTheList: %s"%response.text)

#выполнение http-запросов с параметром method
methods = ['POST','GET','PUT','DELETE']
for i in methods:
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":'%s'%i})
    if i == 'POST':
        if response.text != '{"success":"!"}':
            print('Ошибка: POST-запрос не распознал параметр method=%s'%i)
    else:
        if response.text == '{"success":"!"}':
            print('Ошибка: POST-запрос работает в паре с параметром method=%s'%i)

for i in methods:
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method":'%s'%i})
    if i == 'GET':
        if response.text != '{"success":"!"}' :
            print('Ошибка: GET-запрос не распознал параметр method=%s'%i)
    else :
        if response.text == '{"success":"!"}' :
            print('Ошибка: GET-запрос работает в паре с параметром method=%s'%i)

for i in methods:
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":'%s'%i})
    if i == 'PUT':
        if response.text != '{"success":"!"}' :
            print('Ошибка: PUT-запрос не распознал параметр method=%s'%i)
    else:
        if response.text == '{"success":"!"}' :
            print('Ошибка: PUT-запрос работает в паре с параметром method=%s'%i)

for i in methods:
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":'%s'%i})
    if i == 'DELETE':
        if response.text != '{"success":"!"}':
            print('Ошибка: DELETE-запрос не распознал параметр method=%s'%i)
    else:
        if response.text == '{"success":"!"}':
            print('Ошибка: DELETE-запрос работает в паре с параметром method=%s'%i)