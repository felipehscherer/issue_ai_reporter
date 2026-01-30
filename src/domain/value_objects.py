from enum import Enum


class CardType(str, Enum):
    STORY = "story"
    BUG = "bug"
    TASK = "task"
    EPIC = "epic"


class ReportType(str, Enum):
    QA = "qa"
    RISKS = "risks"
    TEST_STRATEGY = "test_strategy"
