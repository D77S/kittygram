from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cat
from .serializers import CatSerializer


# декоратор @api_view объявляет функцию - вью-функцией работы с api
# в нем указываются методы, только которые и являются допустимыми,
# при попытке других - возвращается ошибка 405.
@api_view(['GET', 'POST', 'PUT', 'PATCH'])
def cat_list(request):

    #  если метод в запросе метод POST (добавить запись), то...
    if request.method == 'POST':
        # Создать объект сериализатора, передав ему в data -
        # данные из реквеста.
        # Причем, если передается/ожидается единственный объект...
        # {
        #  "name": "Стёпа",
        #  "color": "белый",
        #  "birth_year": 1971
        # }
        # ... то параметр many не указывается, либо в False.
        # А если передается/ожидается несколько объъектов (список словарей)...
        # [
        #  {
        #   "name": "Стёпа",
        #   "color": "белый",
        #   "birth_year": 1971
        #  },
        #  {
        #   "name": "Мурка",
        #   "color": "рыжий",
        #   "birth_year": 2010
        #  },
        #  {
        #   "name": "Пушок",
        #   "color": "чёрный",
        #   "birth_year": 2018
        #  }
        # ]
        # ... то надо указать many=True.
        serializer = CatSerializer(data=request.data, many=True)
        # вызвать метод .is_valid сериализатора.
        # если он вернет True, т.е. данные валидны, то...
        if serializer.is_valid():
            #  ... создать новый объект БД. (НЕ ОБНОВИТЬ ИМЕЮЩИЙСЯ!)
            serializer.save()
            # Вызвать метод .data объекта сериализатора, в котором будет
            # только что записанный в базу объект сериализации,
            # и вернуть ответ пользователю. С нужным кодом ответа.
            # Возвращаются специальный объект класса Response;
            # в этот объект в качестве аргумента передаётся Python-словарь,
            # данные из которого и должны быть отправлены
            # в ответ на запрос в JSON формате.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #  если метод в запросе метод PUT (полное обновление записи), то...
    if request.method in ('PUT', 'PATCH'):
        # Создать объект сериализатора, передав ему в data -
        # данные из реквеста.
        # Причем, если передается/ожидается единственный объект...
        # {
        #  "name": "Стёпа",
        #  "color": "белый",
        #  "birth_year": 1971
        # }
        # ... то параметр many не указывается, либо в False.
        # А если передается/ожидается несколько объъектов (список словарей)...
        # [
        #  {
        #   "name": "Стёпа",
        #   "color": "белый",
        #   "birth_year": 1971
        #  },
        #  {
        #   "name": "Мурка",
        #   "color": "рыжий",
        #   "birth_year": 2010
        #  },
        #  {
        #   "name": "Пушок",
        #   "color": "чёрный",
        #   "birth_year": 2018
        #  }
        # ]
        # ... то надо указать many=True.

        # Для метода PUT (полное обновление) еще надо задать
        # тот объект БД, который вообще-то требуется обновить...
        cat = Cat.objects.get(id=3)
        # ... и указать его первым параметром при создании объекта с-ра.

        # Внимание! PUT - метод полного обновления
        # (ожидает полный набор полей),
        # PATCH - частичного обновления.
        if request.method == 'PUT':
            serializer = CatSerializer(cat, data=request.data, many=False)
        if request.method == 'PATCH':
            serializer = CatSerializer(
                cat,
                data=request.data,
                many=False,
                partial=True)  # !!!!!

        # вызвать метод .is_valid сериализатора.
        # если он вернет True, т.е. данные валидны, то...
        if serializer.is_valid():
            #  ... обновить объект БД. (НЕ СОЗДАТЬ!)
            #  На то, что обновить а не создать, указывает
            #  наличие объекта модели при создании сериализатора выше.
            serializer.save()
            # Вызвать метод .data объекта сериализатора, в котором будет
            # только что записанный в базу объект сериализации,
            # и вернуть ответ пользователю. С нужным кодом ответа.
            # Возвращаются специальный объект класса Response;
            # в этот объект в качестве аргумента передаётся Python-словарь,
            # данные из которого и должны быть отправлены
            # в ответ на запрос в JSON формате.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #  ..., а если в запросе метод GET, то...
    #  запросить из базы кверисет со всеми объектами модели
    cats = Cat.objects.all()
    #  создать объект сериализатора, передав в него
    #  только что созданный кверисет,
    #  а если объектов будет набор, то параметр many надо в True.
    serializer = CatSerializer(cats, many=True)
    # Вызвать метод .data объекта сериализатора, в котором будет
    # только что взятый из базы объект сериализации,
    # и вернуть ответ пользователю.
    # Возвращаются специальный объект класса Response;
    # в этот объект в качестве аргумента передаётся Python-словарь,
    # данные из которого и должны быть отправлены
    # в ответ на запрос в JSON формате.
    return Response(serializer.data)


class APICat(APIView):
    #  Все операции CRUD при использовании view-классов
    #  принято разделять на 2 группы:
    #  в одном view-классе описывается создание нового объекта и
    #  запрос всех объектов (например класс APICat),
    #  а в другом классе — получение/изменение/удаление определённого объекта.
    #
    #  Если view-класс унаследован от класса APIView,
    #  то при получении GET-запроса в классе будет вызван метод get(),
    #  а при получении POST-запроса — метод post().
    #  Такие методы описаны для всех типов запросов, но по умолчанию
    #  эти методы не выполняют никаких действий,
    #  их нужно описывать самостоятельно.
    #  def get(self, request):
    #      ...
    #
    #  def post(self, request):
    #      ...
    #
    #  def put(self, request):
    #      ...
    #
    #  def patch(self, request):
    #      ...
    #
    #  def delete(self, request):
    #      ...
    def get(self, request):
        cats = Cat.objects.all()
        serializer = CatSerializer(cats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  дженерик-классы:
#  RetrieveAPIView — возвращает один объект (обрабатывает только GET-запросы);
#  CreateAPIView — создаёт новый объект (обрабатывает только POST-запросы);
#  UpdateAPIView — изменяет объект (обрабатывает только PUT- и PATCH-запросы);
#  DestroyAPIView — удаляет объект (обрабатывает только DELETE-запросы)
class CatList(generics.ListCreateAPIView):
    #  комбинированный дженерик-класс ListCreateAPIView:
    #  - на GET-запрос он возвращает всю коллекцию объектов
    #  - на POST-запрос он создаст новую запись в БД
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class CatDetail(generics.RetrieveUpdateDestroyAPIView):
    # комбинированный дженерик-класс RetrieveUpdateDestroyAPIView:
    # его работа — возвращать, обновлять или удалять объекты модели по одному.
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
