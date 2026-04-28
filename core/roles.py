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


ROLE_ROUTES = {
    "superadmin": {
        "projects": ["create", "read", "update", "delete"],
        "modules": ["create", "read", "update", "delete"],
        "screens": ["create", "read", "update", "delete"],
        "testcases": ["create", "read", "update", "delete"],
        "bugs": ["create", "read", "update", "delete"],
        "testruns": ["create", "read", "update"],
    },
    
    
    
    
    
  
    "admin": {
        "projects": ["create", "read", "update", "delete"],
        "modules": ["create", "read", "update", "delete"],
        "screens": ["create", "read", "update", "delete"],
        "testcases": ["create", "read", "update", "delete"],
        "bugs": ["create", "read", "update", "delete"],
        "testruns": ["create", "read", "update"],
    },

    "tester": {
        "projects": ["read"],  
        "modules": ["create","read","update"],
        "screens": ["create","read","update"],
        "testcases": ["create", "read", "update"],
        "bugs": ["create", "read", "update", "delete"],
        "testruns":["create","read","update"],
    },

    "reviewer": {
        "projects": ["read"],
        "modules": ["read"],
        "screens": ["read"],
        "testcases": ["read"],
        "bugs": ["read", "update"],  # can update status maybe
        "testruns": ["read","update"],
    }
}