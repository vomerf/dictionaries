from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from dictionaries.models import Dictionary
from dictionaries.serializers import DictionarySerializer, DictionaryElementsSerializer
from http import HTTPStatus
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from dictionaries.services.dictionary import DictionaryService
from dictionaries.services.version import VersionService
from dictionaries.services.item import ItemService


class DictionaryAPIView(APIView):

    @extend_schema(
        tags=["Справочники"],
        summary="Получение списка справочников",
        description=(
            "Возвращает список справочников. "
            "Если указана дата, возвращаются только те, у которых есть версия "
            "с датой начала <= указанной."
        ),
        parameters=[
            OpenApiParameter(
                name="date",
                description="Дата в формате YYYY-MM-DD",
                required=False,
                type=str,
            ),
        ],
        responses=OpenApiResponse(
            response=DictionarySerializer(many=True),
            description="Список справочников"
        ),
        examples=[
            OpenApiExample(
                "Пример ответа",
                value={
                    "dictionaries": [
                        {
                            "id": "1",
                            "code": "ICD-9",
                            "name": "Справочник 1"
                        },
                        {
                            "id": "2",
                            "code": "ICD-10",
                            "name": "Справочник 2"
                        }
                    ]
                },
            )
        ]
    )
    def get(self, request):
        date_str = request.GET.get("date")
        qs = Dictionary.objects.all()
        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"error": "Некорректный формат даты"}, status=HTTPStatus.BAD_REQUEST
                )
            qs = DictionaryService.filter_by_date(qs, date)

        serializer = DictionarySerializer(qs, many=True)
        return Response(
            {
                "dictionaries": serializer.data
            }
        )


class DictionaryElementsView(APIView):

    @extend_schema(
        tags=["Справочники"],
        summary="Получение элементов справочника",
        description=(
            "Возвращает элементы версии справочника. "
            "Если версия не указана, используется текущая версия "
            "(с максимальной датой начала, не превышающей текущую дату)."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="ID справочника",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="version",
                description="Версия справочника",
                required=False,
                type=str,
            ),
        ],
        responses=OpenApiResponse(
            response=DictionaryElementsSerializer,
            description="Список элементов"
        ),
        examples=[
            OpenApiExample(
                "Пример ответа",
                value={
                    "elements": [
                        {"code": "J00", "value": "Насморк"},
                        {"code": "J01", "value": "Синусит"}
                    ]
                },
            )
        ]
    )
    def get(self, request, id):
        version_param = request.GET.get("version")

        version = VersionService.get_version(id, version_param)
        if not version:
            return Response({"elements": []})

        items = ItemService.get_items_for_version(version)
        serializer = DictionaryElementsSerializer(
            {
                "elements": items
            }
        )

        return Response(serializer.data)


class DictionaryCheckElementView(APIView):

    @extend_schema(
        tags=["Справочники"],
        summary="Проверка элемента справочника",
        description=(
            "Проверяет, существует ли элемент с заданным кодом и значением "
            "в указанной версии справочника. "
            "Если версия не указана, используется текущая версия."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="ID справочника",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="code",
                description="Код элемента",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="value",
                description="Значение элемента",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="version",
                description="Версия справочника",
                required=False,
                type=str,
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Результат проверки",
                response=dict
            ),
            400: OpenApiResponse(description="Некорректные параметры"),
        },
        examples=[
            OpenApiExample(
                "Элемент найден",
                value={"exists": True},
            ),
            OpenApiExample(
                "Элемент не найден",
                value={"exists": False},
            ),
        ]
    )
    def get(self, request, id):
        code = request.GET.get("code")
        value = request.GET.get("value")
        version_param = request.GET.get("version")

        if not code or not value:
            return Response(
                {"error": "Код и значение обязательны для проверки"},
                status=HTTPStatus.BAD_REQUEST
            )
        version = VersionService.get_version(id, version_param)
        if not version:
            return Response(
                {"exists": False, "error": "Версия справочника не найдена"},
                status=HTTPStatus.NOT_FOUND
            )
        exists = ItemService.check_item_exists(version, code, value)
        return Response({"exists": exists})
