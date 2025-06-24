class User:
    def __init__(self, user_id, first_name, last_name, email, phone, password):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password

    def register(self):
        # à implémenter plus tard
        pass

    def login(self):
        # à implémenter plus tard
        pass

    def logout(self):
        # à implémenter plus tard
        pass

    def send_message(self):
        # à implémenter plus tard
        pass

    def read_messages(self):
        # à implémenter plus tard
        pass

    def __str__(self):
        return f"User: {self.first_name} {self.last_name}" 