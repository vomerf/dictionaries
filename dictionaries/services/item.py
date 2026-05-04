from dictionaries.models import DictionaryItem


class ItemService:

    @staticmethod
    def get_items_for_version(version):
        return version.dictionary_items.all()

    @staticmethod
    def check_item_exists(version, code, value):
        return DictionaryItem.objects.filter(
            dictionary_version=version,
            code=code,
            value=value
        ).exists()
