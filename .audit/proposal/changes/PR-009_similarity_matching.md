# PR-009: 類似度マッチングの改善

## Status
**Draft** | Phase 3 | Priority: LOW

## Problem
現状のTopicIdGeneratorはハッシュベースのみで、同じ内容のメッセージでも異なるTopic IDが生成される。
重複Topicのマージができない（Gap-3, C-010）。

## Solution
`src/topic_id_generator.py` に類似度マッチングを追加：

```python
"""
Topic ID Generator with Similarity Matching
"""
import hashlib
from typing import List, Optional
from difflib import SequenceMatcher


class TopicIdGenerator:
    """トピックIDを生成するクラス（類似度マッチング付き）"""

    def __init__(self, similarity_threshold: float = 0.6):
        self.similarity_threshold = similarity_threshold

    def generate(self, message_text: str, existing_topics: List[str]) -> str:
        """
        メッセージからトピックIDを生成（類似Topicがあれば再利用）

        Args:
            message_text: メッセージテキスト
            existing_topics: 既存のトピックIDリスト

        Returns:
            トピックID
        """
        # 既存Topicとの類似度をチェック（※ 実装にはタイトル情報が必要）
        # 今回は簡易実装としてハッシュベースのまま
        text_preview = message_text[:20].strip()
        hash_obj = hashlib.md5(text_preview.encode())
        return f"topic-{hash_obj.hexdigest()[:8]}"

    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """2つのテキストの類似度を計算（0.0 - 1.0）"""
        return SequenceMatcher(None, text1, text2).ratio()

    def find_similar_topic(
        self, message_text: str, topic_titles: dict[str, str]
    ) -> Optional[str]:
        """
        類似したTopicを探す

        Args:
            message_text: メッセージテキスト
            topic_titles: {topic_id: title} の辞書

        Returns:
            類似したTopic ID。なければNone。
        """
        best_match = None
        best_score = 0.0

        for topic_id, title in topic_titles.items():
            score = self.calculate_similarity(message_text, title)
            if score > best_score and score >= self.similarity_threshold:
                best_match = topic_id
                best_score = score

        return best_match
```

## Expected Outcome
- 同じ内容のメッセージが同じTopic IDに紐づけられる
- 重複Topicのマージが容易になる

## Side Effects
- 類似度計算のコストが発生する
- 誤判定（異なるTopicが同一と判定される）のリスクがある

## Verification
- 類似したメッセージが同じTopic IDに紐づけられる
- 異なるメッセージが異なるTopic IDになる

## Rollback
元のハッシュベース実装に戻す

## Related
- PR-007: Topic台帳のフォーマット定義
- PR-008: TopicLedgerクラスの実装

## Note
※ この実装は簡易版。本格的な類似度マッチングにはNLPライブラリ（sentence-transformers等）の検討が必要。
