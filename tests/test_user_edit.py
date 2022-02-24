from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import random
import allure

@allure.epic("Check edit cases")
class TestUserEdit(BaseCase):

    @allure.description("This test edit of created user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("positive_case")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test edit of non-authorized user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("negative_case")
    def test_edit_not_auth_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response_register_data = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response_register_data, 200)
        Assertions.assert_json_has_key(response_register_data, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response_register_data, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response_login_data = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login_data, "auth_sid")
        token = self.get_header(response_login_data, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 400)

        # GET
        response_user_id = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response_user_id,
            "firstName",
            first_name,
            "Wrong name of the user after edit without authorization"
        )

    @allure.description("This test edit by another user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("negative_case")
    def test_edit_user_by_another_user(self):
        # REGISTER (user)
        register_data_user = self.prepare_registration_data()

        response_register_data_user = MyRequests.post("/user/", data=register_data_user)

        Assertions.assert_code_status(response_register_data_user, 200)
        Assertions.assert_json_has_key(response_register_data_user, "id")

        email_user = register_data_user['email']
        first_name_user = register_data_user['firstName']
        password_user = register_data_user['password']
        user_id = self.get_json_value(response_register_data_user, "id")

        # REGISTER (another user)
        register_data_another_user = self.prepare_registration_data()

        response_register_data_another_user = MyRequests.post("/user/",
                                                            data=register_data_another_user)

        Assertions.assert_code_status(response_register_data_another_user, 200)
        Assertions.assert_json_has_key(response_register_data_another_user, "id")

        email_another_user = register_data_another_user['email']
        first_name_another_user = register_data_another_user['firstName']
        password_another_user = register_data_another_user['password']
        another_user_id = self.get_json_value(response_register_data_another_user, "id")

        # LOGIN (user)
        login_data_user = {
            'email': email_user,
            'password': password_user
        }

        response_login_data_user = MyRequests.post("/user/login", data=login_data_user)

        auth_sid_user = self.get_cookie(response_login_data_user, "auth_sid")
        token_user = self.get_header(response_login_data_user, "x-csrf-token")

        # LOGIN (another user)
        login_data_another_user = {
            'email': email_another_user,
            'password': password_another_user
        }

        response_login_data_another_user = MyRequests.post("/user/login",
                                                         data=login_data_another_user)

        auth_sid_another_user = self.get_cookie(response_login_data_another_user, "auth_sid")
        token_another_user = self.get_header(response_login_data_another_user, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response = MyRequests.put(
            f"/user/{user_id}",
            headers={'x-csrf-token': token_another_user},
            cookies={'auth_sid': auth_sid_another_user},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 200)

        # GET (user)
        response_get_user = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token_user},
            cookies={"auth_sid": auth_sid_user},
        )

        Assertions.assert_json_value_by_name(
            response_get_user,
            "firstName",
            first_name_user,
            "Wrong name of the user after edit by another user"
        )

    @allure.description("This test edit of email by incorrect value")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("negative_case")
    def test_edit_user_with_incorrect_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response_register_data = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_register_data, 200)
        Assertions.assert_json_has_key(response_register_data, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response_register_data, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response_login_data = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login_data, "auth_sid")
        token = self.get_header(response_login_data, "x-csrf-token")

        # EDIT
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        new_email = f"{base_part}{random_part}{domain}"
        response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response, 400)
        assert response.text == 'Invalid email format', "Unexpected response text for invalid email"

        # GET
        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response_get,
            "email",
            email,
            "Wrong email after edit"
        )

    @allure.description("This test edit of name by incorrect short value")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("negative_case")
    def test_edit_user_with_short_username(self) :
        # REGISTER
        register_data = self.prepare_registration_data()

        response_register_data = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_register_data, 200)
        Assertions.assert_json_has_key(response_register_data, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response_register_data, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response_login_data = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login_data, "auth_sid")
        token = self.get_header(response_login_data, "x-csrf-token")

        # EDIT
        new_firstName = ''.join(list(map(chr, [random.randint(98, 122) for i in range(1)])))

        response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_firstName}
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "Too short value for field firstName",
            "Unexpected value for short name"
        )

        # GET
        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response_get,
            "firstName",
            first_name,
            "Wrong email of the user after edit"
        )