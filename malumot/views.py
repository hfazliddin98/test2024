from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from malumot.models import Mavzular, Testlar
from malumot.forms import LoginForm, MavzularForm, TestlarForm



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
        object_list = Mavzular.objects.all()
        paginator = Paginator(object_list, 10)            
        page_number = request.GET.get('page')           
        page_obj = paginator.get_page(page_number)    

        context = {
            'page_obj':page_obj,
        }
        return render(request, 'malumot/mavzular.html', context)

    else:
        return render(request, 'asosiy/404.html')    


@csrf_exempt
def mavzu(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = MavzularForm(request.POST)
            if form.is_valid():
                form.save()                
                return redirect('mavzular')
        else:
            form = MavzularForm()
        context = {
            'form':form,
        }
        return render(request, 'malumot/mavzu.html', context)
    
    else:        
        return render(request, 'asosiy/404.html')


@csrf_exempt
def testlar(request):
    if request.user.is_authenticated:
        object_list = Testlar.objects.all()
        paginator = Paginator(object_list, 10)            
        page_number = request.GET.get('page')           
        page_obj = paginator.get_page(page_number)    

        context = {
            'page_obj':page_obj,
        }
        return render(request, 'malumot/testlar.html', context)

    else:
        return render(request, 'asosiy/404.html')




@csrf_exempt
def test(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TestlarForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('testlar')
        else:
            form = TestlarForm()
            
        context = {
            'form':form,
        }
        return render(request, 'malumot/test.html', context)
    
    else:        
        return render(request, 'asosiy/404.html')


  
