from locust import HttpUser, between, task


class MyUser(HttpUser):
    wait_time = between(1, 2)
    SessionToken = ""
    Otp = ""

    def on_start(self):
        register_response = self.client.post(
            "/api/v1/user/register", json={"name": "name",
                                           "phone_number": "08393393834",
                                           "email": "1234567@gmail.com",
                                           "password": "password",
                                           "business_name": "pet shop",
                                           "business_type": 1,
                                           "city_code": 1})
        self.Otp = register_response.json().get("data").get("otp")
        print(register_response.json())

    @task(1)
    def user_verification(self):
        verification_response = self.client.post(
            "/api/v1/user/register/verification_code", json={"email": "1234567@gmail.com", "otp": self.Otp})
        print(verification_response.json())

    @task(2)
    def user_login(self):
        login_response = self.client.post(
            "/api/v1/user/login", json={"email": "1234567@gmail.com", "password": "password", "force_login": 1})
        print(login_response.json().get("data").get("access_token"))
        self.SessionToken = login_response.json().get("data").get("access_token")

    @task(3)
    def user_info_auth(self):
        get_user_response = self.client.get(
            "/api/v1/user",  headers={"Authorization": "Bearer " + self.SessionToken})
        print(get_user_response.json().get("data").get("majoo_merchant_id"))
