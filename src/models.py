class Category:
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name
class Equipment:
    def __init__(self, equipment_id, category_id, name, description="", daily_rate=0.0, contact_phone="", email="", available=True):
        self.equipment_id = equipment_id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.daily_rate = daily_rate
        self.contact_phone = contact_phone
        self.email = email
        self.available = available

class Customer:
    def __init__(self, customer_id, last_name, first_name, contact_phone="", email=""):
        self.customer_id = customer_id
        self.last_name = last_name
        self.first_name = first_name
        self.contact_phone = contact_phone
        self.email = email

class Rental:
    def __init__(self, rental_id, date, customer_id, equipment_id, return_date=None, cost=0.0):
        self.rental_id = rental_id
        self.date = date
        self.customer_id = customer_id
        self.equipment_id = equipment_id
        self.return_date = return_date
        self.cost = cost
