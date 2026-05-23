from apps.project.models import (
    TestRun,
    Bug
)
from django.db.models import Count, Q
from django.db.models.functions import TruncDate


class ActivityService:

    @staticmethod
    def recent_activity():

        queryset = (

            TestRun.objects

            .exclude(
                executed_by__isnull=True
            )

            .select_related(
                "executed_by",
                "module"
            )

            .order_by("-updated_at")[:10]
        )

        response = []

        for item in queryset:

            response.append({

                "id": str(item.uuid),

                "type": item.run_status,

                "user": item.executed_by.username,

                "action": f"marked as {item.run_status}",

                "target": item.title,

                "time": item.updated_at,
            })

        return response
    

class HeatmapService:

    @staticmethod
    def module_heatmap():

        queryset = (

            TestRun.objects

            .values(
                "module__name"
            )

            .annotate(

                tests=Count("uuid"),

                failures=Count(
                    "uuid",
                    filter=Q(run_status="failed")
                )
            )
        )

        response = []

        for item in queryset:

            failure_rate = 0

            if item["tests"] > 0:

                failure_rate = round(

                    (
                        item["failures"]
                        /
                        item["tests"]
                    ) * 100,

                    2
                )

            risk = "low"

            if failure_rate >= 10:

                risk = "high"

            elif failure_rate >= 5:

                risk = "medium"

            response.append({

                "name": item[
                    "module__name"
                ],

                "tests": item["tests"],

                "failures": item["failures"],

                "rate": failure_rate,

                "risk": risk,
            })

        return response
    

    @staticmethod
    def pass_fail_distribution():

        passed = TestRun.objects.filter(
            run_status="passed"
        ).count()

        failed = TestRun.objects.filter(
            run_status="failed"
        ).count()

        return [

            {
                "name": "Passed",
                "value": passed,
                "color": "#10b981",
            },

            {
                "name": "Failed",
                "value": failed,
                "color": "#ef4444",
            }
        ]
    

class KPIService:

    @staticmethod
    def get_kpis(project_id=None):

        queryset = TestRun.objects.all()

        if project_id:

            queryset = queryset.filter(
                project_id=project_id
            )

        executed = queryset.exclude(
            run_status="not_started"
        ).count()

        passed = queryset.filter(
            run_status="passed"
        ).count()

        failed = queryset.filter(
            run_status="failed"
        ).count()

        blocked = queryset.filter(
            run_status="blocked"
        ).count()

        pass_percentage = 0

        if executed > 0:

            pass_percentage = round(
                (passed / executed) * 100,
                2
            )

        critical_failures = Bug.objects.filter(
            severity="critical"
        ).count()

        total_bugs = Bug.objects.count()

        return {

            "total_executed": executed,

            "pass_percentage": pass_percentage,

            "failed": failed,

            "blocked": blocked,

            "critical_failures": critical_failures,

            "total_bugs": total_bugs,
        }
    

class TrendService:

    @staticmethod
    def daily_execution_trend():

        queryset = (

            TestRun.objects

            .exclude(run_status="not_started")

            .annotate(
                date=TruncDate("updated_at")
            )

            .values("date")

            .annotate(

                executed=Count("uuid"),

                passed=Count(
                    "uuid",
                    filter=Q(run_status="passed")
                ),

                failed=Count(
                    "uuid",
                    filter=Q(run_status="failed")
                )
            )

            .order_by("date")
        )

        return queryset

    @staticmethod
    def failure_trend():

        queryset = (

            TestRun.objects

            .filter(run_status="failed")

            .annotate(
                date=TruncDate("updated_at")
            )

            .values("date")

            .annotate(
                failures=Count("uuid")
            )

            .order_by("date")
        )

        return queryset
    
from django.db.models import Count, Q

from apps.project.models import (
    TestRun,
    Bug
)


class ProductivityService:

    @staticmethod
    def tester_productivity():

        queryset = (

            TestRun.objects

            .exclude(
                executed_by__isnull=True
            )

            .values(
                "executed_by__id",
                "executed_by__username"
            )

            .annotate(

                executed=Count("uuid"),

                passed=Count(
                    "uuid",
                    filter=Q(run_status="passed")
                ),

                failed=Count(
                    "uuid",
                    filter=Q(run_status="failed")
                )
            )
        )

        response = []

        for item in queryset:

            pass_rate = 0

            if item["executed"] > 0:

                pass_rate = round(

                    (
                        item["passed"]
                        /
                        item["executed"]
                    ) * 100,

                    2
                )

            bugs_found = Bug.objects.filter(
                created_by_id=item[
                    "executed_by__id"
                ]
            ).count()

            productivity_score = round(

                (
                    item["executed"] * 0.4
                )
                +
                (
                    pass_rate * 0.3
                )
                +
                (
                    bugs_found * 0.3
                ),

                2
            )

            productivity = "medium"

            if productivity_score >= 150:

                productivity = "high"

            response.append({

                "name": item[
                    "executed_by__username"
                ],

                "executed": item[
                    "executed"
                ],

                "passRate": pass_rate,

                "bugs": bugs_found,

                "productivity": productivity,
            })

        return response
    
    @staticmethod
    def risky_modules():

        queryset = (

            TestRun.objects

            .values(
                "module__name"
            )

            .annotate(

                failures=Count(
                    "uuid",
                    filter=Q(run_status="failed")
                ),

                total=Count("uuid")
            )
        )

        response = []

        for item in queryset:

            failure_rate = 0

            if item["total"] > 0:

                failure_rate = round(

                    (
                        item["failures"]
                        /
                        item["total"]
                    ) * 100,

                    2
                )

            severity = "medium"

            if failure_rate >= 10:

                severity = "critical"

            elif failure_rate >= 5:

                severity = "high"

            response.append({

                "module": item[
                    "module__name"
                ],

                "failures": item[
                    "failures"
                ],

                "failureRate": failure_rate,

                "severity": severity,
            })

        return response