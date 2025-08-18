from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from quiz.models import Mavzus, Tests, Natijas
from users.models import Fakultets, Yonalishs, Kurs, Guruhs
from quiz.forms import LoginForm, MavzusForm, TestsForm, TestAnswerForm, TestFormNoMavzu
import qrcode
import random
from io import BytesIO
from django.core.files.base import ContentFile




@login_required
def teacher_mavzular(request):
    # Since there's no created_by field, show all mavzular for now
    # In a real application, you should add a created_by field to Mavzus model
    mavzular = Mavzus.objects.all()
    return render(request, 'quiz/teacher_mavzular.html', {'mavzular': mavzular})

@login_required
def teacher_testlar(request):
    # Since there's no created_by field, show all tests for now
    # In a real application, you should add a created_by field to Tests model
    testlar = Tests.objects.all()
    mavzular = Mavzus.objects.all()
    return render(request, 'quiz/teacher_testlar.html', {
        'testlar': testlar,
        'mavzular': mavzular
    })

@login_required
@login_required
def mavzu_edit(request, pk):
    mavzu = get_object_or_404(Mavzus, pk=pk)
    form = MavzusForm(request.POST or None, instance=mavzu)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('mavzu_detail', pk=pk)
        
    return render(request, 'quiz/mavzu_edit.html', {'mavzu': mavzu, 'form': form})

@login_required
def mavzu_delete(request, pk):
    mavzu = get_object_or_404(Mavzus, pk=pk)
    
    if request.method == 'POST':
        mavzu.delete()
        return redirect('teacher_mavzular')
        
    return redirect('mavzu_detail', pk=pk)
    
@login_required
def test_delete(request, pk):
    test = get_object_or_404(Tests, pk=pk)
    mavzu_id = test.mavzu.id
    
    if request.method == 'POST':
        test.delete()
    
    return redirect('mavzu_detail', pk=mavzu_id)
    
@login_required
def test_edit(request, pk):
    test = get_object_or_404(Tests, pk=pk)
    mavzu_id = test.mavzu.id
    
    if request.method == 'POST':
        form = TestFormNoMavzu(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('mavzu_detail', pk=mavzu_id)
    else:
        form = TestFormNoMavzu(instance=test)
    
    return render(request, 'quiz/test_edit.html', {
        'test': test,
        'form': form,
        'mavzu_id': mavzu_id
    })

@login_required
def mavzu_qrcode(request, pk):
    mavzu = get_object_or_404(Mavzus, pk=pk)
    return render(request, 'quiz/mavzu_qrcode.html', {'mavzu': mavzu})


def teacher_natijalar(request):
    from django.db.models import Count, Sum, Avg, F, ExpressionWrapper, FloatField
    
    # Get all natijas since there's no created_by relationship
    mavzu_id = request.GET.get('mavzu')
    talaba_filter = request.GET.get('talaba')
    natijalar_query = Natijas.objects.all()
    
    # Apply filters
    if mavzu_id:
        natijalar_query = natijalar_query.filter(mavzu_id=mavzu_id)
    if talaba_filter:
        natijalar_query = natijalar_query.filter(talaba__icontains=talaba_filter)
    
    # Get unique students and their aggregated results for detailed table
    student_summary = {}
    for natija in natijalar_query:
        student_key = f"{natija.talaba}_{natija.kurs.id}_{natija.guruh.id}"
        if student_key not in student_summary:
            student_summary[student_key] = {
                'talaba': natija.talaba,
                'fakultet': natija.fakultet,
                'yonalish': natija.yonalish,
                'kurs': natija.kurs,
                'guruh': natija.guruh,
                'mavzular': {}
            }
        
        # Add topic results for this student
        if natija.mavzu.id not in student_summary[student_key]['mavzular']:
            student_summary[student_key]['mavzular'][natija.mavzu.id] = {
                'mavzu': natija.mavzu,
                'togri': natija.togri,
                'notogri': natija.notogri,
                'jami': natija.jami,
                'foiz': round((natija.togri / natija.jami * 100) if natija.jami > 0 else 0),
                'sana': natija.created_at
            }
    
    # Transform to list for template
    student_results = list(student_summary.values())
    
    # Get all topics for reference
    all_mavzular = Mavzus.objects.all()
    
    # Paginate standard results
    paginator = Paginator(natijalar_query.order_by('-created_at'), 20)
    page = request.GET.get('page', 1)
    natijalar = paginator.get_page(page)
    
    # Get statistics
    natijalar_count = natijalar_query.count()
    talabalar_count = natijalar_query.values('talaba').distinct().count() if natijalar_count > 0 else 0
    
    # Calculate averages
    ortacha_ball = 0
    eng_yuqori_ball = 0
    eng_yuqori_talaba = "Yo'q"
    
    if natijalar_count > 0:
        # Calculate average percentage
        avg_data = natijalar_query.aggregate(
            avg_togri=Avg('togri'),
            avg_jami=Avg('jami')
        )
        if avg_data['avg_jami'] > 0:
            ortacha_ball = round((avg_data['avg_togri'] / avg_data['avg_jami']) * 100)
        
        # Find highest scoring student
        top_result = natijalar_query.annotate(
            ball=ExpressionWrapper(F('togri') * 100.0 / F('jami'), output_field=FloatField())
        ).order_by('-ball').first()
        
        if top_result and top_result.jami > 0:
            eng_yuqori_ball = round((top_result.togri / top_result.jami) * 100)
            eng_yuqori_talaba = top_result.talaba
    
    # Count tests and topics
    mavzular_count = Mavzus.objects.count()
    testlar_count = Tests.objects.count()
    
    # Get all topics for filtering
    mavzular = Mavzus.objects.all()
    
    return render(request, 'quiz/teacher_natijalar.html', {
        'natijalar': natijalar,
        'natijalar_count': natijalar_count,
        'talabalar_count': talabalar_count,
        'ortacha_ball': ortacha_ball,
        'eng_yuqori_ball': eng_yuqori_ball,
        'eng_yuqori_talaba': eng_yuqori_talaba,
        'mavzular_count': mavzular_count,
        'testlar_count': testlar_count,
        'mavzular': mavzular,
        'student_results': student_results,
        'all_mavzular': all_mavzular
    })


def home(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    user = request.user
    if hasattr(user, 'role'):
        if user.role == 'admin':
            return render(request, 'asosiy/home_admin.html')
        elif user.role == 'oqituvchi':
            # Get statistics for teacher dashboard
            mavzular_count = Mavzus.objects.count()
            testlar_count = Tests.objects.count()
            
            # Get natija statistics
            natijalar = Natijas.objects.all()
            natijalar_count = natijalar.count()
            talabalar_count = natijalar.values('talaba').distinct().count() if natijalar_count > 0 else 0
            
            return render(request, 'asosiy/home_teacher.html', {
                'mavzular_count': mavzular_count,
                'testlar_count': testlar_count,
                'natijalar_count': natijalar_count,
                'talabalar_count': talabalar_count
            })
    return render(request, 'asosiy/home.html')



def kirish(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'users/kirish.html', {'form': form})



def chiqish(request):
    logout(request)
    return redirect('/kirish/')





@login_required
def mavzu(request, pk=None):
    if not request.user.is_authenticated:
        return render(request, 'asosiy/404.html')
    if pk:
        mavzu = get_object_or_404(Mavzus, pk=pk)
        tests = mavzu.tests.all()
        form = TestFormNoMavzu(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            test = form.save(commit=False)
            test.mavzu = mavzu
            test.save()
            return redirect('mavzu_detail', pk=pk)
        return render(request, 'quiz/mavzu_detail.html', {'mavzu': mavzu, 'tests': tests, 'form': form})
    else:
        from django.db import transaction
        
        if request.method == 'POST':
            mavzu_form = MavzusForm(request.POST)
            
            if mavzu_form.is_valid():
                try:
                    with transaction.atomic():
                        # Save mavzu
                        mavzu = mavzu_form.save()
                        
                        # Process tests
                        test_count = 0
                        while True:
                            if f'savol_{test_count}' not in request.POST:
                                break
                                
                            savol = request.POST.get(f'savol_{test_count}')
                            variant_a = request.POST.get(f'variant_a_{test_count}')
                            variant_b = request.POST.get(f'variant_b_{test_count}')
                            variant_c = request.POST.get(f'variant_c_{test_count}')
                            variant_d = request.POST.get(f'variant_d_{test_count}')
                            togri_javob = request.POST.get(f'togri_javob_{test_count}')
                            
                            # Validate test data
                            if savol and variant_a and variant_b and variant_c and variant_d and togri_javob:
                                # Create test
                                Tests.objects.create(
                                    mavzu=mavzu,
                                    savol=savol,
                                    variant_a=variant_a,
                                    variant_b=variant_b,
                                    variant_c=variant_c,
                                    variant_d=variant_d,
                                    togri_javob=togri_javob
                                )
                            
                            test_count += 1
                        
                    return redirect('teacher_mavzular')
                except Exception as e:
                    # In case of error, display it
                    return render(request, 'quiz/mavzu.html', {
                        'mavzu_form': mavzu_form,
                        'error': f"Xatolik yuz berdi: {str(e)}"
                    })
            else:
                return render(request, 'quiz/mavzu.html', {'mavzu_form': mavzu_form})
        else:
            mavzu_form = MavzusForm()
            
        return render(request, 'quiz/mavzu.html', {'mavzu_form': mavzu_form})



@login_required
def test(request):
    if not request.user.is_authenticated:
        return render(request, 'asosiy/404.html')
    form = TestsForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('teacher_testlar')
    return render(request, 'quiz/test.html', {'form': form})


from users.forms import YonalishForm


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
    # Tartiblangan querysetlar
    fakultetlar = Fakultets.objects.all().order_by('name')
    yonalishlar = Yonalishs.objects.all().order_by('name')
    kurslar = Kurs.objects.all().order_by('name')
    guruhlar = Guruhs.objects.all().order_by('name')
    if request.method == 'POST':
        print("POST data:", request.POST)
        # Foydalanuvchi javoblari dict ko‘rinishida keladi, masalan:
        # {'test_<uuid>': ['B'], ...}
        yonalishform = YonalishForm(request.POST)
        form = TestAnswerForm(request.POST, tests=shuffled_tests)
        if form.is_valid():
            score = 0
            incorrect_answers = 0
            for test_obj, variants in shuffled_tests:
                # request.POST.getlist() har doim ro'yxat qaytaradi, shuning uchun birinchi elementni olamiz
                user_answers = request.POST.getlist(f'test_{test_obj.id}')
                user_answer = user_answers[0] if user_answers else None
                is_correct = user_answer == test_obj.togri_javob
                print(f"Test ID: {test_obj.id}, User answer: {user_answer}, Correct: {test_obj.togri_javob}, Is correct: {is_correct}")
                if is_correct:
                    score += 1
                else:
                    incorrect_answers += 1
            fakultet_id = yonalishform.cleaned_data.get('fakultet')
            yonalish_id = yonalishform.cleaned_data.get('name')
            kurs_id = request.POST.get('kurs_id')
            guruh_id = request.POST.get('guruh_id')
            talaba_name = request.POST.get('talaba_name')
            if not talaba_name:
                return render(request, 'quiz/take_test.html', {
                    'form': form,
                    'yonalishform': yonalishform,
                    'tests': shuffled_tests,
                    'error': 'Iltimos, ismingizni kiriting!',
                    'fakultetlar': fakultetlar,
                    'yonalishlar': yonalishlar,
                    'kurslar': kurslar,
                    'guruhlar': guruhlar,
                })
            # Natijas obyektini yaratishdan oldin barcha idlar to'g'ri va bo'sh emasligiga ishonch hosil qiling
            if fakultet_id and yonalish_id and kurs_id and guruh_id:
                Natijas.objects.create(
                    mavzu_id=pk,
                    fakultet_id=fakultet_id,
                    yonalish_id=yonalish_id,
                    kurs_id=kurs_id,
                    guruh_id=guruh_id,
                    talaba=talaba_name,
                    togri=score,
                    notogri=incorrect_answers,
                    jami=len(tests)
                )
            else:
                return render(request, 'quiz/take_test.html', {
                    'form': form,
                    'yonalishform': yonalishform,
                    'tests': shuffled_tests,
                    'error': 'Fakultet, yo‘nalish, kurs va guruh to‘liq tanlanishi shart!',
                    'fakultetlar': fakultetlar,
                    'yonalishlar': yonalishlar,
                    'kurslar': kurslar,
                    'guruhlar': guruhlar,
                })
            return render(request, 'quiz/test_result.html', {
                'score': round(score * 100 / len(tests)) if len(tests) > 0 else 0,
                'total': len(tests),
                'correct_answers': score,
                'incorrect_answers': incorrect_answers,
                'fakultet': Fakultets.objects.filter(id=fakultet_id).first(),
                'yonalish': Yonalishs.objects.filter(id=yonalish_id).first(),
                'kurs': Kurs.objects.filter(id=kurs_id).first(),
                'guruh': Guruhs.objects.filter(id=guruh_id).first(),
                'talaba_name': talaba_name,
            })
    else:
        form = TestAnswerForm(tests=shuffled_tests)
        yonalishform = YonalishForm()
    context = {
        'form': form,
        'yonalishform': yonalishform,
        'tests': shuffled_tests,
        'fakultetlar': fakultetlar,
        'yonalishlar': yonalishlar,
        'kurslar': kurslar,
        'guruhlar': guruhlar,
    }
    return render(request, 'quiz/take_test.html', context)
