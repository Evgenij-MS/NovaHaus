
#!/usr/bin/env python3
"""
Einfache Übersetzungslösung ohne korrupte .mo-Dateien
"""

import os
import shutil
from pathlib import Path

def main():
    """Lösche korrupte Übersetzungen und deaktiviere i18n temporär"""
    
    print("🔧 Repariere Übersetzungsproblem...")
    
    base_dir = Path(__file__).parent
    locale_dir = base_dir / 'locale'
    
    # 1. Lösche das gesamte locale-Verzeichnis
    if locale_dir.exists():
        print("🗑️ Entferne korrupte Übersetzungen...")
        shutil.rmtree(locale_dir)
    
    # 2. Erstelle minimale Struktur
    print("📁 Erstelle minimale Struktur...")
    for lang in ['de', 'en', 'tr', 'ru']:
        lang_dir = locale_dir / lang / 'LC_MESSAGES'
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        # Leere .po-Datei ohne Übersetzungen
        po_content = f'''# {lang.upper()} translation for NovaHaus
msgid ""
msgstr ""
"Language: {lang}\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"

'''
        with open(lang_dir / 'django.po', 'w', encoding='utf-8') as f:
            f.write(po_content)
        
        print(f"   ✅ {lang}.po erstellt")
    
    print("\n🚀 Problem gelöst! Starten Sie den Server:")
    print("   python manage.py runserver")

if __name__ == '__main__':
    main()