# PR-002: CONTRIBUTING.mdの作成

## Status
**Draft** | Phase 1 | Priority: HIGH

## Problem
開発環境のセットアップ方法・テスト実行方法がドキュメント化されていない。
新規コントリビューターが開発を始めるのに手間取る。

## Solution
CONTRIBUTING.md を新規作成：

```markdown
# Contributing to Slack Knowledge Loop Tracker

## 開発環境のセットアップ

```bash
# リポジトリのクローン
git clone https://github.com/yourusername/slack_knowledge_loop_tracker.git
cd slack_knowledge_loop_tracker

# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 依存関係のインストール
pip install -e ".[dev]"
```

## テストの実行

```bash
# 全テスト実行
pytest

# カバレッジ付きで実行
pytest --cov=src --cov-report=html

# 特定のテストのみ実行
pytest tests/test_extractor.py
```

## コードスタイル

- PEP 8 準拠
- 型ヒントを必ず付与する
- docstringを追加する（Google Style）

## プルリクエストの送信

1. 機能ブランチを作成: `git checkout -b feature/your-feature`
2. 変更をコミット: `git commit -m "feat: add XXX"`
3. プッシュ: `git push origin feature/your-feature`
4. PRを作成

## 必読ドキュメント

- SYSTEM_CONSTITUTION.md: 憲法・不変の定義
- PURPOSE.md: 大目標・非目標
- AGENTS.md: AIエージェント向け指示
```

## Expected Outcome
- 新規コントリビューターのオンボーディングがスムーズになる
- 開発プロセスが標準化される

## Side Effects
なし

## Verification
- 新しい環境で CONTRIBUTING.md の手順に従って開発環境を構築できる
- pytest が正常に実行できる

## Rollback
CONTRIBUTING.md を削除

## Related
- PR-001: インストール手順の追加
- PR-003: テストカバレッジ計測の導入
