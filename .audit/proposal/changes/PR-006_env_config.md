# PR-006: 環境変数設定の追加

## Status
**Draft** | Phase 2 | Priority: HIGH

## Problem
環境変数（SLACK_BOT_TOKEN等）の管理方法が未定義。
セキュリティリスク（Tokenがコミットされる）がある。

## Solution
環境変数管理の標準化：

### 1. .gitignore に追加

```
.env
__pycache__/
*.pyc
.pytest_cache/
.coverage
htmlcov/
```

### 2. python-dotenv の追加

```toml
[project.optional-dependencies]
slack = ["slack-sdk>=3.0.0", "python-dotenv>=1.0.0"]
```

### 3. src/config.py を作成

```python
"""
Configuration management for Slack Knowledge Loop Tracker
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# .env をロード
load_dotenv()

class Config:
    """環境変数を管理するクラス"""

    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_CLIENT_ID: str = os.getenv("SLACK_CLIENT_ID", "")
    SLACK_CLIENT_SECRET: str = os.getenv("SLACK_CLIENT_SECRET", "")
    SLACK_SIGNING_SECRET: str = os.getenv("SLACK_SIGNING_SECRET", "")

    @classmethod
    def validate(cls) -> bool:
        """必須設定がされているかチェック"""
        if not cls.SLACK_BOT_TOKEN:
            raise ValueError("SLACK_BOT_TOKEN is required")
        return True
```

## Expected Outcome
- Token が誤ってコミットされるリスクが回避される
- 環境ごとの設定管理が容易になる

## Side Effects
- python-dotenv への依存が増える

## Verification
- .env が .gitignore に含まれている
- .env.example がコミットされている
- Config.validate() で Token のチェックができる

## Rollback
.gitignore から削除
src/config.py を削除

## Related
- PR-004: Slack SDKの導入
- PR-005: Slack APIクライアントの実装
