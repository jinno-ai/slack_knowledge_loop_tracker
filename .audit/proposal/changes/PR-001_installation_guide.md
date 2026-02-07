# PR-001: インストール手順の追加

## Status
**Draft** | Phase 1 | Priority: HIGH

## Problem
README.md に「Quick Start」はあるが、実際のインストール手順（`pip install` 等）が記載されていない。
ユーザーがライブラリをインストールして使う方法が不明確。

## Solution
README.md に以下のセクションを追加：

```markdown
## インストール

```bash
# リポジトリのクローン
git clone https://github.com/yourusername/slack_knowledge_loop_tracker.git
cd slack_knowledge_loop_tracker

# 依存関係のインストール
pip install -e .

# 開発用依存関係（テスト等）
pip install -e ".[dev]"
```

## 基本的な使い方

```python
from src.extractor import EventExtractor

# メッセージを準備
messages = [
    {
        "text": "[A] この機能の仕様が不明です",
        "url": "https://slack.com/archives/...",
        "timestamp": "2025-02-07T10:00:00Z"
    }
]

# イベントを抽出
extractor = EventExtractor()
events = extractor.extract(messages)

for event in events:
    print(f"[{event.event_type}] {event.message_text} (confidence: {event.confidence})")
```
```

## Expected Outcome
- ユーザーが README だけでインストールから実行まで完結できる
- 「Hello World」的な最小実行例を提供

## Side Effects
なし

## Verification
- 新しい環境で README の手順に従ってインストールできる
- サンプルコードが実行できる

## Rollback
README.md を編集前の状態に戻す

## Related
- PR-002: CONTRIBUTING.mdの作成
- PR-003: テストカバレッジ計測の導入
