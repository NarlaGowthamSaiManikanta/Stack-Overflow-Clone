# Generated by Django 4.2 on 2024-03-03 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_alter_question_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='id',
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
