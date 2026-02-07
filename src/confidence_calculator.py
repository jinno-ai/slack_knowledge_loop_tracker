"""
Confidence Calculator for A-D Events
"""

import re
from src.constants import EVENT_PATTERNS


class ConfidenceCalculator:
    """イベントの信頼度を算出するクラス"""

    def calculate(self, message_text: str, event_type: str) -> float:
        """
        イベントの信頼度を算出

        Args:
            message_text: メッセージテキスト
            event_type: イベントタイプ

        Returns:
            信頼度（0.0 - 1.0）
        """
        confidence = 0.5

        # 明示的なタグ（[A], [B]等）があれば信頼度を高く
        explicit_tags = [rf"\[{event_type}\]", rf"【{event_type}】"]
        for tag in explicit_tags:
            if re.search(tag, message_text):
                confidence = 0.9
                break

        # 文脈キーワードの数で信頼度を調整
        keyword_count = sum(
            1
            for pattern in EVENT_PATTERNS[event_type]
            if re.search(pattern, message_text)
        )
        confidence += min(keyword_count * 0.05, 0.3)

        return min(confidence, 1.0)
