
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_id = models.TextField(blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=120)
    description = models.TextField(default="None")
    contactInfo = models.TextField(default="N/A")
    room_alert_email = models.EmailField(default="trackerelearning@gmail.com")
    current_people_count = models.PositiveSmallIntegerField(default=0)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return "room: " + self.name

class Schedule(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_slot = models.PositiveSmallIntegerField(default=9)
    schedule_date = models.DateField(default=now, editable=True)


class RoomAccessLog(models.Model):
    STATUS_ALLOWED = "STATUS_ALLOWED"
    STATUS_DENIED = "STATUS_DENIED"
    STATUS_OUT = "STATUS_OUT"

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    temp = models.FloatField(default=37)
    status = models.TextField()

class RoomPresent(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    temp = models.FloatField(default=37)