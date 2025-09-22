from abc import ABC, abstractmethod
from enum import Enum

class Grade(Enum):
    NORMAL = 0
    SILVER = 2
    GOLD = 1

class GradingStrategy(ABC):
    @abstractmethod
    def determine(self, user_id, system):
        pass
    def print_summary(self, user_id, system):
        pass

class NormalGradingStrategy(GradingStrategy):
    def determine(self, user_id, system):
        system.grade[user_id] = Grade.NORMAL.value

    def print_summary(self, user_id, system):
        print(f"NAME : {system.names[user_id]}, POINT : {system.points[user_id]}, GRADE : NORMAL")


class SilverGradingStrategy(GradingStrategy):
    def determine(self, user_id, system):
        system.grade[user_id] = Grade.SILVER.value

    def print_summary(self, user_id, system):
        print(f"NAME : {system.names[user_id]}, POINT : {system.points[user_id]}, GRADE : SILVER")

class GoldGradingStrategy(GradingStrategy):
    def determine(self, user_id, system):
        system.grade[user_id] = Grade.GOLD.value

    def print_summary(self, user_id, system):
        print(f"NAME : {system.names[user_id]}, POINT : {system.points[user_id]}, GRADE : GOLD")