# Generated migration for S8: CaseRecord model

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='case_records/%Y/%m/')),
                ('original_filename', models.CharField(max_length=255)),
                ('mime_type', models.CharField(max_length=100)),
                ('file_size', models.PositiveIntegerField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='cases.case')),
            ],
            options={
                'db_table': 'CaseRecord',
            },
        ),
    ]
