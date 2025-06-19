#!/usr/bin/env python3
"""
Fülle die .po-Dateien mit echten Übersetzungen
"""

import os
import struct
from pathlib import Path

# Übersetzungsmap für alle Sprachen
TRANSLATIONS = {
    # Deutsche Originaltexte -> Übersetzungen
    "Startseite": {
        "en": "Home",
        "tr": "Ana Sayfa",
        "ru": "Главная"
    },
    "Leistungen": {
        "en": "Services",
        "tr": "Hizmetler",
        "ru": "Услуги"
    },
    "Portfolio": {
        "en": "Portfolio",
        "tr": "Portföy",
        "ru": "Портфолио"
    },
    "Über uns": {
        "en": "About Us",
        "tr": "Hakkımızda",
        "ru": "О нас"
    },
    "Kalkulator": {
        "en": "Calculator",
        "tr": "Hesap Makinesi",
        "ru": "Калькулятор"
    },
    "Kontakt": {
        "en": "Contact",
        "tr": "İletişim",
        "ru": "Контакты"
    },
    "Navigation umschalten": {
        "en": "Toggle navigation",
        "tr": "Gezinmeyi değiştir",
        "ru": "Переключить навигацию"
    },
    "NovaHaus - Ihr Partner für Renovierung": {
        "en": "NovaHaus - Your Partner for Renovation",
        "tr": "NovaHaus - Renovasyon Ortağınız",
        "ru": "NovaHaus - Ваш партнер по ремонту"
    },
    "Ihr zuverlässiger Partner für professionelle Renovierung und Sanierung in Köln und Hamburg.": {
        "en": "Your reliable partner for professional renovation and refurbishment in Cologne and Hamburg.",
        "tr": "Köln ve Hamburg'da profesyonel renovasyon ve restorasyon için güvenilir ortağınız.",
        "ru": "Ваш надежный партнер по профессиональному ремонту и реставрации в Кёльне и Гамбурге."
    },
    "Navigation": {
        "en": "Navigation",
        "tr": "Navigasyon",
        "ru": "Навигация"
    },
    "Komplettrenovierung": {
        "en": "Complete Renovation",
        "tr": "Tam Renovasyon",
        "ru": "Полный ремонт"
    },
    "Badezimmersanierung": {
        "en": "Bathroom Renovation",
        "tr": "Banyo Renovasyonu",
        "ru": "Ремонт ванной"
    },
    "Fassadenreinigung": {
        "en": "Facade Cleaning",
        "tr": "Cephe Temizliği",
        "ru": "Очистка фасадов"
    },
    "Kostenrechner": {
        "en": "Cost Calculator",
        "tr": "Maliyet Hesaplayıcısı",
        "ru": "Калькулятор стоимости"
    },
    "Alle Rechte vorbehalten.": {
        "en": "All rights reserved.",
        "tr": "Tüm hakları saklıdır.",
        "ru": "Все права защищены."
    },
    "Datenschutz": {
        "en": "Privacy",
        "tr": "Gizlilik",
        "ru": "Конфиденциальность"
    },
    "Impressum": {
        "en": "Imprint",
        "tr": "Künye",
        "ru": "Выходные данные"
    },
    "Köln & Hamburg": {
        "en": "Cologne & Hamburg",
        "tr": "Köln & Hamburg",
        "ru": "Кёльн и Гамбург"
    }
}


def create_po_file(language, translations):
    """Erstelle eine .po-Datei mit Übersetzungen"""

    # Header für .po-Datei
    header = f'''# LANGUAGE translation for NovaHaus
# Copyright (C) 2024
# This file is distributed under the same license as the NovaHaus package.
#
msgid ""
msgstr ""
"Project-Id-Version: NovaHaus 1.0\\n"
"Language: {language}\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

'''

    # Übersetzungseinträge hinzufügen
    entries = []
    for german_text, translations_dict in translations.items():
        if language in translations_dict:
            translated_text = translations_dict[language]
            entry = f'''msgid "{german_text}"
msgstr "{translated_text}"

'''
            entries.append(entry)

    return header + ''.join(entries)


def create_mo_file(translations, mo_file_path):
    """Erstelle eine .mo-Datei aus Übersetzungen"""

    # Filtere leere Übersetzungen und erstelle Items
    items = [(k, v) for k, v in translations.items() if k and v and k != v]

    if not items:
        # Leere .mo-Datei für fehlende Übersetzungen
        items = [('', '')]

    # MO-Datei Struktur erstellen
    keys = [k.encode('utf-8') for k, v in items]
    values = [v.encode('utf-8') for k, v in items]

    # Offsets berechnen
    koffsets = []
    voffsets = []

    # Header ist 28 bytes + 8 bytes pro String-Paar * 2
    offset = 28 + len(items) * 16

    for key in keys:
        koffsets.append(offset)
        offset += len(key)

    for value in values:
        voffsets.append(offset)
        offset += len(value)

    # .mo-Datei schreiben
    mo_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(mo_file_path, 'wb') as f:
        # Header
        f.write(struct.pack('<I', 0x950412de))  # Magic number
        f.write(struct.pack('<I', 0))  # Version
        f.write(struct.pack('<I', len(items)))  # Number of entries
        f.write(struct.pack('<I', 28))  # Offset of key table
        f.write(struct.pack('<I', 28 + len(items) * 8))  # Offset of value table
        f.write(struct.pack('<I', 0))  # Hash table size
        f.write(struct.pack('<I', 0))  # Offset of hash table

        # Key table
        for i, key in enumerate(keys):
            f.write(struct.pack('<I', len(key)))  # Key length
            f.write(struct.pack('<I', koffsets[i]))  # Key offset

        # Value table
        for i, value in enumerate(values):
            f.write(struct.pack('<I', len(value)))  # Value length
            f.write(struct.pack('<I', voffsets[i]))  # Value offset

        # Key strings
        for key in keys:
            f.write(key)

        # Value strings
        for value in values:
            f.write(value)


def main():
    """Hauptfunktion - Erstelle alle Übersetzungsdateien"""

    print("🌍 Erstelle Übersetzungsdateien...")

    base_dir = Path(__file__).parent
    locale_dir = base_dir / 'locale'

    # Für jede Sprache Dateien erstellen
    languages = ['en', 'tr', 'ru']

    for lang in languages:
        print(f"\n📝 Erstelle {lang.upper()}-Übersetzungen...")

        lang_dir = locale_dir / lang / 'LC_MESSAGES'
        lang_dir.mkdir(parents=True, exist_ok=True)

        po_file = lang_dir / 'django.po'
        mo_file = lang_dir / 'django.mo'

        # .po-Datei erstellen
        po_content = create_po_file(lang, TRANSLATIONS)
        with open(po_file, 'w', encoding='utf-8') as f:
            f.write(po_content)
        print(f"   ✅ {po_file} erstellt")

        # Übersetzungen für .mo-Datei sammeln
        mo_translations = {}
        for german_text, translations_dict in TRANSLATIONS.items():
            if lang in translations_dict:
                mo_translations[german_text] = translations_dict[lang]

        # .mo-Datei erstellen
        create_mo_file(mo_translations, mo_file)
        print(f"   ✅ {mo_file} erstellt")

    # Deutsche Dateien (leer, da es die Standardsprache ist)
    print(f"\n📝 Erstelle DE-Übersetzungen (Standard)...")
    de_dir = locale_dir / 'de' / 'LC_MESSAGES'
    de_dir.mkdir(parents=True, exist_ok=True)

    # Leere deutsche .po-Datei
    de_po_content = '''# German (default) translation for NovaHaus
msgid ""
msgstr ""
"Language: de\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"

'''

    with open(de_dir / 'django.po', 'w', encoding='utf-8') as f:
        f.write(de_po_content)

    # Leere deutsche .mo-Datei
    create_mo_file({}, de_dir / 'django.mo')
    print(f"   ✅ Deutsche Dateien erstellt")

    print("\n🎯 FERTIG! Alle Übersetzungen erstellt.")
    print("\n🔄 Starten Sie den Django-Server neu:")
    print("   python manage.py runserver")
    print("\n🌐 Testen Sie jetzt den Sprachenwechsler!")


if __name__ == '__main__':
    main()