"""
Topic ID Generator
"""

import hashlib


class TopicIdGenerator:
    """トピックIDを生成するクラス"""

    def generate(self, message_text: str, existing_topics: list[str]) -> str:
        """
        メッセージからトピックIDを生成

        Args:
            message_text: メッセージテキスト
            existing_topics: 既存のトピックIDリスト（将来の類似度マッチング用）

        Returns:
            トピックID
        """
        text_preview = message_text[:20].strip()
        hash_obj = hashlib.md5(text_preview.encode())
        return f"topic-{hash_obj.hexdigest()[:8]}"
