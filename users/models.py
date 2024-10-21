import uuid
from django.db import models


class AsosiyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    class Meta:
        abstract = True



class Fakultets(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Yonalishs(AsosiyModel):
    fakultet_id = models.ForeignKey(Fakultets, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Kurs(AsosiyModel):
    yonalish_id = models.ForeignKey(Yonalishs, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Guruhs(AsosiyModel):
    kurs_id = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name





      