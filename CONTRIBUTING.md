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

## 開発の優先順位

1. **安全性**: 人を評価・点数化する機能を追加しない
2. **本質**: A→B→C→Dのループが回ることを優先
3. **検証**: 改善は必ずテストで証明する

## 禁止事項

- 人を評価・点数化する機能の追加
- PII（個人情報）をログに出力するコードの追加
- AI抽出精度を優先しすぎて UX を悪化させる変更
