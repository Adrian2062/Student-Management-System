
import os
import time

BASE_DIR = r"c:\Users\AcerPredator\Desktop\django pw broadway\student_management_app\templates\hod_template"

files_to_delete = [
    "add_student_template.html",
    "add_student_template_v2.html",
    "edit_student_template.html",
    "edit_student_template_v2.html",
    "edit_student_template_v3.html",
    "manage_student_template.html",
    "manage_student_template_v2.html",
]

files_to_rename = {
    "add_student_template_v4.txt": "add_student_template.html",
    "edit_student_template_v4.txt": "edit_student_template.html",
    "manage_student_template_v4.txt": "manage_student_template.html",
}

print("Starting cleanup...")

for filename in files_to_delete:
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            print(f"Deleted: {filename}")
        except Exception as e:
            print(f"Error deleting {filename}: {e}")
    else:
        print(f"File not found (already gone): {filename}")

time.sleep(1)

for src, dst in files_to_rename.items():
    src_path = os.path.join(BASE_DIR, src)
    dst_path = os.path.join(BASE_DIR, dst)
    
    if os.path.exists(src_path):
        # Ensure destination doesn't exist (we tried to delete it above, but just in case)
        if os.path.exists(dst_path):
            try:
                os.remove(dst_path)
                print(f"Removed existing destination: {dst}")
            except Exception as e:
                print(f"Error removing existing destination {dst}: {e}")
        
        try:
            os.rename(src_path, dst_path)
            print(f"Renamed: {src} -> {dst}")
        except Exception as e:
            print(f"Error renaming {src} -> {dst}: {e}")
    else:
        print(f"Source file not found: {src}")

print("Cleanup script finished.")
