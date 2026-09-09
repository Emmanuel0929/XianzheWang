#!/usr/bin/env python3
"""Download externally hosted images referenced by the imported blog Markdown."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUTPUT = ROOT / "blog" / "assets"
OUTPUT.mkdir(parents=True, exist_ok=True)
pattern = re.compile(r"!\[[^\]]*\]\((https?://mmbiz\.qpic\.cn/[^\s)]+)")
urls = sorted({url for path in DOCS.glob("*.md") for url in pattern.findall(path.read_text(encoding="utf-8"))})

def extension(content_type, url):
    if "png" in content_type or "wx_fmt=png" in url:
        return ".png"
    if "gif" in content_type or "wx_fmt=gif" in url:
        return ".gif"
    if "webp" in content_type or "wx_fmt=webp" in url:
        return ".webp"
    return ".jpg"

def download(url):
    digest = sha256(url.encode()).hexdigest()[:16]
    existing = list(OUTPUT.glob(digest + ".*"))
    if existing:
        return url, f"../assets/{existing[0].name}", existing[0].stat().st_size
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        data = response.read()
        content_type = response.headers.get("Content-Type", "").lower()
    if not data or not content_type.startswith("image/"):
        raise ValueError(f"not an image: {content_type}")
    filename = digest + extension(content_type, url)
    (OUTPUT / filename).write_bytes(data)
    return url, f"../assets/{filename}", len(data)

results, failures = {}, []
with ThreadPoolExecutor(max_workers=8) as pool:
    futures = [pool.submit(download, url) for url in urls]
    for future in as_completed(futures):
        try:
            url, path, _ = future.result()
            results[url] = path
        except Exception as exc:
            failures.append(str(exc))

(ROOT / "blog" / "image-map.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
for page in (ROOT / "blog" / "zh").glob("*.html"):
    content = page.read_text(encoding="utf-8")
    for url, local_path in results.items():
        content = content.replace(escape(url, quote=True), local_path).replace(url, local_path)
    page.write_text(content, encoding="utf-8")
print(f"downloaded={len(results)} failed={len(failures)}")
if failures:
    print("\n".join(failures[:10]))
