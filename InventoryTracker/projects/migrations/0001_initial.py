# Generated by Django 3.0.4 on 2020-03-14 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(help_text='Name of this project', max_length=128)),
                ('Description', models.TextField(help_text='Description for this project')),
            ],
            options={
                'verbose_name': 'Project',
            },
        ),
        migrations.CreateModel(
            name='ProjectPartModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField(help_text='Quantity of parts required')),
                ('Part', models.ForeignKey(help_text='Part required', on_delete=django.db.models.deletion.CASCADE, to='inventory.PartModel')),
                ('Project', models.ForeignKey(help_text='Project this part is required for', on_delete=django.db.models.deletion.CASCADE, to='projects.ProjectModel')),
            ],
            options={
                'verbose_name': 'Project Part',
                'unique_together': {('Part', 'Project')},
            },
        ),
        migrations.CreateModel(
            name='BOMDesignatorModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.IntegerField(help_text='Numeric part of the designator')),
                ('Letter', models.CharField(help_text='Letter part of the designator', max_length=2)),
                ('PartModel', models.ForeignKey(help_text='Project part this designator is applied to', on_delete=django.db.models.deletion.CASCADE, to='projects.ProjectPartModel')),
            ],
            options={
                'verbose_name': 'Part Designator',
            },
        ),
        migrations.AddConstraint(
            model_name='bomdesignatormodel',
            constraint=models.UniqueConstraint(fields=('Number', 'Letter', 'PartModel'), name='BOMNumberLetterPartConstrant'),
        ),
        migrations.AddConstraint(
            model_name='bomdesignatormodel',
            constraint=models.CheckConstraint(check=models.Q(Number__gte=0), name='BOMNumbergte0'),
        ),
    ]
