# Generated by Django 4.2 on 2024-03-05 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0011_answer_down_votes_answer_up_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='bounty_amount',
            field=models.IntegerField(default=0),
        ),
    ]
