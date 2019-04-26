from django.contrib import admin
from .models import (
    Announcement, MeetingPlace, Event, LinkGroup, Link,
    QuestionGroup, Question,
)


# Register your models here.
class AnnouncementAdmin(admin.ModelAdmin):
    def title(obj):
        return obj.title

    def text(obj):
        return obj.text

    def date_created(obj):
        return obj.date_created

    list_display = ('title', 'text', 'date_created')


class MeetingPlaceAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'address', 'city', 'state', 'zip_code')


class EventAdmin(admin.ModelAdmin):
    pass


class LinkGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'description', 'group')


class QuestionGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'group')


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(MeetingPlace, MeetingPlaceAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(LinkGroup, LinkGroupAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(Question, QuestionAdmin)
