from rolepermissions.roles import AbstractUserRole

class Student(AbstractUserRole):
    available_permissions = {
        'view_schedule': True, # Students can view their own schedule, not really necessary as they have that in google calendar anyway, but let's keep it for consistency
        'view_attendance': True, # Shows their own attendance records coupled with billing
        'view_billing': True, # Students can view their own billing records
    }
    

class Teacher(AbstractUserRole):
    available_permissions = {
        'crud_schedule': True, # Teachers can create, read, update, and delete schedules
        'crud_attendance': True, # Teachers can view attendance records
        'crud_billing': True, # Teachers can view and manage billing records
    }
    

class Principal(AbstractUserRole):
    available_permissions = {
        'crud_schedule': True, # Principals can create, read, update, and delete schedules
        'crud_attendance': True, # Principals can view attendance records
        'crud_billing': True, # Principals can view and manage billing records
        'manage_teachers': True, # Principals can manage teachers, NOTE: maybe allow them to change permissions?
        'manage_students': True, # Principals can manage students
    }