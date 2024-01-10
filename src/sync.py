from pathlib import Path
from shutil import copytree, copyfile
import yaml
import os

with open("./config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f.read())

ob_path = Path(CONFIG['obsidian_base_path'])

root_path = Path(__file__).resolve().parent.parent

relative_paths = [
    ".obsidian/snippets", "setting/js", "setting/templates",
    "setting/podcast.py"
]
for rp in relative_paths:
    origin_p = ob_path / rp
    print(origin_p)
    if origin_p.is_dir():
        copytree(origin_p, root_path / rp, dirs_exist_ok=True)
    elif origin_p.is_file():
        copyfile(origin_p, root_path / rp)
    else:
        raise Warning(f"Unknown path: {rp}")
