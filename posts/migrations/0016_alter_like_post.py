# Generated by Django 4.0.4 on 2022-07-18 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_alter_like_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to='posts.post'),
        ),
    ]
