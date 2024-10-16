import uuid
from django.db import models
from quiz.models import Testlar


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    class Meta:
        abstract = True



class Talaba(BaseModel):
    tast_id = models.ForeignKey(Testlar, on_delete=models.CASCADE)

