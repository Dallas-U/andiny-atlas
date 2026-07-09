"""
Common type aliases used throughout the application.
"""

from typing import Any

JSONDict = dict[str, Any]
CaseRecord = JSONDict
CaseCollection = list[CaseRecord]
