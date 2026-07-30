import subprocess
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOC_PATH = ROOT_DIR / "data" / "toc.json"

def main():
    with open(TOC_PATH, "r", encoding="utf-8") as f:
        toc = json.load(f)

    sp_ids = {"sp_04", "sp_05", "sp_06"}
    section_ids = []

    for level in toc.get("levels", []):
        if level.get("id") in sp_ids:
            for ch in level.get("chapters", []):
                for sec in ch.get("sections", []):
                    section_ids.append(sec["id"])

    print(f"Found {len(section_ids)} sections to generate in SP4, SP5, SP6.")
    
    for sec_id in section_ids:
        cmd = ["python3", str(ROOT_DIR / "scripts" / "create_chapter.py"), sec_id]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"✅ Generated: {sec_id}")
        else:
            print(f"❌ Error generating {sec_id}: {res.stderr}")

if __name__ == "__main__":
    main()
