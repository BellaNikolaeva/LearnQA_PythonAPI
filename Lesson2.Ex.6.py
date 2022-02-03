import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
history = response.history
number_of_redirects = len(history)
last_response = history[-1]

print(number_of_redirects)
print(last_response.url)