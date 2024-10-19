import qrcode
import random
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import HttpResponse
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from quiz.models import Mavzus, Tests, Natijas
from users.models import Fakultets, Yonalishs, Kurs, Guruhs
from quiz.forms import LoginForm, MavzusForm, TestsForm, TestAnswerForm





@csrf_exempt
def home(request):
    if request.user.is_authenticated:


        return render(request, 'asosiy/home.html')
    
    else:

        return redirect('kirish')


@csrf_exempt
def kirish(request):
    if request.user.is_authenticated:
        return redirect('/')    
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('/')
                else:        
                    return redirect('kirish')
            
        else:
            form = LoginForm()

            context = {
                'form':form,
            }
            return render(request, 'users/kirish.html', context)


@csrf_exempt
def chiqish(request):
    logout(request)  
    return redirect('/')  



@csrf_exempt
def mavzular(request):
    if request.user.is_authenticated:
        mavzus = Mavzus.objects.filter(yaratish=False)
        if mavzus:
            domen = settings.DOMEN
            media_url = settings.MEDIA_ROOT

            for m in mavzus:
                data = f"https://{domen}/test_bajarish/{m.id}/"
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(data)
                qr.make()
                img = qr.make_image()
                img.save(f"{media_url}/mavzu/quiz_{m.id}.png")
                qrlink = f'https://{domen}/{media_url}/mavzu/quiz_{m.id}.png'

                        

                image_url = f'/mavzu/quiz_{m.id}.png'
            
                # Ob'ekt maydonsini yangilash
                m.qrlink = qrlink
                m.qrcode = image_url
                m.yaratish = True
                m.save()

        
        


        object_list = Mavzus.objects.all()
        paginator = Paginator(object_list, 10)            
        page_number = request.GET.get('page')           
        page_obj = paginator.get_page(page_number)    

        context = {
            'page_obj':page_obj,
        }
        return render(request, 'quiz/mavzular.html', context)

    else:
        return render(request, 'asosiy/404.html')    


@csrf_exempt
def mavzu(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = MavzusForm(request.POST)
            if form.is_valid():
                form.save()                
                return redirect('mavzular')
        else:
            form = MavzusForm()
        context = {
            'form':form,
        }
        return render(request, 'quiz/mavzu.html', context)
    
    else:        
        return render(request, 'asosiy/404.html')


@csrf_exempt
def testlar(request):
    if request.user.is_authenticated:
        object_list = Tests.objects.all()
        paginator = Paginator(object_list, 10)            
        page_number = request.GET.get('page')           
        page_obj = paginator.get_page(page_number)    

        context = {
            'page_obj':page_obj,
        }
        return render(request, 'quiz/testlar.html', context)

    else:
        return render(request, 'asosiy/404.html')




@csrf_exempt
def test(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TestsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('testlar')
        else:
            form = TestsForm()
            
        context = {
            'form':form,
        }
        return render(request, 'quiz/test.html', context)
    
    else:        
        return render(request, 'asosiy/404.html')
    


@csrf_exempt
def natijalar(request):
    if request.user.is_authenticated:
        object_list = Natijas.objects.all()
        paginator = Paginator(object_list, 10)            
        page_number = request.GET.get('page')           
        page_obj = paginator.get_page(page_number)    

        context = {
            'page_obj':page_obj,
        }
        return render(request, 'quiz/natijalar.html', context)


    else:
        return render(request, 'asosiy/404.html')




# @csrf_exempt
# def test_bajarish(request, pk):

#     tests = Tests.objects.filter(mavzu_id=pk)

#     if tests:
#         if request.method == 'POST':
#             form = TestAnswerForm(request.POST, tests=tests)
#             if form.is_valid():
#                 data = form.cleaned_data['savol']
#                 print(data)
#                 score = 0
#                 for test in tests:
#                     user_answer = form.cleaned_data[f'test_{test.id}']
#                     if user_answer == test.to_gri_javob:  # To'g'ri javobni tekshirish
#                         score += 1
                
#                 return render(request, 'test_result.html', {'score': score, 'total': len(tests)})
#         else:
#             form = TestAnswerForm(tests=tests)

        
#             return render(request, 'quiz/quiz.html', {'form':form})
#     else:

#         return HttpResponse('data')

 

@csrf_exempt
def test_bajarish(request, pk):
    tests = Tests.objects.filter(mavzu_id=pk)

    shuffled_tests = []
    for test in tests:
        variants = [
            ('A', test.variant_a),
            ('B', test.variant_b),
            ('C', test.variant_c),
            ('D', test.variant_d),
        ]
        random.shuffle(variants)
        shuffled_tests.append((test, variants))

    fakultetlar = Fakultets.objects.all() 
    yonalishlar = Yonalishs.objects.all() 
    kurslar = Kurs.objects.all()          
    guruhlar = Guruhs.objects.all()      

    if request.method == 'POST':
        form = TestAnswerForm(request.POST, tests=shuffled_tests)
        if form.is_valid():
            score = 0
            incorrect_answers = 0
            for test, variants in shuffled_tests:
                user_answer = form.cleaned_data[f'test_{test.id}']
                if user_answer == test.togri_javob:
                    score += 1
                else:
                    incorrect_answers += 1

            fakultet_id = request.POST.get('fakultet_id')
            yonalish_id = request.POST.get('yonalish_id')
            kurs_id = request.POST.get('kurs_id')
            guruh_id = request.POST.get('guruh_id')
            talaba_name = request.POST.get('talaba_name')

            if not talaba_name:
                return render(request, 'quiz/take_test.html', {
                    'form': form,
                    'tests': shuffled_tests,
                    'error': 'Iltimos, ismingizni kiriting!',
                    'fakultetlar': fakultetlar,
                    'yonalishlar': yonalishlar,
                    'kurslar': kurslar,
                    'guruhlar': guruhlar
                })

            Natijas.objects.create(
                mavzu_id_id=pk,
                fakultet_id_id=fakultet_id,
                yonalish_id_id=yonalish_id,
                kurs_id_id=kurs_id,
                guruh_id_id=guruh_id,
                talaba=talaba_name,
                togri=score,
                notogri=incorrect_answers,
                jami=len(tests)
            )

            return render(request, 'quiz/test_result.html', {
                'score': score,
                'total': len(tests)
            })
    else:
        form = TestAnswerForm(tests=shuffled_tests)

    
    context = {
        'form': form,
        'tests': shuffled_tests,
        'fakultetlar': fakultetlar,
        'yonalishlar': yonalishlar,
        'kurslar': kurslar,
        'guruhlar': guruhlar
    }
    return render(request, 'quiz/take_test.html', context)
