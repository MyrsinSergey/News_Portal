# Generated by Django 4.1.7 on 2023-04-19 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_category_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='topics',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]