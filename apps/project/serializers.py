from rest_framework import serializers
from .models import Project, Module, Screen
from .models import TestCase
from .models import Bug
from .models import TestRun



class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = '__all__'
        read_only_fields = [
            'created_by', 'updated_by', 'deleted_by',
            'created_at', 'updated_at', 'deleted_at'
        ]


class ModuleSerializer(serializers.ModelSerializer):
    screens = ScreenSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = '__all__'
        read_only_fields = [
            'created_by', 'updated_by', 'deleted_by',
            'created_at', 'updated_at', 'deleted_at'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

        read_only_fields = [
            'organization',  
            'created_by',
            'updated_by',
            'deleted_by',
            'created_at',
            'updated_at',
            'deleted_at'
        ]

class TestCaseSerializer(serializers.ModelSerializer):

    steps = serializers.JSONField(required=False)

    class Meta:
        model = TestCase
        fields = '__all__'
        read_only_fields = [
            'created_by', 'updated_by', 'deleted_by',
            'created_at', 'updated_at', 'deleted_at'
        ]

    def validate_steps(self, value):
        """
        Convert list → {step 1: ..., step 2: ...}
        """
        if isinstance(value, list):
            return {
                f"step {i+1}": step
                for i, step in enumerate(value)
                if step.strip() != ""
            }
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Ensure steps always returned in required format
        if isinstance(instance.steps, dict):
            data["steps"] = instance.steps

        return data

class BugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bug
        fields = '__all__'
        read_only_fields = [
            'created_by', 'updated_by', 'deleted_by',
            'created_at', 'updated_at', 'deleted_at'
        ]


from rest_framework import serializers
from apps.project.models import TestRun


class TestRunSerializer(serializers.ModelSerializer):

    # 🔹 Readable fields
    test_case_title = serializers.CharField(source="test_case.title", read_only=True)
    executed_by_name = serializers.CharField(source="executed_by.email", read_only=True)

    class Meta:
        model = TestRun
        fields = [
            "uuid",
            "test_case",
            "test_case_title",
            "actual_results",
            "status",
            "executed_by",
            "executed_by_name",
            "executed_at",
        ]
        read_only_fields = ["uuid", "executed_by", "executed_at"]
        
        
# ✅ CREATE SERIALIZER FOR SWAGGER
class BulkTestCaseSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    expected_results = serializers.CharField()
    priority = serializers.CharField()
    status = serializers.CharField()
    screen = serializers.CharField()

