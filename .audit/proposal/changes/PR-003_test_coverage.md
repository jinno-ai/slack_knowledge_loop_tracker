# PR-003: テストカバレッジ計測の導入

## Status
**Draft** | Phase 1 | Priority: MEDIUM

## Problem
現状、テストカバレッジが計測されていない。
QA-001 の目標「>= 80%」に対する現状が不明。

## Solution
pytest-cov の設定を追加：

### 1. pyproject.toml にカバレッジ設定を追加

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "--cov=src --cov-report=term-missing --cov-fail-under=80"
```

### 2. CI設定の追加（.github/workflows/test.yml）

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.9"
      - run: pip install -e ".[dev]"
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v3
```

## Expected Outcome
- `pytest` 実行時に自動的にカバレッジが表示される
- CIでカバレッジが継続的に監視される
- 80%未満の場合にテストが失敗するようになる

## Side Effects
- カバレッジが80%未満の場合、テストが失敗するようになる
- 既存テストの品質向上が必要になる可能性がある

## Verification
- `pytest` 実行時にカバレッジレポートが表示される
- カバレッジが80%以上の場合にテストが成功する

## Rollback
pyproject.toml から `addopts` を削除
CI設定を削除

## Related
- PR-001: インストール手順の追加
- PR-002: CONTRIBUTING.mdの作成
