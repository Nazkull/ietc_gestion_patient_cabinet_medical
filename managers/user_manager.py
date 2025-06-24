from managers.storage_manager import StorageManager
from models.patient import Patient
# We will add other roles like Doctor and Secretary later
import uuid
import re

class UserManager:
    def __init__(self, storage_manager):
        self.storage_manager = storage_manager
        self.users_file = 'users.json'
        self.users = self._load_users()

    def _load_users(self):
        """Loads users from the JSON file."""
        return self.storage_manager.load_data(self.users_file)

    def _save_users(self):
        """Saves the current list of users to the JSON file."""
        self.storage_manager.save_data(self.users_file, self.users)

    def _validate_email(self, email):
        """Validates email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _validate_phone(self, phone):
        """Validates phone number format."""
        # Remove spaces and special characters
        clean_phone = re.sub(r'[^\d]', '', phone)
        return len(clean_phone) >= 10

    def _validate_ssn(self, ssn):
        """Validates social security number format."""
        # Remove spaces and special characters
        clean_ssn = re.sub(r'[^\d]', '', ssn)
        return len(clean_ssn) >= 10

    def find_user_by_email(self, email):
        """Finds a user by their email address."""
        for user in self.users:
            if user['email'] == email:
                return user
        return None

    def find_user_by_id(self, user_id):
        """Finds a user by their user ID."""
        for user in self.users:
            if user.get('user_id') == user_id:
                return user
        return None

    def find_user_by_patient_id(self, patient_id):
        """Finds a patient by their patient ID."""
        for user in self.users:
            if user.get('patient_id') == patient_id:
                return user
        return None

    def find_user_by_doctor_id(self, doctor_id):
        """Finds a doctor by their doctor ID."""
        for user in self.users:
            if user.get('doctor_id') == doctor_id:
                return user
        return None

    def find_user_by_role_id(self, role_id):
        """Finds a user by any role ID (patient_id, doctor_id, secretary_id)."""
        for user in self.users:
            if (user.get('patient_id') == role_id or 
                user.get('doctor_id') == role_id or 
                user.get('secretary_id') == role_id):
                return user
        return None

    def get_user(self, user_id):
        """Gets a user by their ID (alias for find_user_by_id)."""
        return self.find_user_by_id(user_id)

    def update_user(self, email, updated_data):
        """Updates a user's information by email."""
        for i, user in enumerate(self.users):
            if user.get('email') == email:
                self.users[i].update(updated_data)
                self._save_users()
                return True
        return False

    def get_next_user_id(self):
        """Generates a new unique user ID."""
        # This is a simple way to generate IDs. For a real application,
        # a more robust method like UUIDs would be better.
        if not self.users:
            return 1
        return max(user['user_id'] for user in self.users) + 1

    def register_patient(self, first_name, last_name, email, phone, password, date_of_birth, ssn):
        """Registers a new patient and saves them to the file."""
        # Validation
        if not self._validate_email(email):
            print("Error: Invalid email format.")
            return None
            
        if not self._validate_phone(phone):
            print("Error: Invalid phone number format.")
            return None
            
        if not self._validate_ssn(ssn):
            print("Error: Invalid social security number format.")
            return None

        if self.find_user_by_email(email):
            print("Error: A user with this email already exists.")
            return None

        user_id = self.get_next_user_id()
        patient_id = f"PAT-{user_id}" # Example of a specific role ID

        new_patient = {
            "user_id": user_id,
            "patient_id": patient_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "password": password, # Plain text password
            "date_of_birth": date_of_birth,
            "social_security_number": ssn,
            "role": "Patient"
        }
        self.users.append(new_patient)
        self._save_users()
        print("Registration successful!")
        return new_patient

    def register_secretary(self, first_name, last_name, email, phone, password):
        """Registers a new secretary and saves them to the file."""
        # Validation
        if not self._validate_email(email):
            print("Error: Invalid email format.")
            return None
            
        if not self._validate_phone(phone):
            print("Error: Invalid phone number format.")
            return None

        if self.find_user_by_email(email):
            print("Error: A user with this email already exists.")
            return None

        user_id = self.get_next_user_id()
        staff_id = f"STAFF-{user_id}"
        secretary_id = f"SEC-{user_id}"

        new_secretary = {
            "user_id": user_id,
            "staff_id": staff_id,
            "secretary_id": secretary_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "password": password, # Plain text password
            "role": "Secretary"
        }
        self.users.append(new_secretary)
        self._save_users()
        print("Secretary registration successful!")
        return new_secretary

    def register_doctor(self, first_name, last_name, email, phone, password, specialty):
        """Registers a new doctor and saves them to the file."""
        # Validation
        if not self._validate_email(email):
            print("Error: Invalid email format.")
            return None
            
        if not self._validate_phone(phone):
            print("Error: Invalid phone number format.")
            return None

        if self.find_user_by_email(email):
            print("Error: A user with this email already exists.")
            return None

        user_id = self.get_next_user_id()
        staff_id = f"STAFF-{user_id}"
        doctor_id = f"DR-{user_id}"

        new_doctor = {
            "user_id": user_id,
            "staff_id": staff_id,
            "doctor_id": doctor_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "password": password,  # Plain text password
            "specialty": specialty,
            "role": "Doctor"
        }
        self.users.append(new_doctor)
        self._save_users()
        print("Doctor registration successful!")
        return new_doctor

    def login_user(self, email, password):
        """Logs a user in by checking their email and password."""
        self.users = self._load_users() # Reload users from file before login
        user = self.find_user_by_email(email)
        if user and user['password'] == password:  # Direct comparison
            # Do not print here, let the GUI handle messages
            return user
        return None

    def get_all_users(self):
        """Gets all users."""
        return self.users

    def delete_user(self, user_id):
        """Deletes a user by their user ID."""
        for i, user in enumerate(self.users):
            if user['user_id'] == user_id:
                del self.users[i]
                self._save_users()
                return True
        return False 