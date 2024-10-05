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


class Testlar(models.Model):
    savol = models.CharField(max_length=500)
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)
    togri = models.CharField(max_length=25, choices=JAVOB_CHOICES, default="A")
    
