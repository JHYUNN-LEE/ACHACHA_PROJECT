# Generated by Django 3.2.15 on 2022-09-20 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authentication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=30, verbose_name='휴대폰 번호')),
                ('auth_number', models.CharField(max_length=30, verbose_name='인증번호')),
            ],
            options={
                'verbose_name_plural': '휴대폰인증 관리 페이지',
                'db_table': 'authentications',
            },
        ),
    ]
