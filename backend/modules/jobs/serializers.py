from rest_framework import serializers


class JobSearchSerializer(serializers.Serializer):
    salary_min = serializers.IntegerField(required=False, min_value=0)
    salary_max = serializers.IntegerField(required=False, min_value=0)
    job_type = serializers.CharField(required=False, allow_blank=True)
    work_time = serializers.CharField(required=False, allow_blank=True)
    education = serializers.CharField(required=False, allow_blank=True)
    region = serializers.CharField(required=False, allow_blank=True)
    page = serializers.IntegerField(required=False, min_value=1, default=1)
    page_size = serializers.IntegerField(required=False, min_value=1, max_value=50, default=20)


class AnalyzeSerializer(serializers.Serializer):
    mode = serializers.CharField(required=False, default="skills_summary")
    language = serializers.CharField(required=False, default="zh")
    cache = serializers.BooleanField(required=False, default=True)
