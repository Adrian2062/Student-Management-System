"""
Run this script to clean up duplicate users in the database.

Usage:
    python manage.py shell < cleanup_duplicates.py

Or run in Django shell:
    python manage.py shell
    exec(open('cleanup_duplicates.py').read())
"""

from student_management_app.models import CustomUser

# Find and remove duplicate users
emails = CustomUser.objects.values('email').annotate(count=models.Count('email')).filter(count__gt=1)

for email_dict in emails:
    email = email_dict['email']
    users = CustomUser.objects.filter(email=email).order_by('id')
    
    # Keep the first user, delete the rest
    users_to_delete = users[1:]
    
    print(f"Found {users.count()} users with email: {email}")
    print(f"Keeping user ID: {users.first().id}, Username: {users.first().username}")
    
    for user in users_to_delete:
        print(f"Deleting user ID: {user.id}, Username: {user.username}")
        user.delete()

print("\nCleanup complete!")
