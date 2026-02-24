# Generated manually for bootstrap
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='JobNormalized',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('job_id', models.CharField(db_index=True, max_length=64, unique=True)),
                ('source', models.CharField(max_length=64)),
                ('source_job_id', models.CharField(blank=True, default='', max_length=128)),
                ('source_url', models.URLField(blank=True, default='', max_length=500)),
                ('title', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=200)),
                ('salary_text', models.CharField(blank=True, default='', max_length=100)),
                ('region', models.CharField(blank=True, default='', max_length=100)),
                ('jd', models.TextField(blank=True, default='')),
                ('tags', models.JSONField(default=list)),
                ('publish_time', models.DateField(blank=True, null=True)),
                ('extra', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'indexes': [
                    models.Index(fields=['source', 'source_job_id'], name='modules_job_source_b43b6d_idx'),
                    models.Index(fields=['title', 'company'], name='modules_job_title_64db6c_idx')
                ],
                'constraints': [
                    models.UniqueConstraint(fields=('source', 'source_job_id'), name='uniq_source_source_job_id')
                ],
            },
        ),
        migrations.CreateModel(
            name='JobAnalysisCache',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cache_key', models.CharField(max_length=128, unique=True)),
                ('model_name', models.CharField(blank=True, default='', max_length=128)),
                ('payload', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analysis', to='jobs.jobnormalized')),
            ],
            options={'indexes': [models.Index(fields=['job', 'updated_at'], name='modules_job_job_id_cb57ab_idx')]},
        ),
    ]
