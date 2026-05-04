from django.db.models import Exists, OuterRef
from dictionaries.models import DictionaryVersion


class DictionaryService:

    @staticmethod
    def filter_by_date(qs, filter_date):
        versions_subquery = DictionaryVersion.objects.filter(
            dictionary=OuterRef("pk"),
            start_date__lte=filter_date
        )
        return qs.filter(Exists(versions_subquery))
