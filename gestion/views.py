from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login, authenticate,login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .models import UserProfile, Report, NewsArticle
from .forms import UserProfileForm, ReportForm
from django.views.decorators.http import require_POST

@user_passes_test(lambda u: u.level_of_accreditation >= 2)
def view_requise_accreditation(request):
    # Code de la vue ici
    pass

def logout1(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        return render(request, 'home.html')




#@login_required
def home(request):
    template_name = 'gestion/home.html'
    articles = NewsArticle.objects.all()
    return render(request, template_name, {'articles': articles})

@require_POST
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie.')

            # Utilisez le paramètre 'next' pour rediriger l'utilisateur
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'registration/login.html')


@login_required
def profile(request):
    if isinstance(request.user, AnonymousUser):
        # Gérer le cas où l'utilisateur est anonyme
        # Peut-être rediriger vers une page de connexion
        pass
    else:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            return render(request, 'gestion/profile.html', {'user_profile': user_profile})
        except UserProfile.DoesNotExist:
            # Gérer le cas où le UserProfile n'existe pas pour l'utilisateur
            pass

    # Autres logiques en cas d'erreur ou pour les utilisateurs non connectés
    return render(request, 'gestion/profile.html')


def report_list(request):
    template_name = 'gestion/report_list.html'
    reports = ReportForm.objects.all()
    return render(request, template_name, {'reports': reports})


def report_detail(request, pk):
    template_name = 'gestion/report_detail.html'
    report = get_object_or_404(ReportForm, pk=pk)
    return render(request, template_name, {'report': report})


def report_edit(request, pk):
    template_name = 'gestion/report_edit.html'
    report = get_object_or_404(ReportForm, pk=pk)

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm(instance=report)

    return render(request, template_name, {'form': form, 'report': report})


def report_delete(request, pk):
    template_name = 'gestion/report_delete.html'
    report = get_object_or_404(ReportForm, pk=pk)

    if request.method == 'POST':
        report.delete()
        return redirect('report_list')

    return render(request, template_name, {'report': report})


@login_required
@login_required
def submit_report(request):
    template_name = 'gestion/submit_report.html'
    form = ReportForm()

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            
            # Vérifiez si l'utilisateur est authentifié avant d'assigner le rapport à l'utilisateur
            if request.user.is_authenticated:
                print(f"User authenticated: {request.user}")
                report.user = request.user
                report.save()
                print("Report saved successfully.")

                # Envoie de la notification par e-mail
                subject = 'Notification de soumission de rapport'
                message = 'Votre rapport a été soumis avec succès.'
                from_email = 'isilaflamme@gmail.com'
                to_email = [request.user.email]  # Assurez-vous que l'utilisateur a une adresse e-mail valide

                send_mail(subject, message, from_email, to_email, fail_silently=True)

                return redirect('home')
            else:
                print("User not authenticated. Redirecting to login.")
                # Vous pouvez gérer ici le cas où l'utilisateur n'est pas authentifié
                return redirect('login')  # Redirigez l'utilisateur vers la page de connexion, par exemple

    return render(request, template_name, {'form': form})


def register(request):
    template_name = 'registration/register.html'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            print(f"Utilisateur enregistré: {user.username}")

            # Créer un UserProfile associé à l'utilisateur
            UserProfile.objects.create(user=user, accreditation_level='level1')
            print("UserProfile créé avec succès.")
 

            return redirect('home')  # Changer 'login' par 'home' si vous souhaitez rediriger vers la page d'accueil après l'inscription
    else:
        form = UserCreationForm()

    return render(request, template_name, {'form': form})

@login_required
def tableau(request):
    template_name = 'gestion/tableau.html'

    # Débogage pour vérifier si l'utilisateur est correctement authentifié
    print(f"Utilisateur connecté : {request.user}")

    # Gérer le cas où l'utilisateur est anonyme (non connecté)
    if isinstance(request.user, AnonymousUser):
        # Rediriger vers la page de connexion
        return redirect('login')

    # Filtrer les rapports en fonction de l'utilisateur connecté
    reports = Report.objects.filter(user=request.user)

    return render(request, template_name, {'reports': reports})
