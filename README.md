# Contact Harvester

# Export contacts from a SQLite database to a standard vCard (.vcf) file

Quick & simple tool to turn a `users` table (with names & phone numbers) into a `.vcf` file  
that can be imported into phones, Google Contacts, Outlook, iCloud, etc.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white" alt="Python version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

## Features

- Reads from SQLite database (`users.db` by default)
- Creates valid vCard files (currently version 2.1)
- Beautiful console interface with progress bars
- ASCII art title banner
- Basic name → first/last splitting

## Requirements

- Python 3.8 or newer
- Libraries:
  ```bash
  pip install pyfiglet alive-progress
  ```
  *(Note: pandas is imported in the code but not actually used — can be removed)*

## Installation

```bash
git clone https://github.com/YOUR-USERNAME/contact-harvester.git
cd contact-harvester
pip install -r requirements.txt
```

(If no `requirements.txt` exists yet, just run the pip install line above.)

## Usage

**Basic run (uses default `users.db` → `contacts.vcf`):**

```bash
python harvester.py
```

**Future / recommended usage (after adding argparse):**

```bash
python harvester.py --db users.db --output my-contacts.vcf
```

The program expects a table named `users` with at least:
- Column ~2 (index 1): full name
- Column ~6 (index 5): phone number

## Expected Database Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    -- ... other columns you may have ...
    phone TEXT
);
```

## Roadmap / Ideas for Improvement

- [ ] Add command-line arguments (`--db`, `--output`, `--vcard-version`, etc.)
- [ ] Support modern vCard versions (3.0 or 4.0)
- [ ] Smarter name parsing (middle names, titles, single-name cases)
- [ ] Phone number cleaning/normalization
- [ ] Skip entries without valid phone numbers
- [ ] Colored console output
- [ ] Add --help message and --version flag
- [ ] Basic tests
- [ ] GitHub Actions for linting/formatting

## License

MIT License

Feel free to use, fork, modify — attribution appreciated but not required.

Made for fast contact migration / backup tasks.

Happy harvesting! ✨
"""
```

### How to use it right away

```python
# At the end of your script or in a separate setup file
if __name__ == "__main__":
    # ... your existing code ...

    # Optional: create README.md if it doesn't exist
    if not os.path.exists("README.md"):
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(README_CONTENT)
        print("README.md has been created!")
```
