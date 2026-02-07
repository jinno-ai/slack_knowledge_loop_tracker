"""
Pattern Matcher for A-D Events
"""

import re
from src.constants import EVENT_PATTERNS


class PatternMatcher:
    """A-Dイベントのパターンマッチを行うクラス"""

    def __init__(self):
        """初期化"""
        self.patterns = {
            event_type: [re.compile(pattern) for pattern in patterns]
            for event_type, patterns in EVENT_PATTERNS.items()
        }

    def match(self, message_text: str) -> str | None:
        """
        メッセージからマッチするイベントタイプを返す

        Args:
            message_text: メッセージテキスト

        Returns:
            マッチしたイベントタイプ ("A", "B", "C", "D")。マッチしない場合はNone。
        """
        for event_type, patterns in self.patterns.items():
            for pattern in patterns:
                if pattern.search(message_text):
                    return event_type
        return None
