from day_factory import DayStrategyFactory, InvalidDataError
from grading_factory import GradingStrategyFactory
from bonus_factory import BonusStrategyFactory
from enum import Enum

class Grade(Enum):
    NORMAL = 0
    SILVER = 2
    GOLD = 1

class AttendanceSystem:
    # 상수 정의
    MAX_USERS = 100
    NUM_DAYS = 7


    def __init__(self):
        self.user_name_to_id = {}
        self.user_id_cnt = 0
        self.attendance_by_day = [[0] * self.NUM_DAYS for _ in range(self.MAX_USERS)]
        self.points = [0] * self.MAX_USERS
        self.grade = [0] * self.MAX_USERS
        self.names = [''] * self.MAX_USERS
        self.wednesday_attendance_count = [0] * self.MAX_USERS
        self.weekend_attendance_count = [0] * self.MAX_USERS
        self.day_factory = DayStrategyFactory()
        self.grading_factory = GradingStrategyFactory()
        self.bonus_factory = BonusStrategyFactory()

    def get_or_create_user_id(self, user_name):
        if user_name not in self.user_name_to_id:
            self.user_id_cnt += 1
            self.user_name_to_id[user_name] = self.user_id_cnt
            self.names[self.user_id_cnt] = user_name
        return self.user_name_to_id[user_name]

    def record_attendance(self, user_name, day_of_week):
        user_id = self.get_or_create_user_id(user_name)
        try:
            strategy = self.day_factory.get_strategy(day_of_week)
            strategy.execute(user_id, self)  # day_of_week 인자 제거
        except InvalidDataError as e:
            print(f"경고: {e}")


    def calculate_bonus_points(self, user_id):
        self.bonus_factory.get_strategy().calculate(user_id, self)

    def determine_grade(self, user_id):
        self.grading_factory.get_strategy(self.points[user_id]).determine(user_id, self)

    def print_user_summary(self, user_id):
        self.grading_factory.get_strategy(self.points[user_id]).print_summary(user_id, self)

    def print_removed_players(self):
        print("\nRemoved player")
        print("==============")
        for i in range(1, self.user_id_cnt + 1):
            if self.grade[i] not in (Grade.GOLD.value, Grade.SILVER.value) and \
                    self.wednesday_attendance_count[i] == 0 and \
                    self.weekend_attendance_count[i] == 0:
                print(self.names[i])

    def process_line(self, line):
        try:
            parts = line.strip().split()
            if len(parts) != 2:
                raise InvalidDataError(f"잘못된 형식의 데이터: '{line.strip()}'")
            user_name, day_of_week = parts
            self.record_attendance(user_name, day_of_week)

        except InvalidDataError as e:
            print(f"경고: {e}")
        except IndexError:
            pass
        except Exception as e:
            print(f"예상치 못한 오류 발생: {e}")

    def run(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    self.process_line(line)

            for i in range(1, self.user_id_cnt + 1):
                self.calculate_bonus_points(i)
                self.determine_grade(i)
                self.print_user_summary(i)

            self.print_removed_players()

        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {file_path}")


if __name__ == "__main__":
    attendance_system = AttendanceSystem()
    attendance_system.run("attendance_weekday_500.txt")