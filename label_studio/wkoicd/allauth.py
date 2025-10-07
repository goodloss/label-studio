import typing
import time
from django.contrib import messages
from allauth.account.adapter import DefaultAccountAdapter

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_backends,
    get_user_model,
    login as django_login,
    logout as django_logout,
)

from organizations.models import Organization

from django.utils import timezone


class AccountAdapter(DefaultAccountAdapter):

    def set_phone(self, user, phone: str, verified: bool):
        user.phone = phone
        user.phone_verified = verified
        user.save(update_fields=["phone", "phone_verified"])

    def get_phone(self, user) -> typing.Optional[typing.Tuple[str, bool]]:
        if user.phone:
            return user.phone, user.phone_verified
        return None

    def set_phone_verified(self, user, phone):
        self.set_phone(user, phone, True)

    def send_verification_code_sms(self, user, phone: str, code: str, **kwargs):
        messages.add_message(
            self.request,
            messages.WARNING,
            f"⚠️ SMS demo stub: assume code {code} was sent to {phone}.",
        )

    def send_unknown_account_sms(self, phone: str, **kwargs):
        messages.add_message(
            self.request,
            messages.WARNING,
            f"⚠️ SMS demo stub: Enumeration prevention: texted {phone} informing no account exists.",
        )

    def send_account_already_exists_sms(self, phone: str, **kwargs):
        messages.add_message(
            self.request,
            messages.WARNING,
            f"⚠️ SMS demo stub: Enumeration prevention: texted {phone} informing account already exists.",
        )

    def get_user_by_phone(self, phone):
        return User.objects.filter(phone=phone).order_by("-phone_verified").first()

    def pre_login(
        self,
        request,
        user,
        *,
        email_verification,
        signal_kwargs,
        email,
        signup,
        redirect_url,
    ):

        # user.is_staff = True
        # user.is_superuser = True

        if Organization.objects.exists():
            org = Organization.objects.first()
            if not org.has_user(user):
                org.add_user(user)
        else:
            org = Organization.create_organization(
                created_by=user, title="Label Studio"
            )

        user.active_organization = org
        user.save(update_fields=["active_organization"])

        print(f">>>>>>>>>>>Save activity for user={user}")
        print(dir(request))

        user.activity_at = timezone.now()
        user.last_login = timezone.now()
        request.session["last_login"] = time.time()
        user.save()

        if not user.is_active:
            return self.respond_user_inactive(request, user)

    def new_user(self, request):
        """
        Instantiates a new User instance.
        """
        user = get_user_model()()
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        # for k, v in user.__dict__.items():
        #     print(k, "==>", v)

        return user
