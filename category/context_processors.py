from .models import category

def menu_list(request):
    links = category.objects.all()
    return dict(links=links)