# Generated by Django 3.1.5 on 2021-02-27 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_delete_search'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(db_index=True, max_length=30)),
                ('reciever', models.CharField(db_index=True, max_length=30)),
                ('amount', models.IntegerField(default=0)),
                ('sender_id', models.CharField(db_index=True, max_length=30)),
                ('reciever_id', models.CharField(db_index=True, max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
    ]