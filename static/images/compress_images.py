from PIL import Image
import os
import argparse
from concurrent.futures import ThreadPoolExecutor


def parse_args():
    parser = argparse.ArgumentParser(description='Оптимизатор изображений 2.0')
    parser.add_argument('--quality-jpeg', type=int, default=70, help='Качество для JPEG (0-100)')
    parser.add_argument('--quality-webp', type=int, default=80, help='Качество для WebP (0-100)')
    parser.add_argument('--keep-original', action='store_false', help='Не удалять оригиналы после конвертации')
    parser.add_argument('--backup', action='store_true', help='Создавать резервные копии оригиналов')
    parser.add_argument('--threads', type=int, default=4, help='Количество потоков для обработки')
    return parser.parse_args()


def optimize_image(path, quality_jpeg, quality_webp, keep_original, backup_dir):
    try:
        with Image.open(path) as img:
            # Создаём резервную копию при необходимости
            if backup_dir:
                backup_path = os.path.join(backup_dir, os.path.basename(path))
                img.save(backup_path)
                print(f"✓ Создана резервная копия: {backup_path}")

            # Оптимизация оригинального формата
            if path.lower().endswith(('.jpg', '.jpeg')):
                img.save(path, quality=quality_jpeg, optimize=True, progressive=True)
                print(f"✓ Оптимизирован JPEG: {path}")
            elif path.lower().endswith('.png'):
                img.save(path, optimize=True, compress_level=9)
                print(f"✓ Оптимизирован PNG: {path}")

            # Конвертация в WebP
            webp_path = os.path.splitext(path)[0] + ".webp"
            if not os.path.exists(webp_path):
                img.save(webp_path, format='webp', quality=quality_webp, method=6)
                print(f"✓ Конвертировано в WebP: {webp_path}")

            # Удаление оригинала при необходимости
            if not keep_original and os.path.exists(webp_path):
                os.remove(path)
                print(f"🗑 Удалён оригинал: {path}")

    except Exception as e:
        print(f"✗ Ошибка обработки {path}: {str(e)}")
        return str(e)
    return None


def process_images(arguments):
    image_dir = "static/images/"
    backup_dir = os.path.join(image_dir, "backups") if arguments.backup else None

    if backup_dir and not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    tasks = []
    for root, _, files in os.walk(image_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(root, file)
                tasks.append(
                    (path, arguments.quality_jpeg, arguments.quality_webp, arguments.keep_original, backup_dir))

    with ThreadPoolExecutor(max_workers=arguments.threads) as executor:
        results = executor.map(lambda p: optimize_image(*p), tasks)

    error_count = sum(1 for res in results if res is not None)
    print(f"\nОбработка завершена! Ошибок: {error_count}")


if __name__ == "__main__":
    config = parse_args()
    print("=== Запуск Image Optimizer 2.0 ===")
    print(f"• Потоков: {config.threads}")
    print(f"• Качество JPEG: {config.quality_jpeg}")
    print(f"• Качество WebP: {config.quality_webp}")
    print(f"• Резервные копии: {'Да' if config.backup else 'Нет'}")
    print(f"• Удаление оригиналов: {'Нет' if config.keep_original else 'Да'}\n")

    process_images(config)
    print("\n=== Работа завершена! ===")