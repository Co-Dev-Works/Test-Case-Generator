# models.py
from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class TestCase:
    id: int
    title: str
    steps: List[str]
    expected: str
    priority: str
    tags: List[str]
    sample_data: Optional[Dict] = None
