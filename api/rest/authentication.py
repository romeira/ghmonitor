from rest_framework.authentication import SessionAuthentication

# TODO [romeira]: implement csrf {04/06/18 21:13}
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
