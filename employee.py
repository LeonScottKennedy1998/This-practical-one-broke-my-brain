from user import User
class Employee(User):
    def __init__(self, username, password, employee_id):
        super().__init__(username, password)
        self.employee_id = employee_id

