"""
Debug script to check if user was created correctly.
Run this in Django shell: python manage.py shell
Then: exec(open('debug_user.py').read())
"""

from student_management_app.models import CustomUser

print("=== Checking Users in Database ===\n")

users = CustomUser.objects.all()
print(f"Total users: {users.count()}\n")

for user in users:
    print(f"ID: {user.id}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"User Type: {user.user_type}")
    print(f"Is Active: {user.is_active}")
    print(f"Has usable password: {user.has_usable_password()}")
    print("-" * 40)

# Test authentication
print("\n=== Testing Authentication ===")
email = input("Enter email to test: ")
password = input("Enter password to test: ")

try:
    user_obj = CustomUser.objects.get(email=email)
    print(f"\nUser found: {user_obj.username}")
    print(f"User type: {user_obj.user_type}")
    
    # Check password
    if user_obj.check_password(password):
        print("✅ Password is CORRECT!")
    else:
        print("❌ Password is INCORRECT!")
        
except CustomUser.DoesNotExist:
    print(f"❌ No user found with email: {email}")
