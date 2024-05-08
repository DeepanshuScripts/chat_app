import datetime
import jwt
from django.conf import settings
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email=None,phone_number=None, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        # if not email:
        #     raise ValueError("The given email must be set")
        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email,phone_number=None, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number,email,password, **extra_fields)

    def create_superuser(self,email=None,phone_number=None, password=None, **extra_fields):
        """Create and save a SuperUser with the given email, mobile number, and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email,phone_number, password, **extra_fields)

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.phone_number

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + datetime.timedelta(days=60)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.strftime("%s"))},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token.decode("utf-8")




# class UserManager(BaseUserManager):
#     use_in_migrations = True

#     def _create_user(self, email=None,phone_number=None, password=None, **extra_fields):
#         """Create and save a User with the given email and password."""
#         # if not email:
#         #     raise ValueError("The given email must be set")
#         user = self.model(
#             phone_number=phone_number,
#             email=self.normalize_email(email),
#             **extra_fields
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_user(self, email=None,phone_number=None, password=None, **extra_fields):
#         """Create and save a regular User with the given email and password."""
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(phone_number,email,password, **extra_fields)

#     def create_superuser(self,email=None,phone_number=None, password=None, **extra_fields):
#         """Create and save a SuperUser with the given email, mobile number, and password."""
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self._create_user(email,phone_number, password, **extra_fields)

#     def __str__(self):
#         """
#         Returns a string representation of this `User`.

#         This string is used when a `User` is printed in the console.
#         """
#         return self.phone_number