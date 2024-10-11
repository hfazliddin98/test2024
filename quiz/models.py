
from django.db import models

JAVOB_CHOICES = (
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
)



class Mavzular(models.Model):
    mavzu = models.CharField(max_length=255)
    qrcode = models.ImageField(upload_to='mavzu', blank=True)
    yaratish = models.BooleanField(default=False)

    def __str__(self):
        return self.mavzu



class Testlar(models.Model):
    mavzu_id = models.ForeignKey(Mavzular, on_delete=models.CASCADE)
    savol = models.CharField(max_length=500)
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)
    togri = models.CharField(max_length=25, choices=JAVOB_CHOICES, default="A")
    
    def __str__(self):
        return self.savol 