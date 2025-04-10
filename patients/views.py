#patients/views.py
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from datetime import datetime
from django.urls import reverse
from users.models import Doctors , Specialty , Patients
from patients.models import Appointment , Time , Status

User = get_user_model()


@login_required(login_url='/login')
def patient_dashboard(request):
  return render(request,'patients/patient_dashboard.html')


@login_required(login_url='/login')
def my_appointments(request):
  app = Appointment.objects.filter(patient__user = request.user)
  
  filter_status = request.GET.get('filter_status')
  filter_date = request.GET.get('filter_date')
  filter_doctor_name = request.GET.get('filter_doctor_name')

  if filter_status and filter_status != 'All':
    app = app.filter(status__status=filter_status)

  if filter_date:
    app = app.filter(start_date=filter_date)

  if filter_doctor_name:
    app = app.filter(doctor__user__first_name__icontains=filter_doctor_name)

  return render(request, "patients/my_appointments.html", {
    'appointments': app,
    'filter_status': filter_status,
    'filter_date': filter_date,
    'filter_doctor_name': filter_doctor_name
  })
  



@login_required(login_url='/login')
def book_appointment(request):
  specialities = Specialty.objects.all()
  doctors = Doctors.objects.all()
  
  filter_speciality = request.GET.get('filter_speciality')
  filter_city = request.GET.get('filter_city')
  filter_doctor_name = request.GET.get('filter_doctor_name')

  if filter_speciality and filter_speciality != 'All':
    doctors = doctors.filter(specialty__name=filter_speciality)

  if filter_doctor_name:
    doctors = doctors.filter(user__first_name__icontains=filter_doctor_name)

  if filter_city:
    doctors = doctors.filter(user__id_address__city__icontains=filter_city)

  return render(request, "patients/book_appointment.html", {
    'doctors': doctors,
    'specialities': specialities,
    'filter_speciality': filter_speciality,
    'filter_doctor_name': filter_doctor_name,
    'filter_city': filter_city,
  })
  
  # return render(request,'patients/book_appointment.html',{"doctors":doctors})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment, Doctors, Patients, Time, Status

@login_required(login_url='/login')
def patient_confirm_book(request, doctor):
    if request.method == 'POST':
        date = request.POST.get("date")
        summary = request.POST.get("summary")
        description = request.POST.get("description")
        time = request.POST.get("time")
        
        heure = Time.objects.get(time=time)
        doctor = Doctors.objects.get(user__username=doctor)
        patient = Patients.objects.get(user=request.user)
        status = Status.objects.get(status="Waited")

        # Create appointment
        appointment = Appointment.objects.create(
            summary=summary,
            description=description,
            start_date=date,
            time=heure,
            doctor=doctor,
            patient=patient,
            status=status
        )

        # If appointment is successfully created, redirect to payment page
        if appointment:
            return redirect('payment_page', appointment_id=appointment.id)  # Redirect to payment view

    # Render booking confirmation page
    doc = Doctors.objects.get(user__username=doctor)
    if doc:
        times = Time.objects.all()
        return render(request, 'patients/patient_confirm_book.html', {'times': times, 'doctor': doc})

    doctors = Doctors.objects.all()
    return render(request, 'patients/book_appointment.html', {"doctors": doctors})


from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Appointment
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.urls import reverse

@login_required(login_url='/login')
def payment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Create Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': f'Appointment with {appointment.doctor.user.get_full_name()}',
                },
                'unit_amount': 50000,  # ₹500 in paisa
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('my_appointments')),  # ✅ Redirect here after success
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),   # Optional: handle cancel
    )

    return redirect(session.url, code=303)


def payment_success(request):
    return render(request, 'patients/payment_success.html')

def payment_cancel(request):
    return render(request, 'patients/payment_cancel.html')



@login_required(login_url='/login')
def chat_with_doctor(request, doctor_id):
    # Get logged in patient
    try:
        patient = Patients.objects.get(user=request.user)
    except Patients.DoesNotExist:
        messages.error(request, "Invalid access.")
        return redirect('my_appointments')

    # Check if patient has accepted appointment with the doctor
    accepted_appointment = Appointment.objects.filter(
        doctor__user__id=doctor_id,
        patient=patient,
        status__status="Accepted"
    ).first()

    if not accepted_appointment:
        messages.warning(request, "Chat not available. Your appointment is not accepted.")
        return redirect('my_appointments')

    doctor = accepted_appointment.doctor  # Use from appointment

    # Placeholder for chat messages (if implemented)
    chat_messages = []  # Replace with actual model query like ChatMessage.objects.filter(...)

    return render(request, 'users/chat_with_doctor.html', {
        'doctor': doctor,
        'appointment': accepted_appointment,
        'chat_messages': chat_messages,
    })

@login_required(login_url='/login')
def chat_with_patient(request, patient_id):
    try:
        doctor = Doctors.objects.get(user=request.user)
        patient = Patients.objects.get(user__id=patient_id)
    except (Doctors.DoesNotExist, Patients.DoesNotExist):
        messages.error(request, "Invalid access.")
        return redirect('view_appointments')

    # Ensure there's an accepted appointment
    appointment = Appointment.objects.filter(
        doctor=doctor,
        patient=patient,
        status__status="Accepted"
    ).first()

    if not appointment:
        messages.warning(request, "No accepted appointment found for chat.")
        return redirect('view_appointments')

    return render(request, 'doctors/chat_with_patient.html', {
        'patient': patient,
        'appointment': appointment,
        # 'chat_messages': ChatMessage.objects.filter(...),
    })


from django.shortcuts import render

def payment_success(request):
    return render(request, 'patients/payment_success.html')  # create this template or change the name
