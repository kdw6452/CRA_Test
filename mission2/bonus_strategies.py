from abc import ABC, abstractmethod

WEDNESDAY_INDEX = 2
SATURDAY_INDEX = 5
SUNDAY_INDEX = 6
BONUS_ATTENDANCE_COUNT = 10
BONUS_POINTS = 10

class BonusStrategy(ABC):
    @abstractmethod
    def calculate(self, user_id, system):
        pass

class WednesdayBonusStrategy(BonusStrategy):
    def calculate(self, user_id, system):
        if system.attendance_by_day[user_id][WEDNESDAY_INDEX] >= BONUS_ATTENDANCE_COUNT:
            system.points[user_id] += BONUS_POINTS


class WeekendBonusStrategy(BonusStrategy):
    def calculate(self, user_id, system):
        if (system.attendance_by_day[user_id][SATURDAY_INDEX] +
                system.attendance_by_day[user_id][SUNDAY_INDEX]) >= BONUS_ATTENDANCE_COUNT:
            system.points[user_id] += BONUS_POINTS


class AllBonusStrategy(BonusStrategy):
    def calculate(self, user_id, system):
        WednesdayBonusStrategy().calculate(user_id, system)
        WeekendBonusStrategy().calculate(user_id, system)