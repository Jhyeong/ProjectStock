# Generated by Django 3.0.1 on 2019-12-29 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_crawling_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crawling_data',
            name='news_date',
        ),
        migrations.AddField(
            model_name='crawling_data',
            name='current_price',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='crawling_data',
            name='current_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='crawling_data',
            name='indecrease_amount',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='crawling_data',
            name='indecrease_percent',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
