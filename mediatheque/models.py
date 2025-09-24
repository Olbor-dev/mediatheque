from django.core.exceptions import ValidationError
from django.db import models
#from django.http.request import MediaType
from django.utils import timezone

class Media(models.Model):
    class MediaType(models.TextChoices):
        BOOK = 'book', 'Livre'
        CD = 'cd', 'CD'
        DVD ='dvd', 'DVD'
        BG = 'board-game', 'Jeu de plateau'

    type = models.CharField(max_length=50, choices=MediaType.choices, null=False, blank=False)
    title = models.CharField(max_length=250, null=False, blank=False)
    author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.title} ({self.type})"


class Member(models.Model):
    lastname = models.CharField(max_length=100, null=False, blank=False)
    firstname = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.lastname} {self.firstname}"


class Borrow(models.Model):
    media = models.ForeignKey(Media, null=False, blank=False, on_delete=models.CASCADE)
    member = models.ForeignKey(Member,null=False, blank=False, on_delete=models.CASCADE)
    borrowing_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)

    def clean(self):

        # Exclusion des jeux de plateau des "empruntables"
        if self.media and self.media.type == Media.MediaType.BG:
            raise ValidationError("Les jeux de plateau ne sont pas empruntables.")

        # Interdit un emprunt multiple d'un média déjà sorti
        already_borrowed = Borrow.objects.filter(
            media=self.media,
            return_date__isnull=True
        ).exclude(pk=self.pk).exists()
        if already_borrowed:
            raise ValidationError(f"Le média « {self.media.title} » est déjà emprunté.")

        # Limite le nombre à 3 emprunts
        active_borrows_count = Borrow.objects.filter(
            member=self.member,
            return_date__isnull=True
        ).exclude(pk=self.pk).count()
        if active_borrows_count >= 3:
            raise ValidationError(f"{self.member} a déjà 3 emprunts !")

        # Bloque l'emprunt pour le membre qui a un emprunt depuis + de 7 jours
        too_old_borrow = Borrow.objects.filter(
            member=self.member,
            return_date__isnull=True
        ).exclude(pk=self.pk).exists()
        if too_old_borrow:
            raise ValidationError(f"{self.member} a un emprunt depuis plus de 7 jours")

    def __str__(self):
        return f"{self.member.lastname} emprunte '{self.media.title}'"