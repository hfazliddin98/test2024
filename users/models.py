
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

    # ...existing fields...
class Users(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('oqituvchi', 'O‘qituvchi'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='oqituvchi')
    open_password = models.CharField(max_length=128, blank=True, null=True, verbose_name='Ochiq parol')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"







class AsosiyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    class Meta:
        abstract = True



class Fakultets(AsosiyModel):
    name = models.CharField('Fakultet', max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Yonalishs(AsosiyModel):
    fakultet = models.ForeignKey(Fakultets, on_delete=models.CASCADE, related_name='yonalishlar')
    name = models.CharField('Yo‘nalish', max_length=255)

    class Meta:
        ordering = ['fakultet', 'name']

    def __str__(self):
        return f"{self.fakultet.name} / {self.name}"

class Kurs(AsosiyModel):
    yonalish = models.ForeignKey(Yonalishs, on_delete=models.CASCADE, related_name='kurslar')
    name = models.CharField(max_length=255, default='1-kurs')

    class Meta:
        ordering = ['yonalish', 'name']

    def __str__(self):
        return f"{self.yonalish.name} / {self.name}"

class Guruhs(AsosiyModel):
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='guruhlar')
    name = models.CharField(max_length=255, default='1-guruh')

    class Meta:
        ordering = ['kurs', 'name']

    def __str__(self):
        return f"{self.kurs.name} / {self.name}"






      