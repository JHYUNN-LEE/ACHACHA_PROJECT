# Generated by Django 4.1.1 on 2022-09-22 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acha_money', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDeal',
            fields=[
                ('deal_id', models.AutoField(primary_key=True, serialize=False)),
                ('users_id', models.CharField(max_length=45)),
                ('posts_id', models.IntegerField()),
                ('deal', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'user_deal',
                'managed': False,
            },
        ),
    ]
