from django.core.validators import MinLengthValidator
from django.db import models


# def get_profile_image_filepath(self, filename):
#     return f'profile_images/{self.student_id}/{"profile_image.png"}'
#
#
# def get_default_profile_image():
#     return "x.png"


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=256, unique=True)
    student_id = models.IntegerField(unique=True)
    mobile_number = models.CharField(max_length=11, default="09100000000")
    password = models.CharField(max_length=20, validators=[MinLengthValidator(6)], blank=True)
    # date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    # profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + str(self.student_id)
