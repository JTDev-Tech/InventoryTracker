# Generated by Django 3.0.4 on 2020-03-11 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200310_1223'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectmodel',
            options={'verbose_name': 'Project'},
        ),
        migrations.AlterModelOptions(
            name='projectpartmodel',
            options={'verbose_name': 'Project Part'},
        ),
        migrations.AlterUniqueTogether(
            name='projectpartmodel',
            unique_together={('Part', 'Project')},
        ),
        migrations.CreateModel(
            name='BOMDesignatorModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.IntegerField(help_text='Numeric part of the designator')),
                ('Letter', models.CharField(help_text='Letter part of the designator', max_length=2)),
                ('PartModel', models.ForeignKey(help_text='Project part this designator is applied to', on_delete=django.db.models.deletion.CASCADE, to='app.ProjectPartModel')),
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
