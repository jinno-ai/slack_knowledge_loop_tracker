"""
A-D Event Extractor

SlackメッセージからA-Dイベントを抽出するクラス。
"""

from datetime import datetime
from typing import List, Optional

from src.event import ADEvent
from src.pattern_matcher import PatternMatcher
from src.confidence_calculator import ConfidenceCalculator
from src.topic_id_generator import TopicIdGenerator


class EventExtractor:
    """
    SlackメッセージからA-Dイベントを抽出するクラス

    抽出ルール:
    - A: 未知・不確実性・懸念・仮説が「新規に言語化された」状態
    - B: 未知を潰すための観測（テスト/計測/確認）に変換された状態
    - C: 観測により仮説が「潰れた/強まった/否定された」状態
    - D: 次回も回る形になった状態（自動化・テンプレ化）
    """

    def __init__(self):
        """初期化"""
        self.pattern_matcher = PatternMatcher()
        self.confidence_calculator = ConfidenceCalculator()
        self.topic_id_generator = TopicIdGenerator()

    def extract(
        self, messages: List[dict], existing_topics: Optional[List[str]] = None
    ) -> List[ADEvent]:
        """
        メッセージリストからA-Dイベントを抽出

        Args:
            messages: メッセージ辞書のリスト
                     各辞書は "text", "url", "timestamp" キーを持つ
            existing_topics: 既存のトピックIDリスト

        Returns:
            ADEventオブジェクトのリスト
        """
        if existing_topics is None:
            existing_topics = []

        events = []
        for message in messages:
            event = self._extract_single(message, existing_topics)
            if event:
                events.append(event)

        return events

    def _extract_single(
        self, message: dict, existing_topics: List[str]
    ) -> ADEvent | None:
        """
        単一のメッセージからA-Dイベントを抽出

        Args:
            message: メッセージ辞書
            existing_topics: 既存のトピックIDリスト

        Returns:
            ADEventオブジェクト。イベントが見つからない場合はNone。
        """
        message_text = message.get("text", "")
        message_url = message.get("url", "")
        timestamp = message.get("timestamp", datetime.now())

        event_type = self.pattern_matcher.match(message_text)
        if not event_type:
            return None

        topic_id = self.topic_id_generator.generate(
            message_text, existing_topics
        )
        confidence = self.confidence_calculator.calculate(
            message_text, event_type
        )

        return ADEvent(
            event_type=event_type,
            topic_id=topic_id,
            message_text=message_text,
            message_url=message_url,
            timestamp=timestamp,
            confidence=confidence,
        )
