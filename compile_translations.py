#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path


def compile_po_to_mo():
    """Kompiliert .po-Dateien zu .mo-Dateien ohne gettext"""

    import struct

    def compile_po_file(po_file_path, mo_file_path):
        """Einfacher PO zu MO Compiler"""

        translations = {}

        try:
            with open(po_file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Einfaches Parsen der .po-Datei
            lines = content.split('\n')
            msgid = None
            msgstr = None

            for line in lines:
                line = line.strip()

                if line.startswith('msgid "'):
                    msgid = line[7:-1]  # Remove 'msgid "' and '"'
                elif line.startswith('msgstr "'):
                    msgstr = line[8:-1]  # Remove 'msgstr "' and '"'

                    if msgid and msgstr:
                        translations[msgid] = msgstr
                        msgid = None
                        msgstr = None

            # Erstelle .mo-Datei (vereinfacht)
            with open(mo_file_path, 'wb') as f:
                # MO file magic number
                f.write(struct.pack('<I', 0x950412de))
                # Version
                f.write(struct.pack('<I', 0))
                # Number of strings
                f.write(struct.pack('<I', len(translations)))
                # Offset of table with original strings
                f.write(struct.pack('<I', 28))
                # Offset of table with translation strings
                f.write(struct.pack('<I', 28 + len(translations) * 8))
                # Hash table size
                f.write(struct.pack('<I', 0))
                # Offset of hash table
                f.write(struct.pack('<I', 0))

                # Write string tables (simplified)
                offset = 28 + len(translations) * 16
                for msgid, msgstr in translations.items():
                    msgid_bytes = msgid.encode('utf-8')
                    msgstr_bytes = msgstr.encode('utf-8')

                    # Original string table entry
                    f.write(struct.pack('<I', len(msgid_bytes)))
                    f.write(struct.pack('<I', offset))
                    offset += len(msgid_bytes)

                for msgid, msgstr in translations.items():
                    msgstr_bytes = msgstr.encode('utf-8')

                    # Translation string table entry
                    f.write(struct.pack('<I', len(msgstr_bytes)))
                    f.write(struct.pack('<I', offset))
                    offset += len(msgstr_bytes)

                # Write actual strings
                for msgid, msgstr in translations.items():
                    f.write(msgid.encode('utf-8'))

                for msgid, msgstr in translations.items():
                    f.write(msgstr.encode('utf-8'))

            print(f"✅ Kompiliert: {po_file_path} -> {mo_file_path}")

        except Exception as e:
            print(f"❌ Fehler bei {po_file_path}: {e}")

    # Finde alle .po-Dateien
    locale_dir = Path('locale')
    if locale_dir.exists():
        for po_file in locale_dir.rglob('*.po'):
            mo_file = po_file.with_suffix('.mo')
            compile_po_file(po_file, mo_file)
    else:
        print("❌ locale/ Verzeichnis nicht gefunden")


if __name__ == '__main__':
    compile_po_to_mo()