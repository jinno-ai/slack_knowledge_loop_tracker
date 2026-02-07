# PR-004: Slack SDKの導入

## Status
**Draft** | Phase 2 | Priority: HIGH

## Problem
Slack API連携機能が未実装（Gap-1）。
実際のSlackメッセージを取得できない。

## Solution
Slack SDK を依存関係に追加し、認証設定を追加：

### 1. pyproject.toml に依存を追加

```toml
[project.optional-dependencies]
slack = ["slack-sdk>=3.0.0"]
```

### 2. .env.example を作成

```bash
# Slack OAuth Token (xoxb-...)
SLACK_BOT_TOKEN=

# Slack App Client ID (optional)
SLACK_CLIENT_ID=

# Slack App Client Secret (optional)
SLACK_CLIENT_SECRET=

# Slack Signing Secret (optional, for webhook)
SLACK_SIGNING_SECRET=
```

### 3. README.md にSlack App設定手順を追加

```markdown
## Slack Appの設定

1. [Slack API](https://api.slack.com/apps) で新しいAppを作成
2. Bot Token Scopes に以下を追加:
   - `channels:history`
   - `channels:read`
   - `groups:history`
   - `groups:read`
   - `im:history`
   - `im:read`
   - `mpim:history`
   - `mpim:read`
3. Bot User OAuth Token をコピー
4. `.env` ファイルに `SLACK_BOT_TOKEN=xoxb-...` を設定
```

## Expected Outcome
- ユーザーがSlack Appを作成できるようになる
- 開発環境でSlack APIを使用できるようになる

## Side Effects
- Slack SDKへの依存が増える
- セキュリティ：SLACK_BOT_TOKEN は .gitignore に追加する必要がある

## Verification
- `pip install -e ".[slack]"` でインストールできる
- python REPL で `import slack_sdk` が成功する

## Rollback
pyproject.toml から slack-sdk を削除
.env.example を削除

## Related
- PR-005: Slack APIクライアントの実装
- PR-006: 環境変数設定の追加

## Note
※ このPRは依存関係の追加のみ。実際のAPI連携は PR-005 で実装。
