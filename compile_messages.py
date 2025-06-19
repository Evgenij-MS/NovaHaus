# Erstellen Sie compile_messages.py:
import os
import django
from django.conf import settings
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NovaHaus.settings')
django.setup()

# Versuche Django's eigenen Compiler zu verwenden
try:
    call_command('compilemessages', verbosity=2)
    print("✅ Übersetzungen mit Django kompiliert")
except Exception as e:
    print(f"❌ Django Kompilierung fehlgeschlagen: {e}")

    # Fallback: Minimale .mo-Dateien erstellen
    import struct
    from pathlib import Path

    locale_dir = Path('locale')
    for lang in ['en', 'tr', 'ru']:
        mo_path = locale_dir / lang / 'LC_MESSAGES' / 'django.mo'
        mo_path.parent.mkdir(parents=True, exist_ok=True)

        # Erstelle leere aber gültige .mo-Datei
        with open(mo_path, 'wb') as f:
            # MO file header (minimal)
            f.write(struct.pack('<I', 0x950412de))  # Magic
            f.write(struct.pack('<I', 0))  # Version
            f.write(struct.pack('<I', 0))  # Number of strings
            f.write(struct.pack('<I', 28))  # Offset orig table
            f.write(struct.pack('<I', 28))  # Offset trans table
            f.write(struct.pack('<I', 0))  # Hash table size
            f.write(struct.pack('<I', 0))  # Offset hash table

        print(f"✅ Minimale .mo-Datei erstellt: {mo_path}")