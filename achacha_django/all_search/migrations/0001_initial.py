
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('alarm_id', models.AutoField(primary_key=True, serialize=False)),
                ('users_id', models.CharField(blank=True, max_length=45, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('category', models.CharField(blank=True, max_length=45, null=True)),
                ('src', models.CharField(blank=True, max_length=100, null=True)),
                ('turn', models.CharField(blank=True, max_length=2, null=True)),
            ],
            options={
                'db_table': 'alarm',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LostItems',
            fields=[
                ('lost_items_id_pk', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('get_name', models.CharField(blank=True, max_length=150, null=True)),
                ('get_at', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=45, null=True)),
                ('get_time', models.CharField(blank=True, max_length=45, null=True)),
                ('get_place', models.CharField(blank=True, max_length=45, null=True)),
                ('category', models.CharField(blank=True, max_length=45, null=True)),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('find_place', models.CharField(blank=True, max_length=45, null=True)),
                ('pickup_check', models.CharField(blank=True, max_length=10, null=True)),
                ('center_number', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'lost_items',
                'managed': False,
            },
        ),
    ]
