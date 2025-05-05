import Doctor

class Oncologist(Doctor):
    def __init__(self, first_name, last_name, experience):
        super().__init__(first_name, last_name, "Oncology")
        self.experience = experience

    def display_info(self):
        super().display_info()
        print(f"Years of Experience: {self.experience}")