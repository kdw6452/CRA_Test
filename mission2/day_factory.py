from day_strategies import SimpleDayStrategy, WednesdayStrategy, WeekendStrategy

class InvalidDataError(Exception):
    """유효하지 않은 입력 데이터에 대한 커스텀 예외"""
    pass

class DayStrategyFactory:
    DAY_INFO = {
        "monday": {"index": 0, "add_point": 1},
        "tuesday": {"index": 1, "add_point": 1},
        "wednesday": {"index": 2, "add_point": 3, "is_wednesday": True},
        "thursday": {"index": 3, "add_point": 1},
        "friday": {"index": 4, "add_point": 1},
        "saturday": {"index": 5, "add_point": 2, "is_weekend": True},
        "sunday": {"index": 6, "add_point": 2, "is_weekend": True},
    }

    def get_strategy(self, day_of_week):
        info = self.DAY_INFO.get(day_of_week)
        if not info:
            raise InvalidDataError(f"알 수 없는 요일: '{day_of_week}'")

        if info.get("is_wednesday"):
            return WednesdayStrategy(info)
        elif info.get("is_weekend"):
            return WeekendStrategy(info)
        else:
            return SimpleDayStrategy(info)