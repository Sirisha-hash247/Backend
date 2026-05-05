import uuid
from django.db import models
from apps.users.models import User
from core.models import BaseModel


from apps.users.models import Organization 

class Project(BaseModel):

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('completed', 'Completed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    def __str__(self):
        return self.title

class Module(BaseModel):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=255)

class Screen(BaseModel):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='screens')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class TestCase(BaseModel):

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    TYPE_CHOICES = (
        ('smoke', 'Smoke Testing'),
        ('functional', 'Functional Testing'),
        ('non_functional', 'Non-Functional Testing'),
        ('regression', 'Regression Testing'),
        ('integration', 'Integration Testing'),
        ('system', 'System Testing'),
        ('acceptance', 'Acceptance Testing'),
        ('performance', 'Performance Testing'),
        ('security', 'Security Testing'),
        ('usability', 'Usability Testing'),
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='testcases')

    title = models.CharField(max_length=255)
    description = models.TextField()
    expected_results = models.TextField()

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    type_of_testcase = models.CharField(max_length=30, choices=TYPE_CHOICES)

    # 🔥 ADD THIS
    steps = models.JSONField(null=True, blank=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_testcases'
    )
class TestRun(BaseModel):

    STATUS_CHOICES = (
        ('pass', 'Pass'),
        ('fail', 'Fail'),
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    test_case = models.ForeignKey(
        TestCase,
        on_delete=models.CASCADE,
        related_name='test_runs'
    )

    actual_results = models.TextField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    executed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    executed_at = models.DateTimeField(auto_now_add=True)
    
class Bug(BaseModel):

    SEVERITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bugs')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='bugs')
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='bugs')

    test_case = models.ForeignKey(
        TestCase,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bugs'
    )

    # optional (since you didn’t define model for it)
    test_cycle_id = models.UUIDField(null=True, blank=True)

    description = models.TextField()
    steps_to_reproduce = models.TextField()

    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES) 
    expected_results = models.TextField()
    actual_results = models.TextField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

    screenshot_id = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return self.description[:50]