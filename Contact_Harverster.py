#!/usr/bin/env python3
"""
Contact Harvester
Converts users table from SQLite to vCard (.vcf) file
"""

import sqlite3
import argparse
import os
import sys
from datetime import datetime
import pyfiglet
from alive_progress import alive_bar


def parse_arguments():
    parser = argparse.ArgumentParser(description="Export contacts from SQLite to vCard file")
    parser.add_argument("--db", default="users.db", help="Path to SQLite database")
    parser.add_argument("--output", default="contacts.vcf", help="Output vCard file")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    return parser.parse_args()


def get_users(db_path: str) -> list:
    if not os.path.isfile(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}")


def prepare_contact(user_row) -> dict:
    # Adjust indexes according to your real schema
    # Assuming: id, firstname?, fullname?, ..., phone (index 5)
    full_name = (user_row[1] or "").strip()
    phone = (user_row[5] or "").strip()

    if not phone:
        return None

    # Very simple name splitting — improve later
    parts = full_name.split(maxsplit=1)
    first = parts[0] if parts else ""
    last = parts[1] if len(parts) > 1 else ""

    return {
        "first": first,
        "last": last,
        "full": full_name,
        "phone": phone,
    }


def generate_vcard_lines(contacts: list[dict], version="3.0") -> list[str]:
    lines = []

    for i, c in enumerate(contacts, 1):
        if not c:
            continue

        lines.append("BEGIN:VCARD")
        lines.append(f"VERSION:{version}")
        lines.append(f"N:{c['last']};{c['first']};;;")
        lines.append(f"FN:{c['full']}")
        lines.append(f"TEL;TYPE=CELL:{c['phone']}")
        lines.append(f"REV:{datetime.utcnow().isoformat()}+00:00")
        lines.append("END:VCARD\n")

    return lines


def main():
    args = parse_arguments()

    if args.version:
        print("Contact Harvester v0.1.0")
        return

    print(pyfiglet.figlet_format("Contact Harvester", font="small"))

    try:
        print(f"Reading database: {args.db}")
        rows = get_users(args.db)
        print(f"Found {len(rows)} rows")

        contacts = []
        print("Processing contacts...")
        with alive_bar(len(rows), title="Converting") as bar:
            for row in rows:
                contact = prepare_contact(row)
                if contact:
                    contacts.append(contact)
                bar()

        if not contacts:
            print("No valid contacts found.")
            return

        print(f"Generating vCard for {len(contacts)} contacts...")
        vcard_lines = generate_vcard_lines(contacts, version="3.0")

        with open(args.output, "w", encoding="utf-8") as f:
            f.write("\n".join(vcard_lines))

        print(f"\nSuccess! Written {len(contacts)} contacts to → {args.output}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
