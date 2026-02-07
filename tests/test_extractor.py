"""
Tests for EventExtractor
"""

import pytest
from datetime import datetime
from src.extractor import EventExtractor
from src.event import ADEvent


class TestEventExtractor:
    """EventExtractorのテストクラス"""

    def setup_method(self):
        """各テストメソッドの前に実行"""
        self.extractor = EventExtractor()

    def test_extract_type_a_event(self):
        """タイプAイベントの抽出テスト"""
        message = {
            "text": "この機能の仕様が不明です。もしかしてバグ？",
            "url": "https://slack.com/archives/ABC123/p1234567890",
            "timestamp": datetime.now(),
        }

        events = self.extractor.extract([message])

        assert len(events) == 1
        assert events[0].event_type == "A"
        assert events[0].message_text == message["text"]
        assert events[0].message_url == message["url"]
        assert events[0].confidence > 0.0

    def test_extract_type_b_event(self):
        """タイプBイベントの抽出テスト"""
        message = {
            "text": "試しにテストコードを書いて確認します",
            "url": "https://slack.com/archives/ABC123/p1234567890",
            "timestamp": datetime.now(),
        }

        events = self.extractor.extract([message])

        assert len(events) == 1
        assert events[0].event_type == "B"

    def test_extract_type_c_event(self):
        """タイプCイベントの抽出テスト"""
        message = {
            "text": "わかった！問題はここだった",
            "url": "https://slack.com/archives/ABC123/p1234567890",
            "timestamp": datetime.now(),
        }

        events = self.extractor.extract([message])

        assert len(events) == 1
        assert events[0].event_type == "C"

    def test_extract_type_d_event(self):
        """タイプDイベントの抽出テスト"""
        message = {
            "text": "次回も回るようにテンプレート化しました",
            "url": "https://slack.com/archives/ABC123/p1234567890",
            "timestamp": datetime.now(),
        }

        events = self.extractor.extract([message])

        assert len(events) == 1
        assert events[0].event_type == "D"

    def test_extract_with_explicit_tag(self):
        """明示的なタグ[A][B][C][D]のテスト"""
        message = {
            "text": "[A] パフォーマンスが気になる",
            "url": "https://slack.com/archives/ABC123/p1234567890",
            "timestamp": datetime.now(),
        }

        events = self.extractor.extract([message])

        assert len(events) == 1
        assert events[0].event_type == "A"
        assert events[0].confidence >= 0.9  # 明示的なタグは信頼度が高い

    def test_no_event_extracted(self):
        """イベントが抽出されないテスト"""
        message = {
            "text": "ただの雑文です。A-Dに関係ない会話。",
            "url": "https://slack.com/archives/ABC123/p1234567890",
            "timestamp": datetime.now(),
        }

        events = self.extractor.extract([message])

        assert len(events) == 0

    def test_extract_from_multiple_messages(self):
        """複数メッセージからの抽出テスト"""
        messages = [
            {
                "text": "[A] 新機能の設計が不安",
                "url": "https://slack.com/archives/ABC123/p1",
                "timestamp": datetime.now(),
            },
            {
                "text": "テストして確認します",
                "url": "https://slack.com/archives/ABC123/p2",
                "timestamp": datetime.now(),
            },
            {
                "text": "ただの挨拶です",
                "url": "https://slack.com/archives/ABC123/p3",
                "timestamp": datetime.now(),
            },
        ]

        events = self.extractor.extract(messages)

        assert len(events) >= 2  # 少なくとも2つは抽出される

    def test_event_to_dict(self):
        """ADEventの辞書変換テスト"""
        event = ADEvent(
            event_type="A",
            topic_id="topic-123",
            message_text="テストメッセージ",
            message_url="https://slack.com/archives/ABC123",
            timestamp=datetime.now(),
            confidence=0.8,
            note="テスト用",
        )

        event_dict = event.to_dict()

        assert event_dict["event_type"] == "A"
        assert event_dict["topic_id"] == "topic-123"
        assert event_dict["confidence"] == 0.8
        assert "timestamp" in event_dict
