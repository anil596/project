from django.shortcuts import render, redirect
from .forms import ResumeForm, RegisterForm
from .models import Resume
from .utils import extract_text_from_pdf, calculate_score
from django.contrib.auth import authenticate, login, logout

# API imports
from rest_framework.decorators import api_view
from rest_framework.response import Response


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = request.FILES['file']
            job_desc = form.cleaned_data['job_description']

            text = extract_text_from_pdf(resume_file)
            score = calculate_score(text, job_desc)

            Resume.objects.create(file=resume_file, score=score)

            return render(request, 'result.html', {'score': score})
    else:
        form = ResumeForm()

    return render(request, 'upload.html', {'form': form})


def history(request):
    resumes = Resume.objects.all()
    return render(request, 'history.html', {'resumes': resumes})


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('login')

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


# ✅ API 1: Upload Resume
@api_view(['POST'])
def upload_api(request):
    file = request.FILES.get('file')
    job_desc = request.data.get('job_description')

    if not file or not job_desc:
        return Response({"error": "Missing data"}, status=400)

    text = extract_text_from_pdf(file)
    score = calculate_score(text, job_desc)

    return Response({"score": score})


# ✅ API 2: Get all resumes
@api_view(['GET'])
def resume_list_api(request):
    resumes = Resume.objects.all()

    data = []
    for r in resumes:
        data.append({
            "file": r.file.url if r.file else "",
            "score": r.score,
            "uploaded_at": r.uploaded_at
        })

    return Response(data)