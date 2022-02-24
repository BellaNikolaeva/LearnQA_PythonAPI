import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import random
import allure

@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    missed_params = [
        ("username"),
        ("password"),
        ("email"),
        ("firstName"),
        ("lastName")
    ]

    @allure.description("This test successfully registration")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("positive_case")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test unsuccessfully registration of already registered user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("negative_case")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.description("This test registration with incorrect email")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("negative_case")
    def test_create_user_with_incorrect_email(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}{domain}"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

    @allure.description("This test registration with 1 empty field")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("negative_case")
    @pytest.mark.parametrize('condition', missed_params)
    def test_create_user_without_field(self, condition):
        data = self.prepare_registration_data()
        data.pop(condition)
        data_without_parameter = data

        response = MyRequests.post("/user/", data=data_without_parameter)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}", \
            f"Unexpected response content {response.content} with missed param: {condition}"

    @allure.description("This test registration with short username")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("negative_case")
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        data['firstName'] = ''.join(list(map(chr, [random.randint(98, 122) for i in range(1)])))
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short"

    @allure.description("This test registration with long username")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("negative_case")
    def test_create_user_with_long_username(self) :
        data = self.prepare_registration_data()
        data['firstName'] = ''.join(list(map(chr, [random.randint(98, 122) for i in range(251)])))
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long"

