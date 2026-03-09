import enum


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    COMMITTED = "committed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ReferenceType(str, enum.Enum):
    JIRA_EPIC = "jira_epic"
    DOD = "dod"


class TagLevel(str, enum.Enum):
    STRATEGIC_OBJECTIVE = "SO"
    PORTFOLIO_EPIC = "PE"
    BUSINESS_OBJECTIVE = "BO"
    FEATURE = "FE"
