import requests

class TestHomeworkHeader:
    def test_homework_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        headers = response.headers
        assert "x-secret-homework-header" in headers, "There is no header in the response"
        assert headers["x-secret-homework-header"] == "Some secret value", "Headers value does not match"