from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(
        self,
        email,
        password,
        first_name,
        last_name,
        state,
        city,
        bio,
        age,
        gender,
        avater,
        **extra_fields
    ):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            state=state,
            city=city,
            bio=bio,
            age=age,
            gender=gender,
            avater=avater,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("first_name", "")
        extra_fields.setdefault("last_name", "")
        extra_fields.setdefault("state", "")
        extra_fields.setdefault("city", "")
        extra_fields.setdefault("bio", "")
        extra_fields.setdefault("age", 0)
        extra_fields.setdefault("gender", "")
        extra_fields.setdefault("avater", "")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)
