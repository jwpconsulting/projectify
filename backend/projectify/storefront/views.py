from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def accessibility(request: HttpRequest):
    return render(request, 'storefront/accessibility.html')
def contact_us(request: HttpRequest):
    return render(request, 'storefront/contact_us.html')
def credits(request: HttpRequest):
    return render(request, 'storefront/credits.html')
def ethicalads(request: HttpRequest):
    return render(request, 'storefront/ethicalads.html')
def free_software(request: HttpRequest): pass
def pricing(request: HttpRequest) -> HttpResponse: pass
def privacy(request: HttpRequest) -> HttpResponse: pass
def security_disclose(request: HttpRequest) -> HttpResponse: pass
def escurity_general(request: HttpRequest) -> HttpResponse: pass
def solutions_index(request: HttpRequest) -> HttpResponse: pass
def solutions_detail(request: HttpRequest, page: str) -> HttpResponse: pass
def tos(request: HttpRequest) -> HttpResponse: pass
