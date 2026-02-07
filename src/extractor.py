"""
A-D Event Extractor

SlackメッセージからA-Dイベントを抽出するクラス。
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import re


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


class ADEventExtractor:
    """
    SlackメッセージからA-Dイベントを抽出するクラス

    抽出ルール:
    - A: 未知・不確実性・懸念・仮説が「新規に言語化された」状態
    - B: 未知を潰すための観測（テスト/計測/確認）に変換された状態
    - C: 観測により仮説が「潰れた/強まった/否定された」状態
    - D: 次回も回る形になった状態（自動化・テンプレ化）
    """

    # A-Dイベントを示すキーワードパターン
    PATTERNS = {
        "A": [
            r"不明", r"わからない", r"疑問", r"懸念",
            r"仮説", r"もしかして", r"気になる", r"不安",
            r"\?A\b", r"\[A\]", r"【A】"
        ],
        "B": [
            r"試しに", r"テスト", r"計測", r"確認",
            r"調べる", r"検証", r"測る", r"見る",
            r"\?B\b", r"\[B\]", r"【B】"
        ],
        "C": [
            r"わかった", r"判明", r"潰れた", r"否定",
            r"正解", r"間違い", r"結果", r"ダメだった",
            r"\?C\b", r"\[C\]", r"【C】"
        ],
        "D": [
            r"自動化", r"テンプレ", r"再利用", r"資産化",
            r"次回も", r"定型化", r"マニュアル",
            r"\?D\b", r"\[D\]", r"【D】"
        ],
    }

    def __init__(self):
        """初期化"""
        # パターンを正規表現オブジェクトにコンパイル
        self.compiled_patterns = {
            event_type: [re.compile(pattern) for pattern in patterns]
            for event_type, patterns in self.PATTERNS.items()
        }

    def extract_from_message(
        self,
        message_text: str,
        message_url: str,
        timestamp: datetime,
        existing_topics: Optional[List[str]] = None,
    ) -> Optional[ADEvent]:
        """
        単一のメッセージからA-Dイベントを抽出

        Args:
            message_text: Slackメッセージのテキスト
            message_url: メッセージのURL
            timestamp: メッセージのタイムスタンプ
            existing_topics: 既存のトピックIDリスト（紐付け用）

        Returns:
            ADEventオブジェクト。イベントが見つからない場合はNone。
        """
        if existing_topics is None:
            existing_topics = []

        # 各イベントタイプでパターンマッチング
        for event_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(message_text):
                    # トピックIDの生成（既存トピックに紐付けなければ新規生成）
                    topic_id = self._generate_topic_id(
                        message_text, existing_topics
                    )

                    # 信頼度の算出
                    confidence = self._calculate_confidence(
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

        return None

    def extract_from_messages(
        self,
        messages: List[dict],
        existing_topics: Optional[List[str]] = None,
    ) -> List[ADEvent]:
        """
        複数のメッセージからA-Dイベントを抽出

        Args:
            messages: メッセージ辞書のリスト
                     各辞書は "text", "url", "timestamp" キーを持つ必要がある
            existing_topics: 既存のトピックIDリスト

        Returns:
            ADEventオブジェクトのリスト
        """
        if existing_topics is None:
            existing_topics = []

        events = []
        for message in messages:
            event = self.extract_from_message(
                message_text=message.get("text", ""),
                message_url=message.get("url", ""),
                timestamp=message.get("timestamp", datetime.now()),
                existing_topics=existing_topics,
            )
            if event:
                events.append(event)

        return events

    def _generate_topic_id(
        self, message_text: str, existing_topics: List[str]
    ) -> str:
        """
        メッセージからトピックIDを生成または既存トピックに紐付け

        Args:
            message_text: メッセージテキスト
            existing_topics: 既存のトピックIDリスト

        Returns:
            トピックID
        """
        # 簡易実装: メッセージの先頭20文字をハッシュ化してトピックIDとする
        # 実際の運用では、より高度な類似度マッチングが必要
        import hashlib

        text_preview = message_text[:20].strip()
        hash_obj = hashlib.md5(text_preview.encode())
        return f"topic-{hash_obj.hexdigest()[:8]}"

    def _calculate_confidence(
        self, message_text: str, event_type: str
    ) -> float:
        """
        イベントの信頼度を算出

        Args:
            message_text: メッセージテキスト
            event_type: イベントタイプ

        Returns:
            信頼度（0.0 - 1.0）
        """
        confidence = 0.5  # デフォルト値

        # 明示的なタグ（[A], [B]等）があれば信頼度を高く
        explicit_tags = [rf"\[{event_type}\]", rf"【{event_type}】"]
        for tag in explicit_tags:
            if re.search(tag, message_text):
                confidence = 0.9
                break

        # 文脈キーワードの数で信頼度を調整
        keyword_count = sum(
            1
            for pattern in self.PATTERNS[event_type]
            if re.search(pattern, message_text)
        )
        confidence += min(keyword_count * 0.05, 0.3)

        return min(confidence, 1.0)
