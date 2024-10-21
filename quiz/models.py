from django.db import models
from users.models import AsosiyModel, Fakultets, Yonalishs, Kurs, Guruhs




class Mavzus(AsosiyModel):
    mavzu = models.CharField(max_length=255)
    qrcode = models.ImageField(upload_to='mavzu', blank=True)
    qrlink = models.CharField(max_length=255, blank=True)
    yaratish = models.BooleanField(default=False)

    def __str__(self):
        return self.mavzu



class Tests(AsosiyModel):
    mavzu_id = models.ForeignKey(Mavzus, on_delete=models.CASCADE)
    savol = models.CharField(max_length=500)
    variant_a = models.CharField(max_length=255)
    variant_b = models.CharField(max_length=255)
    variant_c = models.CharField(max_length=255)
    variant_d = models.CharField(max_length=255)
    togri_javob = models.CharField(max_length=1, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ])

    def __str__(self):
        return self.savol 
    
    
    
class Natijas(AsosiyModel):
    mavzu_id = models.ForeignKey(Mavzus, on_delete=models.CASCADE)
    fakultet_id = models.ForeignKey(Fakultets, on_delete=models.CASCADE)
    yonalish_id = models.ForeignKey(Yonalishs, on_delete=models.CASCADE)
    kurs_id = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    guruh_id = models.ForeignKey(Guruhs, on_delete=models.CASCADE)
    talaba = models.CharField(max_length=255)
    togri = models.IntegerField(default=0)
    notogri = models.IntegerField(default=0)
    jami = models.IntegerField(default=0)
        

    def __str__(self):
        return self.talaba
    
    class Meta:
        ordering = ('-created_at',)