# vocab-flashcards

A small toolkit that builds English vocabulary flashcards (Vietnamese meanings) as CSV files for [Anki](https://apps.ankiweb.net/).

- `script.py` exports every vocabulary set in `base-vocab.json` to `output/<set name>/<set name>.csv`, one subfolder per set.
- The Claude Code skill `vocab-csv` builds a set from a screenshot of a Reading/Listening exercise, using only the words highlighted in yellow.

Pronunciation uses **British (RP) IPA**, taken from `ipa.json`.

## Structure

```
.
├── script.py                 # base-vocab.json -> output/<set name>/<set name>.csv
├── base-vocab.json           # array of vocabulary sets (name, words...)
├── ipa.json                  # British IPA dictionary ("word" or "word|pos" -> "/ipa/")
├── .claude/skills/vocab-csv/
│   ├── SKILL.md              # rules for building a set from an exercise
│   └── scripts/build_csv.py  # JSON -> CSV in the expected format
└── output/                   # one subfolder per set, not committed
    └── <set name>/<set name>.csv
```

## CSV format

UTF-8 with BOM, no header row, 7 columns:

| Column | Meaning |
|---|---|
| `en` | Word or phrase (base form) |
| `ipa` | British IPA |
| `pos` | Part of speech: `n`, `v`, `adj`, `adv`, `phr v`, `idiom`... |
| `vi` | Vietnamese meaning. If the meaning in the passage differs from the usual one: `{meaning in passage}, {common meanings}` |
| `formula` | Grammar pattern (`pay off`, `stash sth (away)`) |
| `colloc` | Common collocations |
| `note` | Explanation and examples, line breaks as `<br>` |

## Usage

Requires Python 3.8+ (no third-party packages).

### Export all vocabulary sets

```bash
python script.py
```

### Build a set from an exercise (Claude Code)

Open this folder in Claude Code, attach screenshots of the exercise with highlighted words and type:

```
/vocab-csv
```

The skill writes the data to JSON and then runs:

```bash
python .claude/skills/vocab-csv/scripts/build_csv.py <input.json> "output/<Set name>/<Set name>.csv"
```

The script fills empty `ipa` cells from `ipa.json`, normalises `/.../`, turns line breaks into `<br>` and drops duplicate rows.

### Import into Anki

**File → Import**, choose the CSV file, set the separator to *Comma*, enable *Allow HTML in fields*, then map the 7 columns to the fields of your note type.
