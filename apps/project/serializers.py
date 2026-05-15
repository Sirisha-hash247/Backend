from rest_framework import serializers
from .models import Project, Module, Screen
from .models import TestCase
from .models import Bug
from .models import TestRun, TestRunVersion



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

    # =====================================================
    # READABLE FIELDS
    # =====================================================

    testcase_title = serializers.CharField(
        source="testcase.title",
        read_only=True
    )

    executed_by_name = serializers.CharField(
        source="executed_by.email",
        read_only=True
    )

    version_number = serializers.CharField(
        source="version.version_number",
        read_only=True
    )

    class Meta:

        model = TestRun

        fields = [

            # IDs

            "uuid",

            "project",
            "module",
            "screen",

            "version",
            "version_number",

            "testcase",
            "testcase_title",

            # SNAPSHOT DATA

            "title",
            "description",
            "expected_results",
            "steps",

            "priority",
            "type_of_testcase",
            "display_order",

            # EXECUTION DATA

            "run_status",
            "actual_result",
            "notes",

            "executed_by",
            "executed_by_name",

            "started_at",
            "completed_at",

            # ACTIVITY TRACKING

            "created_at",
            "updated_at",

            "created_by",
            "updated_by",
        ]

        read_only_fields = [

            "uuid",

            "created_at",
            "updated_at",

            "created_by",
            "updated_by",

            "executed_by",

            "started_at",
            "completed_at",
        ]

class TestRunVersionSerializer(serializers.ModelSerializer):
    total_executions = serializers.SerializerMethodField()

    def get_total_executions(self, obj):

         return obj.testruns.exclude(
        run_status="not_started"
    ).count()


    class Meta:

        model = TestRunVersion

        fields = [

            # ============================================
            # SYSTEM FIELDS
            # ============================================

            "uuid",

            "created_at",
            "updated_at",

            "created_by",
            "updated_by",

            "deleted_at",
            "deleted_by",

            # ============================================
            # VERSION DATA
            # ============================================

            "project",
            "module",
            "screen",

            "version_number",
            "version_status",
            "notes",
            "total_executions",
        ]

        read_only_fields = [

            # SYSTEM GENERATED

            "uuid",

            "project",
            "module",

            "created_at",
            "updated_at",

            "created_by",
            "updated_by",

            "deleted_at",
            "deleted_by",
        ]
        
        
# ✅ CREATE SERIALIZER FOR SWAGGER
class BulkTestCaseSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    expected_results = serializers.CharField()
    priority = serializers.CharField()
    status = serializers.CharField()
    screen = serializers.CharField()

