# Generated by Django 4.2.5 on 2023-12-04 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0005_course_price_lesson_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]