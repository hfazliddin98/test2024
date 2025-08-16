from django.db import models
from users.models import AsosiyModel, Fakultets, Yonalishs, Kurs, Guruhs





class Mavzus(AsosiyModel):
    mavzu = models.CharField(max_length=255)
    qrcode = models.ImageField(upload_to='mavzu', blank=True)
    qrlink = models.CharField(max_length=255, blank=True)
    yaratish = models.BooleanField(default=False)
    created_by = models.ForeignKey('users.Users', on_delete=models.CASCADE, related_name='mavzular', null=True)

    class Meta:
        ordering = ['mavzu']

    def __str__(self):
        return self.mavzu




class Tests(AsosiyModel):
    mavzu = models.ForeignKey(Mavzus, on_delete=models.CASCADE, related_name='tests')
    savol = models.CharField(max_length=500)
    variant_a = models.CharField(max_length=255)
    variant_b = models.CharField(max_length=255)
    variant_c = models.CharField(max_length=255)
    variant_d = models.CharField(max_length=255)
    togri_javob = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    class Meta:
        ordering = ['savol']

    def __str__(self):
        return self.savol
    
    
    

class Natijas(AsosiyModel):
    mavzu = models.ForeignKey(Mavzus, on_delete=models.CASCADE, related_name='natijalar')
    fakultet = models.ForeignKey(Fakultets, on_delete=models.CASCADE, related_name='natijalar')
    yonalish = models.ForeignKey(Yonalishs, on_delete=models.CASCADE, related_name='natijalar')
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='natijalar')
    guruh = models.ForeignKey(Guruhs, on_delete=models.CASCADE, related_name='natijalar')
    talaba = models.CharField(max_length=255)
    togri = models.IntegerField(default=0)
    notogri = models.IntegerField(default=0)
    jami = models.IntegerField(default=0)

    class Meta:
        ordering = ['talaba']

    def __str__(self):
        return self.talaba
    