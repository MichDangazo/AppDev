from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Classroom



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        selected_role = request.POST.get('role')

        if form.is_valid():
            user = form.get_user()

            # Ensure selected role matches user role
            if user.user_type != selected_role:
                return render(request, 'accounts/login.html', {
                    'form': form,
                    'error': 'Incorrect role selected.'
                })

            login(request, user)

            if user.user_type == 'student':
                return redirect('student_dashboard')
            elif user.user_type == 'instructor':
                return redirect('instructor_dashboard')
            elif user.user_type == 'facilities':
                return redirect('facilities_dashboard')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def student_dashboard(request):
    return render(request, 'accounts/student_dashboard.html')

@login_required
def instructor_dashboard(request):
    classrooms = Classroom.objects.filter(instructor=request.user)

    optimal = 0
    attention = 0

    for room in classrooms:
        if room.status() == "optimal":
            optimal += 1
        else:
            attention += 1

    context = {
        'classrooms': classrooms,
        'optimal_count': optimal,
        'attention_count': attention,
        'total_classrooms': classrooms.count(),
    }

    return render(request, 'accounts/instructor_dashboard.html', context)

@login_required
def facilities_dashboard(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

    # Simple mobile detection
    if 'mobile' in user_agent:
        return redirect('login')

    return render(request, 'accounts/facilities_dashboard.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Redirect based on role
            if user.user_type == 'student':
                return redirect('student_dashboard')
            elif user.user_type == 'instructor':
                return redirect('instructor_dashboard')
            elif user.user_type == 'facilities':
                return redirect('facilities_dashboard')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def student_dashboard(request):
    if request.user.user_type != 'student':
        return redirect('login')
    return render(request, 'accounts/student_dashboard.html')
