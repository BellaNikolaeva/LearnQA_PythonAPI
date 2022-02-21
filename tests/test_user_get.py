import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email' : 'vinkotov@example.com',
            'password' : '1234'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        registration_data = self.prepare_registration_data()

        response_with_registration_data = requests.post("https://playground.learnqa.ru/api/user/", data=registration_data)
        user_id = self.get_json_value(response_with_registration_data, "id")
        Assertions.assert_code_status(response_with_registration_data, 200)
        Assertions.assert_json_has_key(response_with_registration_data, "id")

        response_with_user_id = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid" : auth_sid})

        Assertions.assert_json_has_key(response_with_user_id, "username")
        Assertions.assert_json_has_not_key(response_with_user_id, "email")
        Assertions.assert_json_has_not_key(response_with_user_id, "firstName")
        Assertions.assert_json_has_not_key(response_with_user_id, "lastName")
