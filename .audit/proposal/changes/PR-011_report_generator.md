# PR-011: レポート出力機能の追加

## Status
**Draft** | Phase 4 | Priority: HIGH

## Problem
日次指標は計算できるようになったが、レポート出力機能がない。
ユーザーが結果を確認できない。

## Solution
`src/reporter.py` を新規作成：

```python
"""
Daily Report Generator
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict


class DailyReporter:
    """日次レポートを生成するクラス"""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_report(self, metrics: Dict, date: datetime) -> str:
        """
        日次レポートを生成

        Args:
            metrics: calculate() の返り値
            date: 対象日

        Returns:
            レポートファイルパス
        """
        # JSONレポート
        json_path = self._generate_json(metrics, date)

        # Markdownレポート
        md_path = self._generate_markdown(metrics, date)

        return str(json_path)

    def _generate_json(self, metrics: Dict, date: datetime) -> Path:
        """JSON形式でレポートを出力"""
        filename = f"report_{date.strftime('%Y%m%d')}.json"
        path = self.output_dir / filename

        data = {
            "generated_at": datetime.now().isoformat(),
            "metrics": metrics,
        }

        path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        return path

    def _generate_markdown(self, metrics: Dict, date: datetime) -> Path:
        """Markdown形式でレポートを出力"""
        filename = f"report_{date.strftime('%Y%m%d')}.md"
        path = self.output_dir / filename

        md = f"""# Knowledge Loop Report - {metrics['date']}

## Summary

| 指標 | 値 |
|------|-----|
| 新規A件数 | {metrics['new_a_count']} |
| A→B件数 | {metrics['a_to_b_count']} |
| 滞留A中央値 | {metrics['stuck_a_median_days']} 日 |

## Interpretation

### 新規A件数: {metrics['new_a_count']}
- {'✅ 未知が表に出ている' if metrics['new_a_count'] > 0 else '⚠️ 新しい未知が表出していない'}

### A→B件数: {metrics['a_to_b_count']}
- {'✅ 観測に変換されている' if metrics['a_to_b_count'] > 0 else '⚠️ 未知が観測に変換されていない'}

### 滞留A中央値: {metrics['stuck_a_median_days']} 日
- {self._interpret_stuck_a(metrics['stuck_a_median_days'])}

---

Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        path.write_text(md)
        return path

    @staticmethod
    def _interpret_stuck_a(median_days: float) -> str:
        """滞留A中央値の解釈"""
        if median_days < 3:
            return "✅ 健全：未知が迅速に処理されている"
        elif median_days < 7:
            return "⚠️ 要注意：未知が滞留し始めている"
        else:
            return "❌ 問題あり：未知が腐っている"
```

## Expected Outcome
- 日次レポートが JSON/Markdown 形式で出力される
- チームが指標を確認できる

## Side Effects
- レポートファイルが増えていく（ローテーションが必要）

## Verification
- `generate_report()` でレポートが生成される
- JSON/Markdown の形式が正しい

## Rollback
src/reporter.py を削除

## Related
- PR-010: イベント集計モジュールの実装
- PR-012: 簡易ダッシュボードの実装
