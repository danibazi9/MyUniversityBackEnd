from django.db import models


# Create your models here.
from BookBSE.models import Faculty


class Professor(models.Model):
    professor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='professors/images/', blank=True)

    RANK_CHOICES = (
        ('Professor', 'استاد'),
        ('Associate Professor', 'دانشیار'),
        ('Assistant Professor', 'استادیار'),
    )
    academic_rank = models.CharField(max_length=20, choices=RANK_CHOICES)
    direct_telephone = models.CharField(max_length=11, blank=True)
    address = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=50)
    research_axes = models.TextField(blank=True)
    bachelor = models.CharField(max_length=200, blank=True)
    masters = models.CharField(max_length=200, blank=True)
    phd = models.CharField(max_length=200, blank=True)
    postdoctoral = models.CharField(max_length=200, blank=True)
    webpage_link = models.CharField(max_length=100, blank=True)
    google_scholar_link = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + ", " + self.academic_rank
