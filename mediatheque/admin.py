from django.contrib import admin

from mediatheque.models import Media, Borrow, Member


class MediaAdmin(admin.ModelAdmin):
    list_display = ['type', 'title', 'author']
    list_filter = ('type',)

admin.site.register(Media, MediaAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ['lastname', 'firstname']
    list_filter = ('lastname', 'firstname')

admin.site.register(Member, MemberAdmin)

class BorrowAdmin(admin.ModelAdmin):
    list_display = ['id', 'member_name', 'media_title', 'borrowing_date', 'return_date']

    def member_name(self, obj):
        return f"{obj.member.lastname} {obj.member.firstname}"
    member_name.short_description = 'Emprunteur'

    def media_title(self, obj):
        return f"{obj.media.title} // {obj.media.type}"
    media_title.short_description = 'Titre // Type'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "media":
            kwargs["queryset"] = Media.objects.all().order_by("title", "type")
        if db_field.name == "member":
            kwargs["queryset"] = Member.objects.all().order_by("lastname", "firstname")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Borrow, BorrowAdmin)

