from rest_framework import serializers
from .models import Project, Module, Screen
from .models import TestCase
from .models import Bug



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
            'created_by', 'updated_by', 'deleted_by',
            'created_at', 'updated_at', 'deleted_at'
        ]

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'
        read_only_fields = [
            'created_by', 'updated_by', 'deleted_by',
            'created_at', 'updated_at', 'deleted_at'
        ]

class BugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bug
        fields = '__all__'
        read_only_fields = [
            'created_by', 'updated_by', 'deleted_by',
            'created_at', 'updated_at', 'deleted_at'
        ]