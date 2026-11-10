"""Build artifacts/version_log.csv from REAL run JSON files (no hand-typed metrics).

For each version label (v0..v3) it picks the newest *valid* base run
(provider_error_cases == 0 and measured_cases == total_cases) and writes one row.
metric_before = case_accuracy of the previous version's run.

Usage (from starter_v0/):
    python scripts/fill_version_log.py --author "Nhom145"
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VERSIONS = {
    "v0": ("baseline", "starter prompt + tools chưa sửa",
           "Đo baseline để có mốc so sánh"),
    "v1": ("system_prompt.md", "Bỏ 3 chỉ dẫn xấu của starter (đoán thay vì hỏi, gửi không cần xác nhận, ép một bước); thêm boundary clarify/yes_no/no-tool",
           "Prompt starter ra lệnh đoán bừa và gửi ngay nên các case missing_info / wrong_boundary / out_of_scope / parallel fail; đổi thành hỏi lại + xác nhận sẽ sửa nhóm lỗi này"),
    "v2": ("tools.yaml", "Viết lại description: khi nào dùng / không dùng + convention args (handle không @, name→handle, query chỉ chủ đề, topic=news, timeframe, search_type=Top)",
           "Lỗi còn lại chủ yếu là sai arg (query thừa chữ, thiếu topic/timeframe, sai search_type, sai handle) do description mơ hồ; mô tả convention ngay trong parameter sẽ tăng argument_accuracy"),
    "v3": ("system_prompt.md", "Thêm rule multi-turn (latest turn thắng, carry args, correction), routing table, bảng name→handle",
           "Case multi-turn fail vì model không biết gộp args qua các lượt / xử lý sửa sai; rule multi-turn tường minh sẽ tăng multiturn_accuracy"),
}


def metric(summary: dict) -> str:
    return (f"case={summary.get('case_accuracy')};routing={summary.get('tool_routing_accuracy')};"
            f"args={summary.get('argument_accuracy')};multi={summary.get('multiturn_accuracy')}")


def newest_valid_run(version: str, suite: str) -> tuple[Path, dict] | None:
    best = None
    for path in sorted((ROOT / "runs").glob(f"{version}_B_{suite}_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        s = data["summary"]
        if s["provider_error_cases"] == 0 and s["measured_cases"] == s["total_cases"]:
            best = (path, data)
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", default="Nhom145")
    parser.add_argument("--suite", default="base")
    args = parser.parse_args()

    rows = []
    previous = ""
    for version, (changed, reason, hypothesis) in VERSIONS.items():
        found = newest_valid_run(version, args.suite)
        if not found:
            print(f"!! {version}: no valid {args.suite} run in runs/ - run it first (skipped)")
            continue
        path, data = found
        after = metric(data["summary"])
        rows.append({
            "version": version, "author": args.author, "changed_artifact": changed,
            "artifact_version": data["artifact_version"], "prompt_hash": data["prompt_hash"][:12],
            "tools_hash": data["tools_hash"][:12], "reason": reason, "hypothesis": hypothesis,
            "metric_before": previous or "n/a", "metric_after": after,
            "run_file": f"runs/{path.name}",
        })
        previous = after
        print(f"{version}: {after}  <- {path.name}")

    out = ROOT / "artifacts" / "version_log.csv"
    fields = ["version", "author", "changed_artifact", "artifact_version", "prompt_hash", "tools_hash",
              "reason", "hypothesis", "metric_before", "metric_after", "run_file"]
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {out}")


if __name__ == "__main__":
    main()
