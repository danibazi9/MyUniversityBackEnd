from django.db import models


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=256)
    student_id = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name + " " + self.last_name


class EmailVerify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vc_code = models.IntegerField(default=0)
    expired_time = models.TimeField()

    def __str__(self):
        return self.user.email + " " + str(self.vc_code)
