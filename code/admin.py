import bcrypt

class Admin:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password)

    def add_store(self, store_list, store):
        store_list.append(store)

    def remove_store(self, store_list, store_name):
        for store in store_list:
            if store.name == store_name:
                store_list.remove(store)
                break

    def add_collection_location_credentials(self, collection_location, login_id, login_password):
        collection_location.login_id = login_id
        collection_location.login_password = login_password

    def __str__(self):
        return f"Admin: {self.name}, Email: {self.email}"
