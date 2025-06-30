from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from rolepermissions.checkers import has_role

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        """
        Redirects users to their respective dashboard based on their role.
        """

        user = request.user
        if user.is_authenticated:
            if has_role(user, 'student'):
                return reverse('student_dashboard')  # Redirect to student dashboard
            elif has_role(user, 'teacher'):
                return reverse('teacher_dashboard')  # Redirect to teacher dashboard
            elif has_role(user, 'principal'):
                return reverse('principal_dashboard')  # Redirect to principal dashboard
            else:
                return reverse('/')  # Default redirect for unrecognized roles
            
        return super().get_login_redirect_url(request)
    
    def get_logout_redirect_url(self, request):
        """
        Redirects users to the same dashboard page if they are on a dashboard,
        otherwise redirects to the home page after logout.
        """
        previous_url = request.META.get('HTTP_REFERER', '')
        current_url = request.path

        # Prefer previous_url if it contains 'dashboard', else check current_url
        if 'dashboard' in previous_url:
            return previous_url
        if 'dashboard' in current_url:
            return current_url
        
        return reverse('')