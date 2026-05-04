from django.utils.timezone import now
from dictionaries.models import DictionaryVersion


class VersionService:

    @staticmethod
    def get_version(dictionary_id: int, version_param: str | None):
        qs = DictionaryVersion.objects.filter(dictionary_id=dictionary_id)

        if version_param:
            return qs.filter(version=version_param).first()

        return qs.filter(
            start_date__lte=now().date()
        ).order_by("-start_date").first()
