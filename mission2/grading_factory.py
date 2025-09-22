from grading_strategies import NormalGradingStrategy, SilverGradingStrategy, GoldGradingStrategy


GOLD_GRADE_POINT = 50
SILVER_GRADE_POINT = 30

class GradingStrategyFactory:

    def get_strategy(self, user_points):
        if user_points >= GOLD_GRADE_POINT:
            return GoldGradingStrategy()
        elif user_points >= SILVER_GRADE_POINT:
            return SilverGradingStrategy()
        else:
            return NormalGradingStrategy()