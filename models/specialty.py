class Specialty:
    def __init__(self, specialty_id, name, description=""):
        self.specialty_id = specialty_id
        self.name = name
        self.description = description

    def __str__(self):
        return self.name 