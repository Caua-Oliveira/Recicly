class UserStatistics:
    def __init__(self):
        self.total_trash_amount = 0
        self.trash_by_type = {
            'plastic': 0,
            'metal': 0,
            'paper': 0,
            'glass': 0,
            'organic': 0
        }
        self.all_time_points = 0
        self.current_points = 0
        self.points_traded = 0
        self.number_of_trades = 0

    def add_trash(self, trash_type, amount):
        self.trash_by_type[trash_type] += amount
        self.total_trash_amount += amount

    def add_points(self, num):
        self.all_time_points += num
        self.current_points += num

    def remove_points(self, num):
        if num <= self.current_points:
            self.current_points -= num
            self.points_traded += num
            self.number_of_trades += 1
            return True
