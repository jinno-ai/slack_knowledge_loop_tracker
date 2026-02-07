# PR-008: TopicLedgerクラスの実装

## Status
**Draft** | Phase 3 | Priority: MEDIUM

## Problem
Topic台帳のフォーマットは定義されたが、読み書き・マージ機能が未実装。

## Solution
`src/topic_ledger.py` を新規作成：

```python
"""
Topic Ledger Management
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class Topic:
    """Topicデータモデル"""
    topic_id: str
    title: str
    first_seen: str
    last_updated: str
    status: str  # "A", "B", "C", "D"
    owner: Optional[str] = None
    next_action: Optional[str] = None
    age_days: int = 0
    event_count: int = 0


class TopicLedger:
    """Topic台帳の管理クラス"""

    def __init__(self, ledger_path: str = "topic_ledger.json"):
        self.ledger_path = Path(ledger_path)
        self.topics: Dict[str, Topic] = {}
        self._load()

    def _load(self):
        """台帳をロード"""
        if self.ledger_path.exists():
            data = json.loads(self.ledger_path.read_text())
            for topic_data in data.get("topics", []):
                topic = Topic(**topic_data)
                self.topics[topic.topic_id] = topic

    def save(self):
        """台帳を保存"""
        data = {
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "topics": [asdict(t) for t in self.topics.values()],
        }
        self.ledger_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def get_or_create(self, topic_id: str, title: str = "") -> Topic:
        """Topicを取得または作成"""
        if topic_id not in self.topics:
            now = datetime.now().isoformat()
            self.topics[topic_id] = Topic(
                topic_id=topic_id,
                title=title or topic_id,
                first_seen=now,
                last_updated=now,
                status="A",
                age_days=0,
                event_count=0,
            )
        return self.topics[topic_id]

    def update_status(self, topic_id: str, new_status: str):
        """Topicのステータスを更新"""
        if topic_id in self.topics:
            topic = self.topics[topic_id]
            if self._status_priority(new_status) > self._status_priority(topic.status):
                topic.status = new_status
                topic.last_updated = datetime.now().isoformat()

    def _status_priority(self, status: str) -> int:
        """ステータスの優先度（A < B < C < D）"""
        return {"A": 1, "B": 2, "C": 3, "D": 4}.get(status, 0)
```

## Expected Outcome
- Topic台帳の読み書きができる
- イベント抽出時にTopicが自動登録・更新される

## Side Effects
- ファイルI/O が発生する
- 並列実行時の競合対策が必要（ロック等）

## Verification
- 台帳の保存・読み込みができる
- Topicのステータス更新が正しく動作する

## Rollback
src/topic_ledger.py を削除

## Related
- PR-007: Topic台帳のフォーマット定義
- PR-009: 類似度マッチングの改善
