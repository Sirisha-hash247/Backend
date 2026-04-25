
class Roles:
    SUPER_ADMIN = "superadmin"
    ADMIN = "admin"
    TESTER = "tester"
    REVIEWER = "reviewer"

    CHOICES = (
        (SUPER_ADMIN, "Super Admin"),
        (ADMIN, "Admin"),
        (TESTER, "Tester"),
        (REVIEWER, "Reviewer"),
    )