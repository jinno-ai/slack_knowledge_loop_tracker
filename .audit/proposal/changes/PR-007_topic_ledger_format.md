# PR-007: Topic台帳のフォーマット定義

## Status
**Draft** | Phase 3 | Priority: MEDIUM

## Problem
Topic台帳のフォーマット・永続化方法が未定義（Gap-3, C-010）。
既存Topicとの紐付け・マージができない。

## Solution
Topic台帳のJSONフォーマットを定義：

### topic_ledger.json

```json
{
  "version": "1.0",
  "updated_at": "2025-02-07T12:00:00Z",
  "topics": [
    {
      "topic_id": "topic-12345678",
      "title": "温度条件での割り込み遅延",
      "first_seen": "2025-02-01T10:00:00Z",
      "last_updated": "2025-02-07T10:00:00Z",
      "status": "B",
      "owner": "username",
      "next_action": "テストコードを書く",
      "age_days": 6,
      "event_count": 3
    }
  ]
}
```

### イベントログ events.json

```json
{
  "version": "1.0",
  "updated_at": "2025-02-07T12:00:00Z",
  "events": [
    {
      "date": "2025-02-07",
      "thread_url": "https://slack.com/archives/ABC123/p1234567890",
      "event_type": "A",
      "topic_id": "topic-12345678",
      "topic_title": "温度条件での割り込み遅延",
      "message_url": "https://slack.com/archives/ABC123/p1234567890",
      "author": "username",
      "confidence": 0.85,
      "note": "再現条件不明と明言"
    }
  ]
}
```

## Expected Outcome
- Topic台帳のフォーマットが標準化される
- 永続化の実装（PR-008）が容易になる

## Side Effects
- フォーマット変更の際はマイグレーションが必要になる

## Verification
- JSON Schema でフォーマットが検証できる
- サンプルデータが実際にパースできる

## Rollback
定義したJSONファイルを削除

## Related
- PR-008: TopicLedgerクラスの実装
- PR-009: 類似度マッチングの改善
