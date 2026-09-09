#!/usr/bin/env python3
"""Create publication-ready source copies from exported WeChat Markdown."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs"
OUTPUT = ROOT / "blog" / "clean-source"
OUTPUT.mkdir(parents=True, exist_ok=True)

# These strings begin platform UI, subscription calls-to-action, or unrelated promotion.
CUT_MARKERS = re.compile(
    r"预览时标签不可点|微信扫一扫|后台回复关键词|加入.*讨论群|获取ACL|获取.*论文|关注该公众号"
)
PLATFORM_MARKERS = re.compile(r"预览时标签不可点|微信扫一扫|使用小程序|轻点两下|分享\s+留言\s+收藏")

for source in sorted(SOURCE.glob("*.md")):
    lines = source.read_text(encoding="utf-8").splitlines()
    cleaned = []
    cutoff = False
    for index, line in enumerate(lines):
        if PLATFORM_MARKERS.search(line):
            cutoff = True
            break
        if index > len(lines) * 0.55 and line.lstrip().startswith(">>>"):
            cutoff = True
            break
        # Promotional modules are always in the final 45% of these exports.
        if index > len(lines) * 0.55 and CUT_MARKERS.search(line):
            cutoff = True
            break
        if CUT_MARKERS.search(line):
            continue
        cleaned.append(line)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    # WeChat exports append three or four promotional QR-code images after the
    # editorial conclusion. Preserve article illustrations but discard such tails.
    trailing_images = 0
    cursor = len(cleaned) - 1
    while cursor >= 0:
        if not cleaned[cursor].strip():
            cursor -= 1
            continue
        if cleaned[cursor].lstrip().startswith("![]("):
            trailing_images += 1
            cursor -= 1
            continue
        break
    if trailing_images >= 3:
        cleaned = cleaned[: cursor + 1]
        while cleaned and not cleaned[-1].strip():
            cleaned.pop()
    (OUTPUT / source.name).write_text("\n".join(cleaned) + "\n", encoding="utf-8")
    print(f"{source.name}: {len(lines)} -> {len(cleaned)} lines{' (trimmed)' if cutoff else ''}")
