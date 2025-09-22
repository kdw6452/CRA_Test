import pytest
from grading_strategies import NormalGradingStrategy, SilverGradingStrategy, GoldGradingStrategy
from attendance import AttendanceSystem, Grade, InvalidDataError
from bonus_strategies import BONUS_POINTS, BONUS_ATTENDANCE_COUNT
from grading_factory import GradingStrategyFactory, GOLD_GRADE_POINT, SILVER_GRADE_POINT

@pytest.fixture
def system():
    return AttendanceSystem()


# ... (기존 테스트 함수들) ...

def test_grading_factory_returns_correct_strategy(system):
    """
    GradingStrategyFactory가 포인트에 따라 올바른 전략을 반환하는지 테스트
    """
    factory = GradingStrategyFactory()

    # GOLD 등급
    strategy_gold = factory.get_strategy(GOLD_GRADE_POINT + 1)
    assert isinstance(strategy_gold, GoldGradingStrategy)

    # SILVER 등급
    strategy_silver = factory.get_strategy(SILVER_GRADE_POINT)
    assert isinstance(strategy_silver, SilverGradingStrategy)

    # NORMAL 등급
    strategy_normal = factory.get_strategy(SILVER_GRADE_POINT - 1)
    assert isinstance(strategy_normal, NormalGradingStrategy)


def test_grading_strategy_updates_grade(system):
    """
    각 등급 전략이 AttendanceSystem의 grade를 올바르게 업데이트하는지 테스트
    """
    user_name = "grade_user"
    user_id = system.get_or_create_user_id(user_name)

    # GOLD 전략 테스트
    gold_strategy = GoldGradingStrategy()
    gold_strategy.determine(user_id, system)
    assert system.grade[user_id] == Grade.GOLD.value

    # SILVER 전략 테스트
    silver_strategy = SilverGradingStrategy()
    silver_strategy.determine(user_id, system)
    assert system.grade[user_id] == Grade.SILVER.value

    # NORMAL 전략 테스트
    normal_strategy = NormalGradingStrategy()
    normal_strategy.determine(user_id, system)
    assert system.grade[user_id] == Grade.NORMAL.value


def test_determine_grade_with_factory(system):
    """
    AttendanceSystem의 determine_grade가 팩토리 패턴을 사용해 등급을 결정하는지 테스트
    """
    user_name = "factory_grade_user"
    user_id = system.get_or_create_user_id(user_name)

    # GOLD 등급
    system.points[user_id] = GOLD_GRADE_POINT + 10
    system.determine_grade(user_id)
    assert system.grade[user_id] == Grade.GOLD.value

    # SILVER 등급
    system.points[user_id] = SILVER_GRADE_POINT + 5
    system.determine_grade(user_id)
    assert system.grade[user_id] == Grade.SILVER.value

    # NORMAL 등급
    system.points[user_id] = SILVER_GRADE_POINT - 5
    system.determine_grade(user_id)
    assert system.grade[user_id] == Grade.NORMAL.value

def test_get_or_create_user_id_creates_new_user(system):
    assert system.user_id_cnt == 0
    user_name = "test_user1"
    user_id = system.get_or_create_user_id(user_name)

    assert user_id == 1
    assert system.names[1] == user_name
    assert system.user_name_to_id[user_name] == 1


def test_get_or_create_user_id_returns_existing_user_id(system):
    assert system.user_id_cnt == 0
    user_name = "test_user2"
    system.get_or_create_user_id(user_name)  # 사용자 생성

    user_id = system.get_or_create_user_id(user_name)  # 기존 사용자 ID 조회

    assert user_id == 1
    assert system.user_name_to_id[user_name] == 1


def test_record_attendance(system):
    user_name = "test_user3"
    assert system.user_id_cnt == 0

    system.record_attendance(user_name, "monday")
    system.record_attendance(user_name, "wednesday")
    system.record_attendance(user_name, "saturday")

    user_id = system.user_name_to_id[user_name]

    # DayStrategyFactory 인스턴스를 통해 DAY_INFO에 접근
    assert system.attendance_by_day[user_id][system.day_factory.DAY_INFO["monday"]["index"]] == 1
    assert system.attendance_by_day[user_id][system.day_factory.DAY_INFO["wednesday"]["index"]] == 1
    assert system.attendance_by_day[user_id][system.day_factory.DAY_INFO["saturday"]["index"]] == 1
    assert system.points[user_id] == 1 + 3 + 2
    assert system.wednesday_attendance_count[user_id] == 1
    assert system.weekend_attendance_count[user_id] == 1


def test_record_attendance_invalid_day(system, capsys):
    user_name = "invalid_day_user"

    # 테스트 전의 초기 상태를 기록
    initial_user_id_cnt = system.user_id_cnt

    system.process_line(f"{user_name} invalid_day")

    # capsys 픽스처를 사용하여 출력 캡처
    captured = capsys.readouterr()
    assert "경고: 알 수 없는 요일" in captured.out

    # get_or_create_user_id는 사용자를 생성하므로, user_id_cnt가 1 증가했는지 확인
    assert system.user_id_cnt == initial_user_id_cnt + 1

    # 생성된 사용자의 ID를 가져옴
    user_id = system.user_name_to_id[user_name]

    # 포인트가 증가하지 않았는지 확인
    assert system.points[user_id] == 0

    # 요일별 출석 횟수가 증가하지 않았는지 확인
    assert all(count == 0 for count in system.attendance_by_day[user_id])
    assert system.wednesday_attendance_count[user_id] == 0
    assert system.weekend_attendance_count[user_id] == 0


def test_process_line_with_invalid_data_format(system, capsys):
    """잘못된 형식의 데이터 처리 테스트"""
    invalid_line = "user_one two three"
    system.process_line(invalid_line)

    captured = capsys.readouterr()
    assert "경고: 잘못된 형식의 데이터" in captured.out


def test_calculate_bonus_points(system):
    """보너스 포인트 계산 테스트"""
    user_name = "bonus_user"
    user_id = system.get_or_create_user_id(user_name)

    system.points[user_id] = 0

    # 수요일 10회 출석
    for _ in range(10):
        system.record_attendance(user_name, "wednesday")

    # 주말 10회 출석 (토요일 5, 일요일 5)
    for _ in range(5):
        system.record_attendance(user_name, "saturday")
        system.record_attendance(user_name, "sunday")

    # 보너스 포인트 계산 전
    initial_points = system.points[user_id]

    system.calculate_bonus_points(user_id)

    # 예상 총점: (3 * 10) + (2 * 5) + (2 * 5) + (보너스10) + (보너스10)
    expected_points = initial_points + BONUS_POINTS * 2
    assert system.points[user_id] == expected_points


def test_determine_grade(system):
    user_name = "grade_user"
    user_id = system.get_or_create_user_id(user_name)

    # GOLD 등급
    system.points[user_id] = GOLD_GRADE_POINT + 10
    system.determine_grade(user_id)
    assert system.grade[user_id] == Grade.GOLD.value

    # SILVER 등급
    system.points[user_id] = SILVER_GRADE_POINT + 10
    system.determine_grade(user_id)
    assert system.grade[user_id] == Grade.SILVER.value

    # NORMAL 등급
    system.points[user_id] = SILVER_GRADE_POINT - 1
    system.determine_grade(user_id)
    assert system.grade[user_id] == Grade.NORMAL.value


# 파일 읽기를 위한 임시 파일 생성을 활용한 테스트
@pytest.fixture
def mock_file(tmp_path):
    """테스트용 가상 파일을 생성하는 픽스처"""
    file_content = """user1 monday
user1 monday
user2 wednesday
user3 friday
"""
    file_path = tmp_path / "test_attendance.txt"
    file_path.write_text(file_content)
    return file_path


def test_run_with_mock_file(system, mock_file):
    system.run(mock_file)

    user1_id = system.user_name_to_id["user1"]
    user2_id = system.user_name_to_id["user2"]
    user3_id = system.user_name_to_id["user3"]

    # user1: 월요일 2회 = 2점, 등급 NORMAL
    assert system.points[user1_id] == 2
    assert system.grade[user1_id] == Grade.NORMAL.value

    # user2: 수요일 1회 = 3점, 등급 NORMAL
    assert system.points[user2_id] == 3
    assert system.grade[user2_id] == Grade.NORMAL.value

    # user3: 금요일 1회 = 1점, 등급 NORMAL
    assert system.points[user3_id] == 1
    assert system.grade[user3_id] == Grade.NORMAL.value