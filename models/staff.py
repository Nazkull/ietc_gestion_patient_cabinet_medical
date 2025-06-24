from models.user import User

class Staff(User):
    def __init__(self, user_id, first_name, last_name, email, phone, password, staff_id):
        super().__init__(user_id, first_name, last_name, email, phone, password)
        self.staff_id = staff_id

    def __str__(self):
        return f"Staff: {self.first_name} {self.last_name}" 