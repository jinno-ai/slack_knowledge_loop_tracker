# PR-005: Slack APIクライアントの実装

## Status
**Draft** | Phase 2 | Priority: HIGH

## Problem
Slack SDKは導入されたが、実際のAPIクライアントが実装されていない。

## Solution
`src/slack_client.py` を新規作成：

```python
"""
Slack API Client for A-D Event Extraction
"""
import os
from typing import List, Dict, Optional
from datetime import datetime
import slack_sdk
from slack_sdk.web import WebClient
from src.event import ADEvent
from src.extractor import EventExtractor


class SlackClient:
    """Slack APIを通じてメッセージを取得・イベント抽出を行うクラス"""

    def __init__(self, token: Optional[str] = None):
        """
        Args:
            token: Slack Bot Token. 指定しない場合は環境変数 SLACK_BOT_TOKEN を使用
        """
        self.token = token or os.getenv("SLACK_BOT_TOKEN")
        if not self.token:
            raise ValueError("SLACK_BOT_TOKEN is required")
        self.client = WebClient(token=self.token)
        self.extractor = EventExtractor()

    def fetch_messages(
        self,
        channel_id: str,
        oldest: Optional[datetime] = None,
        latest: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Dict]:
        """
        指定されたチャンネルからメッセージを取得

        Args:
            channel_id: チャンネルID (C...)
            oldest: 最古のメッセージタイムスタンプ
            latest: 最新のメッセージタイムスタンプ
            limit: 取得件数

        Returns:
            メッセージ辞書のリスト
        """
        response = self.client.conversations_history(
            channel=channel_id,
            oldest=str(oldest.timestamp()) if oldest else None,
            latest=str(latest.timestamp()) if latest else None,
            limit=limit,
        )
        return response.get("messages", [])

    def extract_events_from_channel(
        self,
        channel_id: str,
        oldest: Optional[datetime] = None,
        latest: Optional[datetime] = None,
    ) -> List[ADEvent]:
        """
        チャンネルからメッセージを取得し、A-Dイベントを抽出

        Args:
            channel_id: チャンネルID
            oldest: 最古のメッセージタイムスタンプ
            latest: 最新のメッセージタイムスタンプ

        Returns:
            ADEventオブジェクトのリスト
        """
        messages = self.fetch_messages(channel_id, oldest, latest)

        # Slackメッセージ形式を変換
        formatted_messages = []
        for msg in messages:
            if "text" not in msg:
                continue
            formatted_messages.append({
                "text": msg["text"],
                "url": f"https://slack.com/archives/{channel_id}/{msg['ts']}",
                "timestamp": datetime.fromtimestamp(float(msg["ts"])),
            })

        return self.extractor.extract(formatted_messages)
```

## Expected Outcome
- 実際のSlackチャンネルからメッセージを取得できる
- 取得したメッセージからA-Dイベントを抽出できる

## Side Effects
- ネットワークアクセスが発生する
- Slack APIのレート制限に引っかかる可能性がある

## Verification
- テストチャンネルからメッセージを取得できる
- 取得したメッセージからイベントが抽出される

## Rollback
src/slack_client.py を削除

## Related
- PR-004: Slack SDKの導入
- PR-006: 環境変数設定の追加

## Note
※ テストは Mock を使用してネットワークアクセスを回避すること
