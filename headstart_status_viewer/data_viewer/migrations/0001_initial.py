# Generated by Django 4.2.1 on 2023-10-30 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('method', models.CharField(choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')], max_length=10)),
                ('path', models.CharField(max_length=100)),
                ('params', models.CharField(max_length=100)),
                ('status_code', models.IntegerField()),
                ('ip', models.CharField(default='', max_length=15)),
                ('device', models.CharField(default='', max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
