# Generated by Django 4.0.dev20210914135008 on 2021-10-20 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='auth.user'),
        ),
    ]