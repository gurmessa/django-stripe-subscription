from django_registration.forms import RegistrationForm
from accounts.models import User


class UserRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User