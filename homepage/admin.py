from django.contrib import admin
from .models import (
    Announcement, MeetingPlace, Event, LinkGroup, Link,
    QuestionGroup, Question,
)
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
class AnnouncementAdmin(MarkdownxModelAdmin):
    def title(obj):
        return obj.title

    def text(obj):
        return obj.text

    def date_created(obj):
        return obj.date_created

    list_display = ('title', 'text', 'date_created', 'expiration_date')


class MeetingPlaceAdmin(MarkdownxModelAdmin):
    list_display = ('venue_name', 'address', 'city', 'state', 'zip_code')


class EventAdmin(MarkdownxModelAdmin):
    pass


class LinkGroupAdmin(MarkdownxModelAdmin):
    list_display = ('name',)


class LinkAdmin(MarkdownxModelAdmin):
    list_display = ('name', 'url', 'description', 'group')


class QuestionGroupAdmin(MarkdownxModelAdmin):
    list_display = ('name',)


class QuestionAdmin(MarkdownxModelAdmin):
    list_display = ('question_text', 'group')


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(MeetingPlace, MeetingPlaceAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(LinkGroup, LinkGroupAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(Question, QuestionAdmin)
