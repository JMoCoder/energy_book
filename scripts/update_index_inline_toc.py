import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOC_PATH = ROOT_DIR / "data" / "toc.json"
INDEX_PATH = ROOT_DIR / "index.html"

def main():
    with open(TOC_PATH, "r", encoding="utf-8") as f:
        toc_data = json.load(f)

    toc_json_str = json.dumps(toc_data, ensure_ascii=False, separators=(',', ':'))

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(
        r'const _INLINE_TOC = \{.*?\};',
        f'const _INLINE_TOC = {toc_json_str};',
        content,
        flags=re.DOTALL
    )

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Updated index.html inline TOC successfully!")

if __name__ == "__main__":
    main()
