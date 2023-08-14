from src.data_quality_rule import DataQualityRule


class NotionCardDataQualityIssue:
    def __init__(self, data_quality_rule: DataQualityRule, notion_card):
        self.data_quality_rule = data_quality_rule
        self.notion_card = notion_card

    def __str__(self):
        return f"{self.notion_card['id']}: \"{self.data_quality_rule.name}\""

    def __repr__(self):
        return self.__str__()