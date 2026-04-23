from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Director, Service, Project, CompanyInfo, ContactMessage, ClientAccount
from .forms import ContactForm, RegistrationForm

def home(request):
    directors = Director.objects.filter(is_active=True)[:4]
    services = Service.objects.all()[:6]
    featured_projects = Project.objects.filter(is_featured=True)[:6]
    company_info = CompanyInfo.objects.first()
    
    context = {
        'directors': directors,
        'services': services,
        'featured_projects': featured_projects,
        'company_info': company_info,
    }
    return render(request, 'core/home.html', context)

def about(request):
    directors = Director.objects.filter(is_active=True)
    company_info = CompanyInfo.objects.first()
    return render(request, 'core/about.html', {'directors': directors, 'company_info': company_info})

def services(request):
    all_services = Service.objects.all()
    return render(request, 'core/services.html', {'services': all_services})

def portfolio(request):
    projects = Project.objects.all()
    return render(request, 'core/portfolio.html', {'projects': projects})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email notification
            try:
                send_mail(
                    f'Contact Form: {contact.subject}',
                    f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}",
                    contact.email,
                    ['admin@yourcompany.com'],  # Change to your email
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(request, 'Thank you! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    company_info = CompanyInfo.objects.first()
    return render(request, 'core/contact.html', {'form': form, 'company_info': company_info})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create client account
            ClientAccount.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            login(request, user)
            messages.success(request, 'Registration successful! Welcome!')
            return redirect('client_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def client_dashboard(request):
    try:
        client_account = request.user.clientaccount
    except ClientAccount.DoesNotExist:
        return redirect('register')
    
    return render(request, 'core/dashboard.html', {'client_account': client_account})

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')