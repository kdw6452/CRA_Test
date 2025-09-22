from bonus_strategies import AllBonusStrategy

class BonusStrategyFactory:
    def get_strategy(self):
        return AllBonusStrategy()