# Improvement Roadmap
version: "1.0"
generated_at: "2025-02-07T12:00:00Z"

## Current Status
- **Phase**: 初期実装完了・Slack連携未実装
- **Core Functions**: 3/4 実装済み（CF-001, CF-002, CF-003 ✅ | CF-004 ❌）
- **Verification**: ✅ 実装済み機能の検証完了

## Roadmap

### Phase 1: 基盤整備（優先度: HIGH）
**Goal**: ユーザーがライブラリをインストールして使える状態にする

| PR | タイトル | 説明 | 依存関係 |
|----|---------|------|----------|
| PR-001 | インストール手順の追加 | READMEにpip install手順を追加 | なし |
| PR-002 | CONTRIBUTING.mdの作成 | 開発環境セットアップ・テスト実行方法を記載 | PR-001 |
| PR-003 | テストカバレッジ計測の導入 | pytest-covの設定とCIでの実行 | PR-002 |

### Phase 2: Slack連携（優先度: HIGH）
**Goal**: 実際のSlackメッセージを取得できるようにする

| PR | タイトル | 説明 | 依存関係 |
|----|---------|------|----------|
| PR-004 | Slack SDKの導入 | slackclient依存の追加と認証設定 | PR-001 |
| PR-005 | Slack APIクライアントの実装 | Webhook受信/メッセージ取得機能 | PR-004 |
| PR-006 | 環境変数設定の追加 | .env.exampleとSLACK_TOKENのドキュメント | PR-005 |

### Phase 3: データ永続化（優先度: MEDIUM）
**Goal**: Topic台帳・イベントログを保存できるようにする

| PR | タイトル | 説明 | 依存関係 |
|----|---------|------|----------|
| PR-007 | Topic台帳のフォーマット定義 | JSON/CSV形式での永続化 | なし |
| PR-008 | TopicLedgerクラスの実装 | 台帳の読み書き・マージ機能 | PR-007 |
| PR-009 | 類似度マッチングの改善 | 文字列類似度によるTopic紐付け | PR-008 |

### Phase 4: 日次指標追跡（優先度: HIGH）
**Goal**: 日次指標（新規A、A→B、滞留A中央値）を計算できるようにする

| PR | タイトル | 説明 | 依存関係 |
|----|---------|------|----------|
| PR-010 | イベント集計モジュールの実装 | 日次指標の計算ロジック | PR-008 |
| PR-011 | レポート出力機能の追加 | JSON/Markdown形式でのレポート出力 | PR-010 |
| PR-012 | 簡易ダッシュボードの実装 | HTML/Console形式での可視化 | PR-011 |

## Priority Matrix
| Phase | 優先度 | 見積り | リスク |
|-------|--------|--------|--------|
| Phase 1: 基盤整備 | HIGH | 1-2日 | LOW |
| Phase 2: Slack連携 | HIGH | 3-5日 | MEDIUM（Slack App設定が必要） |
| Phase 3: データ永続化 | MEDIUM | 2-3日 | LOW |
| Phase 4: 日次指標追跡 | HIGH | 3-4日 | MEDIUM |

## Assumptions
- ASM-001: ユーザーはSlack Workspaceを管理している
- ASM-002: Slack Appの作成権限を持っている
- ASM-003: ローカル環境での実行を想定（クラウドデプロイは後日）

## Success Criteria
各Phase完了後の成功条件：
- **Phase 1**: `pip install` と `pytest` が動く
- **Phase 2**: 実際のSlackメッセージからイベント抽出ができる
- **Phase 3**: Topic台帳の保存・マージができる
- **Phase 4**: 日次指標が計算・表示できる
