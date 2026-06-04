import logging
from datetime import timedelta

from django.contrib.auth.views import INTERNAL_RESET_SESSION_TOKEN, LoginView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .forms import StyledAuthenticationForm, StyledPasswordResetForm, StyledSetPasswordForm

logger = logging.getLogger('booking.auth')

PASSWORD_RESET_LIMIT = 3
PASSWORD_RESET_WINDOW_SECONDS = 15 * 60


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def _rate_limit_key(request, email):
    return f'auth:password-reset:{_client_ip(request)}:{email.lower().strip()}'


def _increment_reset_counter(request, email):
    key = _rate_limit_key(request, email)
    now = timezone.now()
    default_state = {
        'count': 0,
        'expires_at': (now + timedelta(seconds=PASSWORD_RESET_WINDOW_SECONDS)).timestamp(),
    }
    state = cache.get(key, default_state)
    if state['expires_at'] <= now.timestamp():
        state = default_state
    state['count'] += 1
    cache.set(key, state, timeout=PASSWORD_RESET_WINDOW_SECONDS)
    return state['count']


class SecureLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = StyledAuthenticationForm

    def form_valid(self, form):
        logger.info(
            'Successful login',
            extra={
                'username': form.cleaned_data.get('username'),
                'ip': _client_ip(self.request),
            },
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        username = self.request.POST.get('username', '').strip()
        if username:
            logger.warning(
                'Failed login attempt',
                extra={
                    'username': username,
                    'ip': _client_ip(self.request),
                },
            )
        return super().form_invalid(form)


class SecurePasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.txt'
    html_email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    form_class = StyledPasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        attempts = _increment_reset_counter(self.request, email)
        if attempts > PASSWORD_RESET_LIMIT:
            logger.warning(
                'Password reset rate limited',
                extra={
                    'email': email,
                    'ip': _client_ip(self.request),
                    'attempts': attempts,
                },
            )
            form.add_error(None, _('Please wait before requesting another reset link.'))
            return self.form_invalid(form)

        logger.info(
            'Password reset requested',
            extra={
                'email': email,
                'ip': _client_ip(self.request),
                'attempts': attempts,
            },
        )
        return super().form_valid(form)


class SecurePasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class SecurePasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = StyledSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

    def dispatch(self, request, *args, **kwargs):
        self.user = self.get_user(kwargs.get('uidb64'))
        token = kwargs.get('token')
        if self.user is not None and token != self.reset_url_token:
            if self.token_generator.check_token(self.user, token):
                request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                kwargs['token'] = self.reset_url_token
            else:
                logger.warning(
                    'Invalid password reset token attempt',
                    extra={
                        'uidb64': kwargs.get('uidb64'),
                        'ip': _client_ip(request),
                    },
                )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(
            'Password reset completed',
            extra={
                'user_id': getattr(self.user, 'pk', None),
                'ip': _client_ip(self.request),
            },
        )
        return response
