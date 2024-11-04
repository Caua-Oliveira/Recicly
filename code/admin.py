import bcrypt

class Admin:
    def __init__(self, code, password):
        self.code = code
        self.password = password

    def add_collection_location_credentials(self, collection_location, login_id, login_password):
        collection_location.login_id = login_id
        collection_location.login_password = login_password

