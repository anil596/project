from django.urls import path
from .views import home, history, upload_api, resume_list_api

urlpatterns = [
    path('', home),
    path('history/', history),

    # APIs
    path('api/upload/', upload_api),
    path('api/resumes/', resume_list_api),
]