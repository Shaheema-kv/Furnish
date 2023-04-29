from .models import Categorie

def menu_links(request):
    links = Categorie.objects.all()
    return dict(links=links)