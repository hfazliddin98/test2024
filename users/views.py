from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Fakultets, Yonalishs, Kurs, Guruhs




@csrf_exempt
def get_yonalishlar(request):
    fakultet_id = request.GET.get('fakultet_id')
    yonalishlar = list(Yonalishs.objects.filter(fakultet=fakultet_id).values('id', 'name'))
    return JsonResponse({'yonalishlar': yonalishlar})


