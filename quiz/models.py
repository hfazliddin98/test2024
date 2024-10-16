from django.db import models
from users.models import AsosiyModel, Fakultets, Yonalishs, Kurs, Guruhs


JAVOB_CHOICES = (
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
)



class Mavzular(AsosiyModel):
    mavzu = models.CharField(max_length=255)
    qrcode = models.ImageField(upload_to='mavzu', blank=True)
    qrlink = models.CharField(max_length=255, blank=True)
    yaratish = models.BooleanField(default=False)

    def __str__(self):
        return self.mavzu



class Testlar(AsosiyModel):
    mavzu_id = models.ForeignKey(Mavzular, on_delete=models.CASCADE)
    savol = models.CharField(max_length=500)
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)
    togri = models.CharField(max_length=25, choices=JAVOB_CHOICES, default="A")
    
    def __str__(self):
        return self.savol 
    
class Talabas(AsosiyModel):
    tast_id = models.ForeignKey(Testlar, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    fakultet_id = models.ForeignKey(Fakultets, on_delete=models.CASCADE)
    yonalish_id = models.ForeignKey(Yonalishs, on_delete=models.CASCADE)
    kurs_id = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    guruh_id = models.ForeignKey(Guruhs, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name