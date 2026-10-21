
from pathlib import Path

# Locate the original policy text.
project_dir = Path(__file__).resolve().parent
path = project_dir / "texts" / "POL01.txt"

text = path.read_text(encoding="utf-8")

# Create a backup only if one does not already exist.
backup = path.with_suffix(".txt.bak")

if not backup.exists():
    backup.write_text(text, encoding="utf-8")
    print("Original backup created:", backup.name)
else:
    print("Existing backup preserved:", backup.name)

# Repair confirmed spacing issues only.
replacements = {
    "specieslisted": "species listed",
    "MemberStatein": "Member State in",
    "MemberState": "Member State",
    "thefollowing": "the following",
    "areaof": "area of",
    "andcondition": "and condition",
    "andtrend": "and trend",
    "andthe": "and the",
    "theareas": "the areas",
    "forforest": "for forest",
    "listedin": "listed in",
    "Article 12(3);(g)": "Article 12(3); (g)",
}

for old, new in replacements.items():
    count = text.count(old)

    if count > 0:
        text = text.replace(old, new)
        print(f"{old!r} -> {new!r}: {count} replacement(s)")

path.write_text(text, encoding="utf-8")

print("\nFinished.")
print("Updated file:", path)
print("Please check the corrected text against the original legal source.")
