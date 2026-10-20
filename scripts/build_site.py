"""Copy only website files to dist; no third-party packages are needed."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "dist"
DEST.mkdir(exist_ok=True)
for name in ("index.html", "styles.css", "script.js", ".nojekyll"):
    shutil.copy2(ROOT / name, DEST / name)
shutil.copytree(ROOT / "assets", DEST / "assets", dirs_exist_ok=True)
print(f"Website ready: {DEST}")
