"""
A-D Event Data Model
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ADEvent:
    """A-Dイベントを表すデータクラス"""

    event_type: str  # "A", "B", "C", "D"
    topic_id: str
    message_text: str
    message_url: str
    timestamp: datetime
    confidence: float  # 0.0 - 1.0
    note: Optional[str] = None

    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            "event_type": self.event_type,
            "topic_id": self.topic_id,
            "message_text": self.message_text,
            "message_url": self.message_url,
            "timestamp": self.timestamp.isoformat(),
            "confidence": self.confidence,
            "note": self.note,
        }
