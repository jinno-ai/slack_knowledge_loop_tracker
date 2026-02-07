# PR-012: 簡易ダッシュボードの実装

## Status
**Draft** | Phase 4 | Priority: LOW

## Problem
レポート出力はできるようになったが、可視化機能がない。
指標の推移を一目で確認できない。

## Solution
簡易ダッシュボードを実装（HTML出力）：

```python
"""
Simple Dashboard Generator
"""
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class DashboardGenerator:
    """簡易ダッシュボードを生成するクラス"""

    def generate(self, metrics_history: List[Dict], output_path: str = "dashboard.html"):
        """
        HTML形式のダッシュボードを生成

        Args:
            metrics_history: 日次指標のリスト（最新順）
            output_path: 出力ファイルパス
        """
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Knowledge Loop Dashboard</title>
    <style>
        body {{ font-family: sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
        th {{ background-color: #4CAF50; color: white; }}
        .metric {{ font-size: 24px; font-weight: bold; }}
        .label {{ color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <h1>Knowledge Loop Dashboard</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <h2>Latest Metrics</h2>
    {self._render_latest_metrics(metrics_history[0] if metrics_history else {})}

    <h2>History</h2>
    {self._render_history_table(metrics_history)}
</body>
</html>
"""
        Path(output_path).write_text(html)

    def _render_latest_metrics(self, metrics: Dict) -> str:
        """最新指標を描画"""
        return f"""
    <div style="display: flex; gap: 20px;">
        <div style="background: #f0f0f0; padding: 20px; border-radius: 8px;">
            <div class="metric">{metrics.get('new_a_count', 0)}</div>
            <div class="label">新規A件数</div>
        </div>
        <div style="background: #f0f0f0; padding: 20px; border-radius: 8px;">
            <div class="metric">{metrics.get('a_to_b_count', 0)}</div>
            <div class="label">A→B件数</div>
        </div>
        <div style="background: #f0f0f0; padding: 20px; border-radius: 8px;">
            <div class="metric">{metrics.get('stuck_a_median_days', 0):.1f}</div>
            <div class="label">滞留A中央値（日）</div>
        </div>
    </div>
"""

    def _render_history_table(self, metrics_history: List[Dict]) -> str:
        """履歴テーブルを描画"""
        rows = "\\n".join([
            f"""        <tr>
            <td>{m.get('date', '')}</td>
            <td>{m.get('new_a_count', 0)}</td>
            <td>{m.get('a_to_b_count', 0)}</td>
            <td>{m.get('stuck_a_median_days', 0):.1f}</td>
        </tr>"""
            for m in metrics_history[:30]  # 最新30日分
        ])

        return f"""
    <table>
        <tr>
            <th>日付</th>
            <th>新規A件数</th>
            <th>A→B件数</th>
            <th>滞留A中央値</th>
        </tr>
{rows}
    </table>
"""
```

## Expected Outcome
- HTML形式のダッシュボードが生成される
- ブラウザで指標の推移を確認できる

## Side Effects
- HTMLファイルの生成コストがかかる
- 本格的な可視化には不向き（将来的にはグラフライブラリの導入を検討）

## Verification
- `generate()` で HTML が生成される
- ブラウザで表示できる

## Rollback
src/dashboard.py を削除

## Related
- PR-010: イベント集計モジュールの実装
- PR-011: レポート出力機能の追加

## Note
※ この実装は簡易版。将来的には Plotly/Bokeh 等のグラフライブラリ導入を検討。
