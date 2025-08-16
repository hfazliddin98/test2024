# ===== IMPORTS =====
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth import logout
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Max, F, ExpressionWrapper, DecimalField, Case, When, Value
from django.db.models.functions import Round
from users.models import Users, Yonalishs, Kurs, Guruhs, Fakultets
from users.forms import OqituvchiForm, FakultetForm, YonalishForm, KursForm, GuruhForm
from quiz.models import Natijas, Mavzus


# ===== ADMIN NATIJALAR =====
@login_required
def admin_natijalar(request):
    # Get filters
    fakultet_id = request.GET.get('fakultet')
    yonalish_id = request.GET.get('yonalish')
    
    # Base query
    natijalar_query = Natijas.objects.select_related(
        'fakultet', 'yonalish', 'kurs', 'guruh', 'mavzu'
    )
    
    # Apply filters
    if fakultet_id and fakultet_id.strip():  # Make sure it's not empty
        natijalar_query = natijalar_query.filter(fakultet_id=fakultet_id)
        
        if yonalish_id:
            natijalar_query = natijalar_query.filter(yonalish_id=yonalish_id)
    
    # Pagination
    paginator = Paginator(natijalar_query.order_by('-created_at'), 20)
    page = request.GET.get('page', 1)
    natijalar = paginator.get_page(page)
    
    # Get all fakultets for filtering
    fakultetlar = Fakultets.objects.all()
    
    # Get yonalishlar for the selected fakultet
    yonalishlar = []
    selected_fakultet = None
    if fakultet_id and fakultet_id.strip():
        try:
            selected_fakultet = Fakultets.objects.get(pk=fakultet_id)
            yonalishlar = Yonalishs.objects.filter(fakultet_id=fakultet_id)
        except Fakultets.DoesNotExist:
            selected_fakultet = None
    
    # Count statistics - filtered results count and total count
    filtered_natijalar_count = natijalar_query.count()
    natijalar_count = filtered_natijalar_count  # Use filtered count for display
    
    # Calculate statistics similar to teacher view
    talabalar_count = natijalar_query.values('talaba').distinct().count() if natijalar_count > 0 else 0
    
    # Calculate averages and other statistics
    ortacha_ball = 0
    eng_yuqori_ball = 0
    eng_yuqori_talaba = "Yo'q"
    fakultetlar_count = Fakultets.objects.count()
    yonalishlar_count = Yonalishs.objects.count()
    
    if natijalar_count > 0:
        # Calculate average percentage
        avg_data = natijalar_query.aggregate(
            avg_togri=Avg('togri'),
            avg_jami=Avg('jami')
        )
        if avg_data['avg_jami'] and avg_data['avg_jami'] > 0:
            ortacha_ball = round((avg_data['avg_togri'] / avg_data['avg_jami']) * 100)
        
        # Find highest score
        top_result = natijalar_query.annotate(
            percentage=ExpressionWrapper(
                F('togri') * 100.0 / F('jami'),
                output_field=DecimalField(max_digits=5, decimal_places=2)
            )
        ).order_by('-percentage').first()
        
        if top_result:
            eng_yuqori_ball = round(float(top_result.percentage))
            eng_yuqori_talaba = top_result.talaba
    
    # Get all topics for reference
    all_mavzular = Mavzus.objects.all()
    
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
    
    # Return only the necessary data for our simplified view
    return render(request, 'asosiy/admin_natijalar.html', {
        'natijalar': natijalar,
        'fakultetlar': fakultetlar,
        'yonalishlar': yonalishlar,
        'selected_fakultet': selected_fakultet,
        'natijalar_count': natijalar_count,
        'talabalar_count': talabalar_count,
        'ortacha_ball': ortacha_ball,
        'eng_yuqori_ball': eng_yuqori_ball,
        'eng_yuqori_talaba': eng_yuqori_talaba,
        'fakultetlar_count': fakultetlar_count,
        'yonalishlar_count': yonalishlar_count,
        'all_mavzular': all_mavzular,
        'student_results': student_results
    })


# ===== FAKULTET CRUD =====
@login_required
def admin_fakultetlar(request):
    fakultetlar = Fakultets.objects.all()
    return render(request, 'asosiy/admin_fakultetlar.html', {'fakultetlar': fakultetlar})


@login_required
def fakultet_create(request):
    if request.method == 'POST':
        fakultet_nomi = request.POST.get('name')
        if not fakultet_nomi:
            return render(request, 'asosiy/fakultet_create.html', {'error': 'Fakultet nomi kiritilishi shart.'})

        yonalishlar = request.POST.getlist('yonalishlar[]')
        kurslar_dict = {}
        guruhlar_dict = {}
        
        for key in request.POST:
            if key.startswith('kurslar') and key.endswith('[]'):
                idx = key.replace('kurslar', '').replace('[]', '')
                kurslar_dict[idx] = request.POST.getlist(key)
            if key.startswith('guruhlar') and key.endswith('[]'):
                parts = key.replace('guruhlar', '').replace('[]', '').split('_')
                if len(parts) == 2:
                    yon_idx, kurs_idx = parts
                    guruhlar_dict[(yon_idx, kurs_idx)] = request.POST.getlist(key)

        try:
            with transaction.atomic():
                fakultet = Fakultets.objects.create(name=fakultet_nomi)
                for yon_idx, yon_nomi in enumerate(yonalishlar):
                    if not yon_nomi.strip():
                        continue
                    yonalish = Yonalishs.objects.create(name=yon_nomi.strip(), fakultet=fakultet)
                    kurslar = kurslar_dict.get(str(yon_idx), [])
                    if kurslar:
                        kurs_idx = len(kurslar) - 1
                        kurs_nomi = kurslar[kurs_idx].strip()
                        if kurs_nomi:
                            kurs_obj = Kurs.objects.create(yonalish=yonalish, name=kurs_nomi)
                            guruhlar = guruhlar_dict.get((str(yon_idx), str(kurs_idx)), [])
                            for guruh_nomi in guruhlar:
                                if guruh_nomi.strip():
                                    Guruhs.objects.create(kurs=kurs_obj, name=guruh_nomi.strip())
                        for prev_idx in range(len(kurslar)-1):
                            prev_nomi = kurslar[prev_idx].strip()
                            if prev_nomi:
                                Kurs.objects.create(yonalish=yonalish, name=prev_nomi)
            return redirect('admin_fakultetlar')
        except Exception as e:
            return render(request, 'asosiy/fakultet_create.html', {'error': f'Xatolik: {str(e)}'})

    return render(request, 'asosiy/fakultet_create.html')


@login_required
def fakultet_update(request, pk):
    fakultet = Fakultets.objects.get(pk=pk)
    if request.method == 'POST':
        fakultet_nomi = request.POST.get('name')
        if not fakultet_nomi:
            return render(request, 'asosiy/fakultet_update.html', {'fakultet': fakultet, 'error': 'Fakultet nomi kiritilishi shart.'})

        yonalishlar = request.POST.getlist('yonalishlar[]')
        kurslar_dict = {}
        guruhlar_dict = {}
        
        for key in request.POST:
            if key.startswith('kurslar') and key.endswith('[]'):
                idx = key.replace('kurslar', '').replace('[]', '')
                kurslar_dict[idx] = request.POST.getlist(key)
            if key.startswith('guruhlar') and key.endswith('[]'):
                parts = key.replace('guruhlar', '').replace('[]', '').split('_')
                if len(parts) == 2:
                    yon_idx, kurs_idx = parts
                    guruhlar_dict[(yon_idx, kurs_idx)] = request.POST.getlist(key)

        try:
            with transaction.atomic():
                fakultet.name = fakultet_nomi
                fakultet.save()
                
                # Delete all old related objects
                for yonalish in fakultet.yonalishlar.all():
                    for kurs in yonalish.kurslar.all():
                        kurs.guruhlar.all().delete()
                    yonalish.kurslar.all().delete()
                fakultet.yonalishlar.all().delete()

                # Create new objects
                for yon_idx, yon_nomi in enumerate(yonalishlar):
                    if not yon_nomi.strip():
                        continue
                    yonalish = Yonalishs.objects.create(name=yon_nomi.strip(), fakultet=fakultet)
                    kurslar = kurslar_dict.get(str(yon_idx), [])
                    if kurslar:
                        kurs_idx = len(kurslar) - 1
                        kurs_nomi = kurslar[kurs_idx].strip()
                        if kurs_nomi:
                            kurs_obj = Kurs.objects.create(yonalish=yonalish, name=kurs_nomi)
                            guruhlar = guruhlar_dict.get((str(yon_idx), str(kurs_idx)), [])
                            for guruh_nomi in guruhlar:
                                if guruh_nomi.strip():
                                    Guruhs.objects.create(kurs=kurs_obj, name=guruh_nomi.strip())
                        for prev_idx in range(len(kurslar)-1):
                            prev_nomi = kurslar[prev_idx].strip()
                            if prev_nomi:
                                Kurs.objects.create(yonalish=yonalish, name=prev_nomi)
            return redirect('admin_fakultetlar')
        except Exception as e:
            return render(request, 'asosiy/fakultet_update.html', {'fakultet': fakultet, 'error': f'Xatolik: {str(e)}'})

    return render(request, 'asosiy/fakultet_update.html', {'fakultet': fakultet})


@login_required
@require_POST
def fakultet_delete(request, pk):
    fakultet = Fakultets.objects.get(pk=pk)
    fakultet.delete()
    return redirect('admin_fakultetlar')


# ===== YONALISH CRUD =====
@login_required
def admin_yonalishlar(request):
    fakultetlar = Fakultets.objects.all()
    fakultet_id = request.GET.get('fakultet')
    yonalishlar = Yonalishs.objects.select_related('fakultet').all()
    if fakultet_id:
        yonalishlar = yonalishlar.filter(fakultet_id=fakultet_id)
    return render(request, 'asosiy/admin_yonalishlar.html', {
        'yonalishlar': yonalishlar,
        'fakultetlar': fakultetlar,
    })


@login_required
def yonalish_create(request):
    fakultet_id = request.GET.get('fakultet')
    if fakultet_id:
        fakultet = Fakultets.objects.get(pk=fakultet_id)
    else:
        fakultet = None

    if request.method == 'POST':
        yonalish_nomi = request.POST.get('name')
        if not yonalish_nomi or not fakultet:
            error = "Yonalish nomi va fakultet tanlanishi shart."
            return render(request, 'asosiy/yonalish_create.html', {'fakultet': fakultet, 'error': error})

        kurslar = request.POST.getlist('kurslar[]')
        guruhlar_dict = {}
        
        for key in request.POST:
            if key.startswith('guruhlar') and key.endswith('[]'):
                idx = key.replace('guruhlar', '').replace('[]', '')
                guruhlar_dict[idx] = request.POST.getlist(key)

        try:
            with transaction.atomic():
                yonalish = Yonalishs.objects.create(name=yonalish_nomi, fakultet=fakultet)
                for i, kurs_nomi in enumerate(kurslar):
                    if not kurs_nomi.strip():
                        continue
                    kurs_obj = Kurs.objects.create(yonalish=yonalish, name=kurs_nomi.strip())
                    guruhlar = guruhlar_dict.get(str(i), [])
                    for guruh_nomi in guruhlar:
                        if guruh_nomi.strip():
                            Guruhs.objects.create(kurs=kurs_obj, name=guruh_nomi.strip())
            return redirect(f"/admin_yonalishlar/?fakultet={fakultet.pk}")
        except Exception as e:
            error = f"Xatolik: {str(e)}"
            return render(request, 'asosiy/yonalish_create.html', {'fakultet': fakultet, 'error': error})

    if fakultet:
        return render(request, 'asosiy/yonalish_create.html', {'fakultet': fakultet})
    else:
        form = YonalishForm()
        return render(request, 'asosiy/yonalish_create.html', {'form': form})


@login_required
def yonalish_update(request, pk):
    yonalish = Yonalishs.objects.get(pk=pk)
    if request.method == 'POST':
        form = YonalishForm(request.POST, instance=yonalish)
        if form.is_valid():
            form.save()
            return redirect('admin_yonalishlar')
    else:
        form = YonalishForm(instance=yonalish)
    return render(request, 'asosiy/yonalish_update.html', {'form': form, 'yonalish': yonalish})


@login_required
@require_POST
def yonalish_delete(request, pk):
    yonalish = Yonalishs.objects.get(pk=pk)
    yonalish.delete()
    return redirect('admin_yonalishlar')


# ===== KURS CRUD =====
@login_required
def admin_kurslar(request):
    kurslar = Kurs.objects.all()
    return render(request, 'asosiy/admin_kurslar.html', {'kurslar': kurslar})


@login_required
def kurs_create(request):
    if request.method == 'POST':
        form = KursForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_kurslar')
    else:
        form = KursForm()
    return render(request, 'asosiy/kurs_create.html', {'form': form})


@login_required
def kurs_update(request, pk):
    kurs = Kurs.objects.get(pk=pk)
    if request.method == 'POST':
        form = KursForm(request.POST, instance=kurs)
        if form.is_valid():
            form.save()
            return redirect('admin_kurslar')
    else:
        form = KursForm(instance=kurs)
    return render(request, 'asosiy/kurs_update.html', {'form': form, 'kurs': kurs})


@login_required
@require_POST
def kurs_delete(request, pk):
    kurs = Kurs.objects.get(pk=pk)
    kurs.delete()
    return redirect('admin_kurslar')


# ===== GURUH CRUD =====
@login_required
def admin_guruhlar(request):
    guruhlar = Guruhs.objects.all()
    return render(request, 'asosiy/admin_guruhlar.html', {'guruhlar': guruhlar})


@login_required
def guruh_create(request):
    if request.method == 'POST':
        form = GuruhForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_guruhlar')
    else:
        form = GuruhForm()
    return render(request, 'asosiy/guruh_create.html', {'form': form})


@login_required
def guruh_update(request, pk):
    guruh = Guruhs.objects.get(pk=pk)
    if request.method == 'POST':
        form = GuruhForm(request.POST, instance=guruh)
        if form.is_valid():
            form.save()
            return redirect('admin_guruhlar')
    else:
        form = GuruhForm(instance=guruh)
    return render(request, 'asosiy/guruh_update.html', {'form': form, 'guruh': guruh})


@login_required
@require_POST
def guruh_delete(request, pk):
    guruh = Guruhs.objects.get(pk=pk)
    guruh.delete()
    return redirect('admin_guruhlar')


# ===== OQITUVCHI CRUD =====
@login_required
def admin_oqituvchilar(request):
    oqituvchilar = Users.objects.filter(role='oqituvchi')
    return render(request, 'asosiy/admin_oqituvchilar.html', {'users': oqituvchilar})


@login_required
def oqituvchi_create(request):
    if request.method == 'POST':
        form = OqituvchiForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'oqituvchi'
            user.set_password(form.cleaned_data['password'])
            user.open_password = form.cleaned_data['password']
            user.save()
            return redirect('admin_oqituvchilar')
    else:
        form = OqituvchiForm()
    return render(request, 'asosiy/oqituvchi_create.html', {'form': form})


@login_required
def oqituvchi_update(request, pk):
    user = get_object_or_404(Users, pk=pk)
    if request.method == 'POST':
        form = OqituvchiForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'oqituvchi'
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
                user.open_password = password
            else:
                user.open_password = user.open_password or ''
            user.save()
            return redirect('admin_oqituvchilar')
    else:
        form = OqituvchiForm(instance=user, initial={'password': user.open_password or '', 'password2': user.open_password or ''})
    return render(request, 'asosiy/oqituvchi_update.html', {'form': form, 'user': user})


@login_required
@require_POST
def oqituvchi_delete(request, pk):
    user = get_object_or_404(Users, pk=pk, role='oqituvchi')
    user.delete()
    return redirect('admin_oqituvchilar')


# ===== AJAX YONALISHLAR =====
@csrf_exempt
def get_yonalishlar(request):
    fakultet_id = request.GET.get('fakultet_id')
    yonalishlar = list(Yonalishs.objects.filter(fakultet=fakultet_id).values('id', 'name'))
    return JsonResponse({'yonalishlar': yonalishlar})


# ===== AUTH =====
def chiqish_user(request):
    """Foydalanuvchini tizimdan chiqaradi"""
    logout(request)
    return redirect('kirish')



