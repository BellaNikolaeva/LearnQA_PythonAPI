from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserDelete(BaseCase):

    def test_delete_user_with_id2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response, 'auth_sid')
        token = self.get_header(response, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response, 'user_id')

        response2 = MyRequests.delete(
            f"/user/{user_id_from_auth_method}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_code_status(response2, 400)

        assert response2.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response for deletion user with ID 1, 2, 3, 4 or 5."

        response3 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        expected_fields = ["username", "firstName", "lastName", "email"]

        Assertions.assert_json_has_keys(response3, expected_fields)

    def test_delete_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response_register_data = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_register_data, 200)
        Assertions.assert_json_has_key(response_register_data, "id")

        email = register_data['email']
        password = register_data['password']
        first_name = register_data['firstName']
        user_id = self.get_json_value(response_register_data, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response_login_data = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login_data, "auth_sid")
        token = self.get_header(response_login_data, "x-csrf-token")

        # DELETE
        response_delete = MyRequests.delete(
            f"/user/{user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_code_status(response_delete, 200)

        # GET
        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response_get, 404)

        assert response_get.text == "User not found", f"Unexpected response for getting deleted user"

    def test_delete_user_from_another_user(self):
        # REGISTER (user)
        register_data_user = self.prepare_registration_data()

        response_register_data_user = MyRequests.post("/user/", data=register_data_user)

        Assertions.assert_code_status(response_register_data_user, 200)
        Assertions.assert_json_has_key(response_register_data_user, "id")

        email_user = register_data_user['email']
        password_user = register_data_user['password']
        first_name_user = register_data_user['firstName']
        last_name_user = register_data_user['lastName']
        user_id = self.get_json_value(response_register_data_user, "id")

        # REGISTER (another user)
        register_data_another_user = self.prepare_registration_data()

        response_register_data_another_user = MyRequests.post("/user/", data=register_data_another_user)

        Assertions.assert_code_status(response_register_data_another_user, 200)
        Assertions.assert_json_has_key(response_register_data_another_user, "id")

        email_another_user = register_data_another_user['email']
        password_another_user = register_data_another_user['password']
        first_name_another_user = register_data_another_user['firstName']
        another_user_id = self.get_json_value(response_register_data_another_user, "id")

        # LOGIN (user)
        login_data_user = {'email': email_user, 'password': password_user}

        response_login_data_user = MyRequests.post("/user/login", data=login_data_user)

        user_auth_sid = self.get_cookie(response_login_data_user, "auth_sid")
        user_token = self.get_header(response_login_data_user, "x-csrf-token")

        # LOGIN (another_user)
        login_data_another_user = {'email': email_another_user, 'password': password_another_user}

        response_login_data_another_user = MyRequests.post("/user/login", data=login_data_another_user)

        another_user_auth_sid = self.get_cookie(response_login_data_another_user, "auth_sid")
        another_user_token = self.get_header(response_login_data_another_user, "x-csrf-token")

        # DELETE
        response_delete = MyRequests.delete(
            f"/user/{user_id}",
            headers={'x-csrf-token': another_user_token},
            cookies={'auth_sid': another_user_auth_sid}
        )

        Assertions.assert_code_status(response_delete, 200)

        # GET (user)
        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": user_token},
            cookies={"auth_sid": user_auth_sid},
        )

        Assertions.assert_code_status(response_get, 200)
        Assertions.assert_json_value_by_name(
            response_get,
            "firstName",
            first_name_user,
            "Wrong firstName of the user 1 after delete by another user"
        )

        Assertions.assert_json_value_by_name(
            response_get,
            "lastName",
            last_name_user,
            "Wrong lastName of the user 1 after delete by another user"
        )

        Assertions.assert_json_value_by_name(
            response_get,
            "email",
            email_user,
            "Wrong email of the user 1 after delete by another user"
        )