from code.user_statistics import UserStatistics
import bcrypt
from code.database_connection import *
import pandas as pd

class User:
    def __init__(self, name, email, password, id=None, is_active=True, statistics=UserStatistics()):
        self.name = name
        self.email = email
        self.id = id
        self.password = self.hash_password(password) if isinstance(password, str) else password
        self.is_active = is_active
        self.statistics = statistics

    def show_statistics(self):
        # Trash statistics data
        trash_data = {
            "Metric": [
                "Total de lixo entregue (kg)",
                "Plastic (kg)",
                "Metal (kg)",
                "Paper (kg)",
                "Glass (kg)",
                "Organic (kg)"
            ],
            "Value": [
                self.statistics.total_trash_amount,
                self.statistics.trash_by_type['plastic'],
                self.statistics.trash_by_type['metal'],
                self.statistics.trash_by_type['paper'],
                self.statistics.trash_by_type['glass'],
                self.statistics.trash_by_type['organic']
            ]
        }

        points_data = {
            "Metric": [
                "Pontos disponíveis",
                "Pontos acumulados",
                "Pontos trocados",
                "Número de trocas"
            ],
            "Value": [
                self.statistics.current_points,
                self.statistics.all_time_points,
                self.statistics.points_traded,
                self.statistics.number_of_trades
            ]
        }

        # Convert dictionaries to DataFrames
        trash_df = pd.DataFrame(trash_data)
        points_df = pd.DataFrame(points_data)

        print("Trash Statistics:")
        print(trash_df)
        print("\nPoints Statistics:")
        print(points_df)

    @staticmethod
    def hash_password(password):
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def verify_password(self, password):
        # Check if the provided password matches the stored hash
        stored_password = self.password.encode('utf-8') if isinstance(self.password, str) else self.password
        return bcrypt.checkpw(password.encode('utf-8'), stored_password)

    def deactivate_account(self):
        self.is_active = False
        update_user_in_db(self)

    def reactivate_account(self):
        self.is_active = True
        update_user_in_db(self)

    def update_email(self, new_email):
        self.email = new_email
        update_user_in_db(self)

    def update_password(self, new_password):
        self.password = self.hash_password(new_password)
        update_user_in_db(self)

    def to_dict(self):
        return {
        'name': self.name.title(),
        'email': self.email,
        'points': self.statistics.current_points,
        'total_trash_amount': self.statistics.total_trash_amount,
        'trash_by_type': {
            'plastic': self.statistics.trash_by_type.get('plastic', 0),
            'metal': self.statistics.trash_by_type.get('metal', 0),
            'paper': self.statistics.trash_by_type.get('paper', 0),
            'glass': self.statistics.trash_by_type.get('glass', 0),
            'organic': self.statistics.trash_by_type.get('organic', 0)
        },
        'all_time_points': self.statistics.all_time_points,
        'current_points': self.statistics.current_points,
        'points_traded': self.statistics.points_traded,
        'number_of_trades': self.statistics.number_of_trades
    }


