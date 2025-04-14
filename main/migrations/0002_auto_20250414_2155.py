from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='Portfolio',
            name='panorama_image',
            field=models.ImageField(upload_to='portfolio/panorama/', blank=True, null=True, verbose_name='Панорамное изображение'),
        ),
    ]