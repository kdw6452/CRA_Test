
user_name_to_id = {}
user_id_cnt = 0

MAX_USERS = 100
NUM_DAYS = 7  # 7개의 요일 (월, 화, 수, 목, 금, 토, 일)
attendance_by_day = [[0] * NUM_DAYS for _ in range(MAX_USERS)]

points = [0] * MAX_USERS
grade = [0] * MAX_USERS
names = [''] * MAX_USERS
wednesday_attendance_count = [0] * MAX_USERS
weekend_attendance_count = [0] * MAX_USERS

WEDNESDAY_INDEX = 2
SATURDAY_INDEX = 5
SUNDAY_INDEX = 6
BONUS_ATTENDANCE_COUNT = 10
BONUS_POINTS = 10

GOLD_GRADE_POINT = 50
SILVER_GRADE_POINT = 30

DAILY_POINT = 1
WEDNESDAY_POINT = 3
WEEKEND_POINT = 2

from enum import Enum

class Grade(Enum):
    NORMAL = 0
    SILVER = 2
    GOLD = 1

def get_or_create_user_id(user_name):
    global user_id_cnt

    if user_name not in user_name_to_id:
        user_id_cnt += 1
        user_name_to_id[user_name] = user_id_cnt
        names[user_id_cnt] = user_name

    return user_name_to_id[user_name]


def print_removed_players(user_id_cnt, grade, names, wed, weekend):
    print("\nRemoved player")
    print("==============")

    for i in range(1, user_id_cnt + 1):
        if grade[i] not in (Grade.GOLD.value, Grade.SILVER.value) and wed[i] == 0 and weekend[i] == 0:
            print(names[i])

def update_user_attendance(user_name, day_of_week):
    DAY_INFO = {
        "monday": {"index": 0, "add_point": DAILY_POINT},
        "tuesday": {"index": 1, "add_point": DAILY_POINT},
        "wednesday": {"index": 2, "add_point": WEDNESDAY_POINT, "is_wednesday": True},
        "thursday": {"index": 3, "add_point": DAILY_POINT},
        "friday": {"index": 4, "add_point": DAILY_POINT},
        "saturday": {"index": 5, "add_point": WEEKEND_POINT, "is_weekend": True},
        "sunday": {"index": 6, "add_point": WEEKEND_POINT, "is_weekend": True},
    }

    try:
        if day_of_week not in DAY_INFO:
            raise Exception

        user_id = get_or_create_user_id(user_name)
        info = DAY_INFO[day_of_week]
        add_point = info["add_point"]
        index = info["index"]

        attendance_by_day[user_id][index] += 1
        points[user_id] += add_point

        if info.get("is_wednesday"):
            wednesday_attendance_count[user_id] += 1
        if info.get("is_weekend"):
            weekend_attendance_count[user_id] += 1

    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")


def calculate_bonus_points(user_id):
    if attendance_by_day[user_id][WEDNESDAY_INDEX] > BONUS_ATTENDANCE_COUNT - 1:
        points[user_id] += BONUS_ATTENDANCE_COUNT
    if attendance_by_day[user_id][SATURDAY_INDEX] + attendance_by_day[user_id][SUNDAY_INDEX] > BONUS_ATTENDANCE_COUNT - 1:
        points[user_id] += BONUS_ATTENDANCE_COUNT

def determine_grade(user_id):
    if points[user_id] >= GOLD_GRADE_POINT:
        grade[user_id] = Grade.GOLD.value
    elif points[user_id] >= SILVER_GRADE_POINT:
        grade[user_id] = Grade.SILVER.value
    else:
        grade[user_id] = Grade.NORMAL.value

def print_user_summary(user_id):
    grade_map = {
        Grade.GOLD.value: "GOLD",
        Grade.SILVER.value: "SILVER",
        Grade.NORMAL.value: "NORMAL"
    }
    grade_text = grade_map.get(grade[user_id], "NORMAL")
    print(f"NAME : {names[user_id]}, POINT : {points[user_id]}, GRADE : {grade_text}")

def process_line(line):
    try:
        parts = line.strip().split()
        if len(parts) != 2:
            raise Exception
        user_name, day_of_week = parts
        update_user_attendance(user_name, day_of_week)
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")

def input_file():
    try:
        file_path = "attendance_weekday_500.txt"
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                process_line(line)
        for i in range(1, user_id_cnt + 1):
            calculate_bonus_points(i)
            determine_grade(i)
            print_user_summary(i)

        print_removed_players(user_id_cnt, grade, names, wednesday_attendance_count, weekend_attendance_count)

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    input_file()
