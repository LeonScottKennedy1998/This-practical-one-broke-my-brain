from user import User
class Customer(User):
    def __init__(self, username, password, customer_id):
        super().__init__(username, password)
        self.customer_id = customer_id


