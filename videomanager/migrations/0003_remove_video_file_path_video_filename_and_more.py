# Generated by Django 5.0.2 on 2024-03-10 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videomanager', '0002_playlistsource_rename_channelid_channel_channel_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='file_path',
        ),
        migrations.AddField(
            model_name='video',
            name='filename',
            field=models.CharField(default='', max_length=110),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(),
        ),
    ]
