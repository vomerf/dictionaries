from django.db import models


class Dictionary(models.Model):
    code = models.CharField("Код", max_length=100, unique=True)
    name = models.CharField("Название", max_length=300)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    

class DictionaryVersion(models.Model):
    dictionary = models.ForeignKey(
        "Dictionary",
        on_delete=models.CASCADE,
        related_name="dictionary_versions"
    )
    version = models.CharField("Версия", max_length=50)
    start_date = models.DateField("Дата начала")

    class Meta:
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочников"
        constraints = [
            models.UniqueConstraint(
                fields=["dictionary", "version"],
                name="unique_dictionary_version"
            ),
            models.UniqueConstraint(
                fields=["dictionary", "start_date"],
                name="unique_dictionary_start_date"
            )
        ]
        indexes = [
            models.Index(fields=["dictionary", "-start_date"]),
        ]

    def __str__(self):
        return f"{self.dictionary.code} - {self.version}"


class DictionaryItem(models.Model):
    dictionary_version = models.ForeignKey(
        "DictionaryVersion",
        on_delete=models.CASCADE,
        related_name="dictionary_items"
    )
    code = models.CharField("Код", max_length=100)
    value = models.CharField("Значение", max_length=300)

    class Meta:
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочника"
        constraints = [
            models.UniqueConstraint(
                fields=["dictionary_version", "code"],
                name="unique_item_code_per_version"
            )
        ]
    indexes = [
        models.Index(fields=["dictionary_version", "code"]),
    ]    
    def __str__(self):
        return f"{self.code}: {self.value}"