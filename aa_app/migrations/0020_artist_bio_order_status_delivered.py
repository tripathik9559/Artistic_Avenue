from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_app', '0019_art_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='bio',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Delivered', 'Delivered')],
                default='Pending',
                max_length=50,
            ),
        ),
    ]
