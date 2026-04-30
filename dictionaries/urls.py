from django.urls import path
# from dictionaries.views import DictionaryListView
from dictionaries.views import DictionaryAPIView, DictionaryCheckElementView, DictionaryElementsView

urlpatterns = [
    path("", DictionaryAPIView.as_view(), name="dictionary-list"),
    path("<int:id>/elements", DictionaryElementsView.as_view(), name="dictionaryelements-list"),
    path("<int:id>/check-element", DictionaryCheckElementView.as_view(), name="dictionarycheckelement"),
]