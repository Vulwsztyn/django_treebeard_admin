from django.contrib import admin
from django.db.models import QuerySet
from django.db.models.expressions import RawSQL
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe

from tree.models import Category
from django.utils.html import format_html
from django import forms
from treebeard.admin import TreeAdmin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        print()
        qs: QuerySet = super(admin.ModelAdmin, self).get_queryset(request)
        print(qs.query)
        return qs \
            .annotate(parent=RawSQL("""
                   select id from tree_category tc where tc.depth="tree_category"."depth"-1 and "tree_category"."path" like tc.path || '%%'
                   """, []
                                    ))

    list_display = (
        'id',
        'path',
        'depth',
        'numchild',
        'name',
        'parent',
    )

    class CategoryForm(ModelForm):
        parent_link = forms.BooleanField(disabled=True)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            url = reverse('admin:tree_category_change', args=[self.instance.parent])
            self.fields['parent_link'].label = format_html('<a href="{}">Link to  Parent</a>', url)

        class Meta:
            model = Category
            fields = '__all__'

    form = CategoryForm

    def parent(self, obj):
        # result = obj.grade_avg
        if obj.parent is None:
            return format_html("<b><i>{}</i></b>", obj.parent)
        url = reverse('admin:tree_category_change', args=[obj.parent])
        return format_html('<a href="{}"> Parent</a>', url)
    # list_select_related = ()
    # raw_id_fields = ("id",)
