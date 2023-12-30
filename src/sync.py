from pathlib import Path
from shutil import copytree
import yaml

with open("./config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f.read())

ob_path = Path(CONFIG['obsidian_base_path'])

root_path = Path(__file__).resolve().parent.parent

relative_paths = [".obsidian/snippets", "setting/js", "setting/templates"]
for rp in relative_paths:
    copytree(ob_path / rp, root_path / rp, dirs_exist_ok=True)
