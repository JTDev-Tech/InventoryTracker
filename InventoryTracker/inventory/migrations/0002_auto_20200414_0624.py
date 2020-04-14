# Generated by Django 3.0.4 on 2020-04-14 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='containermodel',
            options={'verbose_name': 'Container'},
        ),
        migrations.AlterModelOptions(
            name='packagemodel',
            options={'verbose_name': 'Footprint'},
        ),
        migrations.AlterModelOptions(
            name='partattrmodel',
            options={'verbose_name': 'Part Attribute'},
        ),
        migrations.AlterModelOptions(
            name='partcategorymodel',
            options={'verbose_name': 'Part Category'},
        ),
        migrations.AlterModelOptions(
            name='partcountmodel',
            options={'verbose_name': 'Part Count'},
        ),
        migrations.AlterModelOptions(
            name='partmodel',
            options={'verbose_name': 'Part'},
        ),
        migrations.AlterModelOptions(
            name='shelfmodel',
            options={'verbose_name': 'Shelf'},
        ),
        migrations.AddField(
            model_name='partmodel',
            name='PreviewImage',
            field=models.ImageField(blank=True, help_text='Preview image for this part', null=True, upload_to='preview_img/%m/'),
        ),
    ]