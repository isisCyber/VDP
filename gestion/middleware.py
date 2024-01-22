from django.shortcuts import redirect
from django.urls import reverse

class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Code à exécuter avant que la vue ne soit appelée
        if request.user.is_authenticated:
            # Vérifier le niveau d'accréditation de l'utilisateur
            if not self.check_authorization(request.user):
                # Rediriger l'utilisateur s'il n'est pas autorisé
                return redirect(reverse('page_non_autorisee'))

        return response

    def check_authorization(self, user):
        # Implémentez la logique de vérification de l'accréditation ici
        # Par exemple, vérifiez si l'utilisateur a le niveau d'accréditation nécessaire
        return user.level_of_accreditation >= 2
