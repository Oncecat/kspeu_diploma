# Generated by Django 2.1.15 on 2020-05-21 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Myip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=255, null=True, verbose_name='IP')),
                ('mac', models.CharField(max_length=255, verbose_name='MAC')),
                ('type', models.CharField(blank=True, choices=[(0, 'Динамический'), (1, 'Статический'), (2, 'Не выбрано')], default=2, max_length=255, null=True, verbose_name='Тип')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'IP',
                'verbose_name_plural': 'IP',
                'ordering': ['-id'],
            },
        ),
    ]