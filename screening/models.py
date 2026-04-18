from django.db import models

class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    score = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
