from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import get_template


from apps.users.models import User


def get_send_email_token(email):
    try:
        user = None
        while True:
            try:
                user = User.objects.get(email=email)
                break
            except User.DoesNotExist:
                continue
        if user:
            refresh = RefreshToken.for_user(user)
            response_token = {'refresh': refresh,
                              'access': str(refresh.access_token),
                              'user': user}
            return response_token
        else:
            raise Exception
    except Exception as ex:
        raise (ValidationError({'email': [ex]}))


def send_email_confirm_account(user, type_new_acc):
    from_email = settings.CONTACT_EMAIL
    to = user.email
    token = get_send_email_token(to)['access']
    html_content = None
    subject = None
    if type_new_acc == 'TEACHER':
        subject = 'Welcome to the IntelliFace!'
        html_template = get_template('users/welcome_new_teacher.html')
        context = {
            'full_name_receiver': user.first_name + ' ' + user.last_name,
            'create_password_link': settings.TEACHER_URL +
                                    '/teacher-setup?user_type=teacher&token={}'.format(token)
        }
        html_content = html_template.render(context)

    msg = EmailMultiAlternatives(subject=subject, from_email=from_email, to=[to])
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
    except Exception as ex:
        print(ex)


def send_teacher_setup_email(user):
    """Send a password-setup email to a newly created teacher using
    Django's PasswordResetTokenGenerator and a uid in the link.
    """
    from django.conf import settings
    from django.contrib.auth.tokens import PasswordResetTokenGenerator
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes

    from_email = settings.CONTACT_EMAIL
    to = user.email

    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(str(user.pk)))

    frontend = getattr(settings, 'FRONTEND_URL', None) or getattr(settings, 'TEACHER_URL', '')
    frontend = frontend.rstrip('/')
    link = f"{frontend}/set-password?uid={uid}&token={token}"

    subject = 'Set up your IntelliFace account'
    html_content = f"<p>Hello {user.first_name or user.email},</p>\n"
    html_content += f"<p>Please set your account password by visiting the link below. This link will expire shortly for security.</p>\n"
    html_content += f"<p><a href=\"{link}\">Set your password</a></p>\n"
    html_content += "<p>If you did not expect this email, please ignore it.</p>"

    msg = EmailMultiAlternatives(subject=subject, from_email=from_email, to=[to])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except Exception as ex:
        # avoid exposing sensitive errors; log to stdout for now
        print('Failed to send teacher setup email:', ex)