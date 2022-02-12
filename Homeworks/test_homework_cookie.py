import requests

class TestHomeworkCookie:
    def test_homework_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        cookies = dict(response.cookies)
        print(cookies)
        assert "HomeWork" in cookies, "There is no cookie in the response"
        assert cookies["HomeWork"] == "hw_value", "Cookies value does not match"