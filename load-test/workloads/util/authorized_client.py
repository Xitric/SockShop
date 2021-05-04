import base64
from locust import HttpUser

class AuthorizedClient(HttpUser):
    abstract= True
    next_id = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        AuthorizedClient.next_id += 1
        self.name = f"client{AuthorizedClient.next_id}"

    def __login(self):
        auth_header_raw = f"{self.name}:password"
        auth_header_encoded = str(base64.b64encode(auth_header_raw.encode("utf-8")), "utf-8")

        login = self.client.get("/login", headers={
            "Authorization": f"Basic {auth_header_encoded}"
        })

        if login.status_code == 200:
            return False
        else:
            # Otherwise we must register a new account
            self.client.post("/register", json={
                "username": self.name,
                "password": "password",
                "email": f"{self.name}@ahsgvfaisvf.com",
                "firstName": self.name,
                "lastName": "testuser",
            })

            self.client.get("/login", headers={
                "Authorization": f"Basic {auth_header_encoded}"
            })

            return True

    def __update_address(self):
        self.client.post("/addresses", json={
            "number": "1",
            "street": "Street",
            "city": "City",
            "postcode": "1010",
            "country": "Country",
        })

    def __update_visa(self):
        self.client.post("/cards", json={
            "longNum": "1234567812345678",
            "expires": "01/16",
            "ccv": "123",
        })

    # Ensure that the client has registered and logged in to authorize further
    # requests
    def on_start(self):
        if self.__login():
            # Login resulted in creating a new account, so we should initialize
            # account info
            self.__update_address()
            self.__update_visa()
