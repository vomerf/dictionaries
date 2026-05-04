from django.contrib import admin
from dictionaries.models import Dictionary, DictionaryVersion, DictionaryItem
from django.db.models import OuterRef, Subquery
from django.utils import timezone


class DictionaryVersionInline(admin.TabularInline):
    model = DictionaryVersion
    extra = 1


class DictionaryItemInline(admin.TabularInline):
    model = DictionaryItem
    extra = 1
    fields = ("code", "value")


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = (
        "id", "code", "name", "get_current_version", "get_current_start_date"
    )
    search_fields = ("code", "name")
    inlines = [DictionaryVersionInline]

    def get_queryset(self, request):
        today = timezone.now().date()
        qs = super().get_queryset(request)

        latest_version_qs = (
            DictionaryVersion.objects
            .filter(dictionary=OuterRef("pk"), start_date__lte=today)
            .order_by("-start_date")
        )

        return qs.annotate(
            current_version=Subquery(latest_version_qs.values("version")[:1]),
            current_start_date=Subquery(latest_version_qs.values("start_date")[:1]),
        )

    def get_current_version(self, obj):
        return obj.current_version or "-"
    get_current_version.short_description = "Текущая версия"

    def get_current_start_date(self, obj):
        return obj.current_start_date or "-"
    get_current_start_date.short_description = "Дата начала"


@admin.register(DictionaryVersion)
class DictionaryVersionAdmin(admin.ModelAdmin):
    list_display = ("version", "start_date", "get_dictionary_code", "get_dictionary_name")
    inlines = [DictionaryItemInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("dictionary")

    def get_dictionary_code(self, obj):
        return obj.dictionary.code
    get_dictionary_code.short_description = "Код справочника"
    get_dictionary_code.admin_order_field = "dictionary__code"

    def get_dictionary_name(self, obj):
        return obj.dictionary.name
    get_dictionary_name.short_description = "Наименование справочника"
    get_dictionary_name.admin_order_field = "dictionary__name"


@admin.register(DictionaryItem)
class DictionaryItemAdmin(admin.ModelAdmin):
    list_display = ("dictionary_version", "code", "value")
    list_select_related = ("dictionary_version",)
