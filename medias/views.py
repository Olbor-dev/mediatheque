from django.views.generic import ListView
from mediatheque.models import Media, Borrow

class MediaListView(ListView):
    model = Media
    template_name = "medias_list.html"
    context_object_name = "medias"

    def get_queryset(self):
        # On récupère tous les médias
        queryset = Media.objects.all()

        # On annote chaque média avec un booléen "is_borrowed"
        for media in queryset:
            media.is_borrowed = Borrow.objects.filter(
                media=media,
                return_date__isnull=True
            ).exists()
        return queryset


