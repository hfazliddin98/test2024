from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from quiz.models import Natijas, Mavzus
from users.models import Fakultets, Yonalishs
from django.db.models import Count, Avg, Max, F, ExpressionWrapper, DecimalField, Case, When, Value
from django.db.models.functions import Round

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
    if fakultet_id:
        selected_fakultet = Fakultets.objects.get(pk=fakultet_id)
        yonalishlar = Yonalishs.objects.filter(fakultet_id=fakultet_id)
    
    # Count statistics - filtered results count and total count
    filtered_natijalar_count = natijalar_query.count()
    natijalar_count = filtered_natijalar_count  # Use filtered count for display
    
    # Debug information
    debug_info = {
        'received_fakultet_id': fakultet_id,
        'filter_applied': bool(fakultet_id and fakultet_id.strip()),
        'query_count': filtered_natijalar_count,
    }
    
    # Get filtered talaba count if fakultet filter is applied
    talabalar_count = natijalar_query.values('talaba').distinct().count() if fakultet_id else Natijas.objects.values('talaba').distinct().count()
    
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
        'debug_info': debug_info,
        'all_mavzular': all_mavzular,
        'student_results': student_results
    })
