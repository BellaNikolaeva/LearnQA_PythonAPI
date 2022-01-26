import requests #импорт библиотеки

response = requests.get('https://playground.learnqa.ru/api/hello') #создание GET-запроса
print(response.text)