# Generated by Django 4.2 on 2024-03-05 05:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0009_answer_saved_by_question_saved_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='down_votes',
            field=models.ManyToManyField(blank=True, related_name='down_votes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='up_votes',
            field=models.ManyToManyField(blank=True, related_name='up_votes', to=settings.AUTH_USER_MODEL),
        ),
    ]
