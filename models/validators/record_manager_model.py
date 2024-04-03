from enum import Enum


class CleanupMethod(str, Enum):
    incremental = "incremental"
    full = "full"
