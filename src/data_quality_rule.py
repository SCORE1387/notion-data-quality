from enum import Enum


class IssueTypeSeverity(Enum):
    RED = 1         # Critical
    YELLOW = 2      # Warning
    BLUE = 3        # Info
    GREEN = 4       # OK


class DataQualityRule:
    def __init__(self, name: str, description: str, dashboard_link: str,
                 severity: IssueTypeSeverity, evaluate_function: callable):
        self.name = name
        self.description = description
        self.dashboard_link = dashboard_link
        self.severity = severity
        self.evaluate_function = evaluate_function

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()