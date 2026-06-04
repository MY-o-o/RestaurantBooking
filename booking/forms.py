from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class AuthFieldStylingMixin:
    input_class = 'auth-input'

    def _apply_common_attrs(self):
        for name, field in self.fields.items():
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_class} {self.input_class}'.strip()
            field.widget.attrs.setdefault('autocomplete', name)


class StyledAuthenticationForm(AuthFieldStylingMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_common_attrs()
        self.fields['username'].widget.attrs.update({
            'autofocus': True,
            'autocomplete': 'username',
            'placeholder': _('Enter your username'),
        })
        self.fields['password'].widget.attrs.update({
            'autocomplete': 'current-password',
            'placeholder': _('Enter your password'),
        })


class RegistrationForm(AuthFieldStylingMixin, UserCreationForm):
    email = forms.EmailField(label=_('Email'), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_common_attrs()
        self.fields['username'].widget.attrs.update({
            'autofocus': True,
            'autocomplete': 'username',
            'placeholder': _('Choose a username'),
        })
        self.fields['email'].widget.attrs.update({
            'autocomplete': 'email',
            'placeholder': 'name@example.com',
        })
        self.fields['password1'].widget.attrs.update({
            'autocomplete': 'new-password',
            'placeholder': _('Create a strong password'),
        })
        self.fields['password2'].widget.attrs.update({
            'autocomplete': 'new-password',
            'placeholder': _('Repeat your password'),
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class StyledPasswordResetForm(AuthFieldStylingMixin, PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_common_attrs()
        self.fields['email'].widget.attrs.update({
            'autocomplete': 'email',
            'placeholder': 'name@example.com',
        })


class StyledSetPasswordForm(AuthFieldStylingMixin, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_common_attrs()
        self.fields['new_password1'].widget.attrs.update({
            'autocomplete': 'new-password',
            'placeholder': _('Create a new password'),
        })
        self.fields['new_password2'].widget.attrs.update({
            'autocomplete': 'new-password',
            'placeholder': _('Repeat the new password'),
        })
