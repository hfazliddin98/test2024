import uuid
from django.db import models






KURS_CHOICES = (
    ('1-kurs','1-kurs'),
    ('2-kurs','2-kurs'),
    ('3-kurs','3-kurs'),
    ('4-kurs','4-kurs'),    
)


GURUH_CHOICES = (
    ('1-guruh','1-guruh'),
    ('2-guruh','2-guruh'),
    ('3-guruh','3-guruh'),
    ('4-guruh','4-guruh'),    
    ('5-guruh','5-guruh'),
    ('6-guruh','6-guruh'),
    ('7-guruh','7-guruh'),
    ('8-guruh','8-guruh'),    
    ('9-guruh','9-guruh'),
    ('10-guruh','10-guruh'),
    ('11-guruh','11-guruh'),
    ('12-guruh','12-guruh'),    
)

class AsosiyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    class Meta:
        abstract = True


class Fakultets(AsosiyModel):
    name = models.CharField('Fakultetni kiriting', max_length=255)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name

class Yonalishs(AsosiyModel):
    fakultet = models.ForeignKey(Fakultets, on_delete=models.CASCADE)
    name = models.CharField('Yo`nalishni kiriting', max_length=255)

    class Meta:
        ordering = ['-fakultet', '-name']

    def __str__(self):
        return self.name

class Kurs(AsosiyModel):
    name = models.CharField(max_length=255, default='1-kurs')

    class Meta:
        ordering = ['name']


    def __str__(self):
        return self.name

class Guruhs(AsosiyModel):
    name = models.CharField(max_length=255, default='1-guruh')

    class Meta:
        ordering = ['name']


    def __str__(self):
        return self.name






      