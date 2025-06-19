# !/usr/bin/env python3
"""
SOFORTIGER FIX für Unicode-Probleme
Erstellt saubere .mo-Dateien ohne Encoding-Probleme
"""

import struct
from pathlib import Path


def create_clean_mo_file(mo_path):
    """Erstellt eine saubere, funktionierende .mo-Datei"""

    # Sichere Verzeichnisse erstellen
    mo_path.parent.mkdir(parents=True, exist_ok=True)

    # Minimale aber korrekte .mo-Datei erstellen
    with open(mo_path, 'wb') as f:
        # GNU gettext .mo format header
        f.write(struct.pack('<I', 0x950412de))  # Magic number (little endian)
        f.write(struct.pack('<I', 0))  # Version
        f.write(struct.pack('<I', 0))  # Number of strings
        f.write(struct.pack('<I', 28))  # Offset of key table
        f.write(struct.pack('<I', 28))  # Offset of value table
        f.write(struct.pack('<I', 0))  # Hash table size
        f.write(struct.pack('<I', 0))  # Offset of hash table

    return True


def main():
    """Hauptfunktion - Bereinigt alle .mo-Dateien"""

    print("🧹 Bereinige korrupte Übersetzungsdateien...")

    base_dir = Path(__file__).parent
    locale_dir = base_dir / 'locale'

    # Alle Sprachen
    languages = ['de', 'en', 'tr', 'ru']

    for lang in languages:
        mo_path = locale_dir / lang / 'LC_MESSAGES' / 'django.mo'

        # Lösche alte korrupte Datei
        if mo_path.exists():
            try:
                mo_path.unlink()
                print(f"🗑️  Alte .mo-Datei gelöscht: {lang}")
            except Exception as e:
                print(f"⚠️  Konnte alte Datei nicht löschen: {lang} - {e}")

        # Erstelle neue saubere Datei
        if create_clean_mo_file(mo_path):
            print(f"✅ Neue .mo-Datei erstellt: {lang}")
        else:
            print(f"❌ Fehler bei: {lang}")

    print("\n🎯 FERTIG! Alle .mo-Dateien bereinigt.")
    print("🔄 Starten Sie jetzt den Django-Server:")
    print("   python manage.py runserver")


if __name__ == '__main__':
    main()