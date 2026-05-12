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

    screen = models.ForeignKey(
        Screen,
        on_delete=models.CASCADE,
        related_name='testcases'
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    expected_results = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    type_of_testcase = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES
    )

    steps = models.JSONField(null=True, blank=True)

    display_order = models.PositiveIntegerField(default=0)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_testcases'
    )


class TestRunVersion(BaseModel):

    VERSION_STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='test_run_versions'
    )

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='test_run_versions'
    )

    screen = models.ForeignKey(
        Screen,
        on_delete=models.CASCADE,
        related_name='test_run_versions'
    )

    version_number = models.CharField(
        max_length=50
    )

    version_status = models.CharField(
        max_length=20,
        choices=VERSION_STATUS,
        default='draft'
    )

    notes = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.version_number
    

class TestRun(BaseModel):

    RUN_STATUS = (
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('blocked', 'Blocked'),
    )

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='testruns'
    )

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='testruns'
    )

    screen = models.ForeignKey(
        Screen,
        on_delete=models.CASCADE,
        related_name='testruns'
    )

    version = models.ForeignKey(
        TestRunVersion,
        on_delete=models.CASCADE,
        related_name='testruns'
    )

    testcase = models.ForeignKey(
        TestCase,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testruns'
    )

    # SNAPSHOT DATA

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    expected_results = models.TextField()

    steps = models.JSONField(
        null=True,
        blank=True
    )

    priority = models.CharField(
        max_length=20
    )

    type_of_testcase = models.CharField(
        max_length=30
    )

    display_order = models.PositiveIntegerField(default=0)

    # EXECUTION DATA

    run_status = models.CharField(
        max_length=20,
        choices=RUN_STATUS,
        default='not_started'
    )

    actual_result = models.TextField(
        null=True,
        blank=True
    )

    notes = models.TextField(
        null=True,
        blank=True
    )

    executed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='executed_test_runs'
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title
    
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

    testcase = models.ForeignKey(
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
    actual_result = models.TextField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

    screenshot_id = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return self.description[:50]