from code.database_connection import *

class Collection_Location:
    def __init__(self, name, address, contact, coordinates):
        self.login_id = None
        self.login_password = None
        self.name = name
        self.address = address
        self.contact = contact
        self.coordinates = coordinates
        self.statistics = {
            'total_trash_received': 0,
            'total_trash_received_by_type': {
                'plastic': 0,
                'metal': 0,
                'paper': 0,
                'glass': 0,
                'organic': 0
            },
        }
        self.point_values = {
            'plastic': 1000,
            'metal': 1500,
            'paper': 800,
            'glass': 1200,
            'organic': 500
        }

    def calculate_points(self, trash_amount, trash_type):
        points_per_kg = self.point_values[trash_type]
        total_points = trash_amount * points_per_kg
        return total_points

    def deliver_trash(self):
        try:
            user_obj = fetch_user_by_email(input("User email: "))
            trash_amount = float(input("Enter the amount of trash delivered (kg): "))
            trash_type = input("Enter the type of trash (plastic/metal/paper/glass/organic): ").lower()
            if trash_type in self.statistics['total_trash_received_by_type']:
                self.statistics['total_trash_received'] += trash_amount
                self.statistics['total_trash_received_by_type'][trash_type] += trash_amount
                user_obj.statistics.add_trash(trash_type, trash_amount)
                points_earned = self.calculate_points(trash_amount, trash_type)
                user_obj.statistics.add_points(points_earned)
                print(f"Trash delivered successfully! You earned {points_earned} points.")
            else:
                print("Invalid trash type.")
        except ValueError:
            print("Invalid amount entered.")


