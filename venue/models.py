from django.db import models

# Create your models here.

class Venue(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Booking(models.Model):
    APPROVAL_CHOICES = (
    (u'2', u'No'),
    (u'3', u'Yes'),
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.ForeignKey(Venue,models.CASCADE,'bookings')
    status = models.CharField(max_length=1,default='1',choices=APPROVAL_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    

