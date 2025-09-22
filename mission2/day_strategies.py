from abc import ABC, abstractmethod

class AttendanceStrategy(ABC):
    def __init__(self, day_info):
        self.day_info = day_info

    @abstractmethod
    def execute(self, user_id, system):
        pass


class SimpleDayStrategy(AttendanceStrategy):
    def execute(self, user_id, system):
        index = self.day_info["index"]
        add_point = self.day_info["add_point"]
        system.attendance_by_day[user_id][index] += 1
        system.points[user_id] += add_point

class WednesdayStrategy(AttendanceStrategy):
    def execute(self, user_id, system):
        index = self.day_info["index"]
        add_point = self.day_info["add_point"]
        system.attendance_by_day[user_id][index] += 1
        system.points[user_id] += add_point
        system.wednesday_attendance_count[user_id] += 1

class WeekendStrategy(AttendanceStrategy):
    def execute(self, user_id, system):
        index = self.day_info["index"]
        add_point = self.day_info["add_point"]
        system.attendance_by_day[user_id][index] += 1
        system.points[user_id] += add_point
        system.weekend_attendance_count[user_id] += 1