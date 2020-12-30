from django.db import models

from BookBSE.models import Faculty


class Time(models.Model):
    time_id = models.AutoField(primary_key=True)

    WEEKDAY_CHOICES = (
        ('Saturday', 'شنبه'),
        ('Sunday', 'یکشنبه'),
        ('Monday', 'دوشنبه'),
        ('Tuesday', 'سه‌شنبه'),
        ('Wednesday', 'چهارشنبه'),
        ('Thursday', 'پنج‌شنبه'),
        ('Friday', 'جمعه'),
    )
    weekday = models.CharField(max_length=20, choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.weekday + str(self.start_time) + " , " + str(self.end_time)


class ResearchAxis(models.Model):
    research_axis_id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


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
    free_times = models.ManyToManyField(Time, blank=True)
    direct_telephone = models.CharField(max_length=11, blank=True)
    address = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=50)
    research_axes = models.ManyToManyField(ResearchAxis, blank=True)
    bachelor = models.CharField(max_length=200, blank=True)
    masters = models.CharField(max_length=200, blank=True)
    phd = models.CharField(max_length=200, blank=True)
    postdoctoral = models.CharField(max_length=200, blank=True)
    webpage_link = models.CharField(max_length=100, blank=True)
    google_scholar_link = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + ", " + self.academic_rank
