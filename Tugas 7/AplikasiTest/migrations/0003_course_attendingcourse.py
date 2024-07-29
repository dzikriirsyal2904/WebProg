# Generated by Django 5.0.4 on 2024-07-29 16:18

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AplikasiTest', '0002_rename_aplikasites_account_e4b5b9_idx_aplikasites_account_6857fe_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.UUIDField(default=uuid.UUID('e39b8ff6-7045-452e-aec0-251e4a471c43'), editable=False, primary_key=True, serialize=False, unique=True)),
                ('course_name', models.CharField(editable=False, max_length=255)),
                ('course_created_by', models.CharField(max_length=255)),
                ('course_created_date', models.DateTimeField(auto_now_add=True)),
                ('course_updated_by', models.CharField(max_length=255, null=True)),
                ('course_updated_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('course_id',),
                'indexes': [models.Index(fields=['course_id'], name='AplikasiTes_course__f62a9b_idx')],
            },
        ),
        migrations.CreateModel(
            name='AttendingCourse',
            fields=[
                ('attending_course_id', models.UUIDField(default=uuid.UUID('1788646a-b93b-4a75-b76d-72ac15b062f0'), editable=False, primary_key=True, serialize=False, unique=True)),
                ('attending_account_profile_id', models.CharField(editable=False, max_length=255)),
                ('attending_course_created_by', models.CharField(max_length=255)),
                ('attending_course_created_date', models.DateTimeField(auto_now_add=True)),
                ('attending_course_updated_by', models.CharField(max_length=255, null=True)),
                ('attending_course_updated_date', models.DateTimeField(auto_now_add=True)),
                ('attending_courseid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AplikasiTest.course')),
            ],
            options={
                'ordering': ('attending_course_id',),
                'indexes': [models.Index(fields=['attending_course_id', 'attending_courseid'], name='AplikasiTes_attendi_6a69c9_idx')],
            },
        ),
    ]