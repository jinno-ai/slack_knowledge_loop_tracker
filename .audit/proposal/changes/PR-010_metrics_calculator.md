# PR-010: イベント集計モジュールの実装

## Status
**Draft** | Phase 4 | Priority: HIGH

## Problem
日次指標（新規A件数、A→B件数、滞留A中央値）の計算ロジックが未実装（Gap-2, CF-004）。
SYSTEM_CONSTITUTION.md §2.2 で定義された核心指標が追跡できない。

## Solution
`src/metrics.py` を新規作成：

```python
"""
Daily Metrics Calculator
"""
from datetime import datetime, timedelta
from typing import List, Dict
from collections import defaultdict
from src.event import ADEvent


class DailyMetrics:
    """日次指標を計算するクラス"""

    def __init__(self, events: List[ADEvent]):
        self.events = events

    def calculate(self, date: datetime) -> dict:
        """
        指定日の日次指標を計算

        Args:
            date: 対象日

        Returns:
            {
                "date": "2025-02-07",
                "new_a_count": 5,
                "a_to_b_count": 3,
                "stuck_a_median_days": 4.5
            }
        """
        target_date_str = date.strftime("%Y-%m-%d")

        # 新規A件数
        new_a_count = sum(
            1
            for e in self.events
            if e.event_type == "A" and e.timestamp.strftime("%Y-%m-%d") == target_date_str
        )

        # A→B件数（Aイベントの後、同日にBイベントが発生したTopicをカウント）
        a_to_b_count = self._calculate_a_to_b(date)

        # 滞留A年齢中央値
        stuck_a_median_days = self._calculate_stuck_a_median(date)

        return {
            "date": target_date_str,
            "new_a_count": new_a_count,
            "a_to_b_count": a_to_b_count,
            "stuck_a_median_days": stuck_a_median_days,
        }

    def _calculate_a_to_b(self, date: datetime) -> int:
        """A→B件数を計算"""
        target_date_str = date.strftime("%Y-%m-%d")

        # 当日のAイベントをGroup化
        a_topics = {
            e.topic_id
            for e in self.events
            if e.event_type == "A" and e.timestamp.strftime("%Y-%m-%d") == target_date_str
        }

        # 当日のBイベントをGroup化
        b_topics = {
            e.topic_id
            for e in self.events
            if e.event_type == "B" and e.timestamp.strftime("%Y-%m-%d") == target_date_str
        }

        # A→Bの共通Topic数を返す
        return len(a_topics & b_topics)

    def _calculate_stuck_a_median(self, date: datetime) -> float:
        """滞留A年齢中央値を計算"""
        target_date = date.date()

        # 全Aイベントのトピックと初出日を集計
        topic_first_seen = {}
        for e in self.events:
            if e.event_type == "A":
                if e.topic_id not in topic_first_seen:
                    topic_first_seen[e.topic_id] = e.timestamp.date()

        # 現在Aのままのトピックを抽出（※ 実装にはTopic台帳が必要）
        # 今回は簡易実装として、全Aトピックの年齢を計算
        ages = [
            (target_date - first_seen).days
            for first_seen in topic_first_seen.values()
        ]

        if not ages:
            return 0.0

        # 中央値を計算
        sorted_ages = sorted(ages)
        n = len(sorted_ages)
        if n % 2 == 0:
            return (sorted_ages[n // 2 - 1] + sorted_ages[n // 2]) / 2
        else:
            return float(sorted_ages[n // 2])
```

## Expected Outcome
- 日次指標が計算できる
- SYSTEM_CONSTITUTION.md §2.2 の核心指標が追跡可能になる

## Side Effects
- 件数増加に伴い計算コストが増加する

## Verification
- サンプルイベントデータで日次指標が正しく計算される
- 新規A、A→B、滞留A中央値が正しい値を返す

## Rollback
src/metrics.py を削除

## Related
- PR-007: Topic台帳のフォーマット定義
- PR-008: TopicLedgerクラスの実装
- PR-011: レポート出力機能の追加

## Note
※ 滞留Aの判定にはTopic台帳（現在のstatusがAのもの）が必要。
   現状の実装は簡易版で、将来的にはTopic台帳との連携が必要。
