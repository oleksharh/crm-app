from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from rolepermissions.checkers import has_role
from rolepermissions.roles import get_user_roles

# TODO: This adapter needs to be adapted, key points are:
# 1. Redirect users to their respective dashboards based on their role.
# 2. For multiple roles, prioritize principal > teacher > student.
# 3. If no recognized role, redirect to the home page or unrecognized user page, where they can send a
# request to be approved and given a role.

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        """
        Redirects users to their respective dashboard based on their role.
        """

        user = request.user
        roles = get_user_roles(user)
        if user.is_authenticated:
            if has_role(user, 'student'):
                return reverse('student_dashboard')  # Redirect to student dashboard
            elif has_role(user, 'teacher'):
                return reverse('teacher_dashboard')  # Redirect to teacher dashboard
            elif has_role(user, 'principal'):
                return reverse('principal_dashboard')  # Redirect to principal dashboard
            else:
                return reverse('list-events')  # Default redirect for unrecognized roles
            
        return super().get_login_redirect_url(request)
    
    def get_signup_redirect_url(self, request):
        login_redirect = self.get_login_redirect_url(request)
        if login_redirect == super().get_login_redirect_url(request):
            return super().get_signup_redirect_url(request)
        
        return login_redirect
    
    def get_logout_redirect_url(self, request):
        """
        Redirects users to the same dashboard page if they are on a dashboard,
        otherwise redirects to the home page after logout.
        """
        previous_url = request.META.get('HTTP_REFERER', '')
        current_url = request.path

        if 'dashboard' in previous_url:
            return previous_url
        if 'dashboard' in current_url:
            return current_url
        
        return reverse('home')