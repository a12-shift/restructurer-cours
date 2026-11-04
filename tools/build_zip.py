"""Construit dist/<nom>.zip, l'archive à importer dans Claude (Customize > Skills).

Claude attend le dossier du skill à la racine de l'archive (<nom>/SKILL.md),
avec un nom de dossier identique au champ `name` de SKILL.md.

Usage : python tools/build_zip.py
"""

import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
# Contenu du skill copié dans l'archive ; les dossiers absents sont ignorés.
SKILL_ENTRIES = ("SKILL.md", "LICENSE", "references", "assets")
TEXT_SUFFIXES = {".md", ".txt"}
FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.DOTALL)
NAME_PATTERN = re.compile(r"^name:\s*[\"']?([a-z0-9-]+)[\"']?\s*$", re.MULTILINE)


def read_skill_name(skill_md: Path) -> str:
    frontmatter = FRONTMATTER_PATTERN.match(skill_md.read_text(encoding="utf-8"))
    if not frontmatter:
        sys.exit("SKILL.md : en-tête YAML (---) introuvable.")
    name = NAME_PATTERN.search(frontmatter.group(1))
    if not name:
        sys.exit("SKILL.md : champ `name` introuvable ou invalide.")
    return name.group(1)


def list_files(entry: Path) -> list[Path]:
    if entry.is_file():
        return [entry]
    if entry.is_dir():
        return sorted(path for path in entry.rglob("*") if path.is_file())
    return []


def copy_file(source: Path, target: Path) -> None:
    """Copie un fichier en forçant les fins de ligne LF pour le texte."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix in TEXT_SUFFIXES:
        content = source.read_text(encoding="utf-8").replace("\r\n", "\n")
        target.write_text(content, encoding="utf-8", newline="\n")
    else:
        shutil.copy2(source, target)


def stage(name: str) -> Path:
    """Copie le skill dans dist/<nom>/, dossier aussi utilisé pour la validation."""
    staging = DIST / name
    if staging.exists():
        shutil.rmtree(staging)
    for entry in SKILL_ENTRIES:
        for source in list_files(ROOT / entry):
            copy_file(source, staging / source.relative_to(ROOT))
    return staging


def build_archive(staging: Path) -> Path:
    archive = DIST / f"{staging.name}.zip"
    archive.unlink(missing_ok=True)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in list_files(staging):
            zf.write(path, path.relative_to(DIST).as_posix())
    return archive


def check_archive(archive: Path, name: str) -> list[str]:
    with zipfile.ZipFile(archive) as zf:
        entries = zf.namelist()
    misplaced = [entry for entry in entries if not entry.startswith(f"{name}/")]
    if f"{name}/SKILL.md" not in entries or misplaced:
        sys.exit(f"{archive.name} : structure invalide, attendu {name}/SKILL.md à la racine.")
    return entries


def main() -> None:
    name = read_skill_name(ROOT / "SKILL.md")
    archive = build_archive(stage(name))
    entries = check_archive(archive, name)
    print(f"{archive.relative_to(ROOT).as_posix()} :")
    for entry in entries:
        print(f"  {entry}")


if __name__ == "__main__":
    main()
