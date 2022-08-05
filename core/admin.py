from django.contrib import admin

from core.models import Person, Course, Grade
from django.utils.html import format_html
from django import forms
from django.db.models import Avg


class PersonAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"

    def clean_first_name(self):
        if self.cleaned_data["first_name"] == "Spike":
            raise forms.ValidationError("No Vampires")

        return self.cleaned_data["first_name"]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = ("first_name", "last_name", "courses")
    list_display = ("last_name", "first_name", 'show_average' )
    search_fields = ("last_name__startswith",)
    form = PersonAdminForm

    # def show_average(self, obj):
    #     result = Grade.objects.filter(person=obj).aggregate(Avg("grade"))
    #     return format_html("<b><i>{}</i></b>", result["grade__avg"])

    def show_average(self, obj):
        # result = obj.grade_avg
        return format_html("<b><i>{}</i></b>", obj.grade_avg)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["first_name"].label = "First Name (Humans only!):"
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(grade_avg=Avg("grade__grade"))

    # show_average.short_description = "Average Grade"


from django.urls import reverse
from django.utils.http import urlencode


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "view_students_link")
    list_filter = ("year",)

    def view_students_link(self, obj):
        count = obj.person_set.count()
        url = (
                reverse("admin:core_person_changelist")
                + "?"
                + urlencode({"courses__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Students</a>', url, count)

    view_students_link.short_description = "Students"


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass
