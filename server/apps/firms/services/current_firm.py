from apps.firms.models import LawFirm

def get_default_firm():
    return LawFirm.objects.first()