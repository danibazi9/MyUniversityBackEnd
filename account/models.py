from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, student_id, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not student_id:
            raise ValueError('Users must have a student_id')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            student_id=student_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, student_id):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            student_id=student_id,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.first_name = 'admin'
        user.last_name = 'admin'
        user.role = 'superuser'
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    student_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to='users/images/', blank=True)
    mobile_number = models.CharField(max_length=11, default="09100000000")
    password = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(default='student', max_length=20, verbose_name='role')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'student_id']

    objects = MyAccountManager()

    def __str__(self):
        return self.username + ", " + str(self.student_id)

    # For checking permissions. to keep it simple all admin have ALL permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
