import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

#создание новой задачи
responseNewTask = requests.get(url)
parsingResponseNewTask = responseNewTask.json()
token = parsingResponseNewTask["token"]
taskExecutionTime = parsingResponseNewTask["seconds"]

#запрос с параметром token до того, как задача готова
responseTaskNotReady = requests.get(url, params = {"token": "%s" % token})
parsingResponseTaskNotReady = responseTaskNotReady.json()
if parsingResponseTaskNotReady["status"] == "Job is NOT ready":
    print("Запрос до готовности задачи выполнен успешно")
else:
    print("Ошибка: Запрос выполнен после готовности задачи")

#запрос с параметром token после того, как задача готова
time.sleep(taskExecutionTime)
responseTaskReady = requests.get(url, params = {"token": "%s" % token})
parsingResponseTaskReady = responseTaskReady.json()
if parsingResponseTaskReady["status"] == "Job is ready":
    print("Запрос после готовности задачи выполнен успешно")
    try:
        print("Результат: %s"% parsingResponseTaskReady["result"])
    except:
        print("Ошибка: Поле result отсутствует")
else:
    print("Ошибка: Запрос выполнен до готовности задачи")