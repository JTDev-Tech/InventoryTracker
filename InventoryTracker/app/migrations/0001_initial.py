# Generated by Django 3.0.4 on 2020-03-10 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PackageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(help_text='Name of this package', max_length=256, unique=True)),
                ('Reference', models.URLField(help_text='Link to reference documentation for this parts package')),
            ],
        ),
        migrations.CreateModel(
            name='PartAttrModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(help_text='Name assigned to this attribute', max_length=256)),
                ('Value', models.CharField(help_text='Value of this attribute', max_length=256)),
            ],
            options={
                'unique_together': {('Name', 'Value')},
            },
        ),
        migrations.CreateModel(
            name='PartCategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CategoryName', models.CharField(help_text='Name of this part classification', max_length=256)),
                ('Parent', models.ForeignKey(blank=True, help_text='Parent category, if any', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.PartCategoryModel')),
            ],
            options={
                'unique_together': {('CategoryName', 'Parent')},
            },
        ),
        migrations.CreateModel(
            name='ShelfModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=256)),
                ('LocationID', models.CharField(help_text='User assigned location ID for this shelf', max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PartModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(help_text='Name of the electronic part', max_length=256)),
                ('Value', models.IntegerField(blank=True, help_text='Value for this part', null=True)),
                ('MfgPartNumber', models.CharField(blank=True, help_text='Manufactorers part number for this part', max_length=128)),
                ('UnitID', models.IntegerField(blank=True, null=True)),
                ('DataSheet', models.FileField(blank=True, help_text='Datasheet for this part', null=True, upload_to='data_sheets/%m/')),
                ('Attributes', models.ManyToManyField(blank=True, help_text='Part this attribute is assigned to', to='app.PartAttrModel')),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.PartCategoryModel')),
                ('Package', models.ForeignKey(help_text='Package of this part', on_delete=django.db.models.deletion.CASCADE, to='app.PackageModel')),
            ],
            options={
                'unique_together': {('Value', 'UnitID')},
            },
        ),
        migrations.CreateModel(
            name='ContainerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=256)),
                ('LocationID', models.CharField(help_text='User assigned location ID for this container', max_length=32)),
                ('Shelf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ShelfModel')),
            ],
            options={
                'unique_together': {('LocationID', 'Shelf'), ('LocationID', 'Name')},
            },
        ),
        migrations.CreateModel(
            name='PartCountModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField(help_text='Part quantity')),
                ('Location', models.ForeignKey(help_text='Location of these parts', on_delete=django.db.models.deletion.CASCADE, to='app.ContainerModel')),
                ('Part', models.ForeignKey(help_text='Part this count is for', on_delete=django.db.models.deletion.CASCADE, to='app.PartModel')),
            ],
            options={
                'unique_together': {('Location', 'Part')},
            },
        ),
    ]
