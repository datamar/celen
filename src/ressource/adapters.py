from allauth.account.adapter import DefaultAccountAdapter

class KwargsAccountAdapter(DefaultAccountAdapter):

    def should_send_confirmation_mail(self, request, email_address, signup):
        # On envoie l'email uniquement si signup=True
        return signup
