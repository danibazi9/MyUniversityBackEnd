from django.db import models
from account.models import Account


class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    established_year = models.IntegerField()
    head_of_organization = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name + ",    Head: " + self.head_of_organization.first_name + " " + self.head_of_organization.last_name


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event/images/', blank=True)
    organizer = models.ForeignKey(Organization, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    HOLD_CHOICES = (
        ('Presence', 'Presence'),
        ('Online', 'Online'),
    )
    hold_type = models.CharField(max_length=10, choices=HOLD_CHOICES)
    location = models.CharField(max_length=255)
    cost = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name + "    Organized by: " + self.organizer.name
