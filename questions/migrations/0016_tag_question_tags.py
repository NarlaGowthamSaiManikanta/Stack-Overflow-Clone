# Generated by Django 4.2 on 2024-03-05 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0015_remove_question_tags_delete_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, to='questions.tag'),
        ),
    ]
