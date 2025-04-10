#patients/models.py
from django.db import models
from users.models import Patients ,Doctors

class Time(models.Model):
    time = models.CharField(max_length=10)
    class Meta:
        verbose_name = "Time"
        verbose_name_plural = "Times"
    def __str__(self):
        return self.time
    
class Status(models.Model):
    status =  models.CharField(max_length=20) 
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"
    def __str__(self):
        return self.status

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, )
    summary = models.TextField()
    description = models.TextField()
    start_date = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, )
    time = models.ForeignKey(Time, on_delete=models.CASCADE, default=1)
    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
    def __str__(self):
        return self.summary
    

# models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.message}"
