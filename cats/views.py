from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cat
from .serializers import CatSerializer


# декоратор @api_view объявляет функцию - вью-функцией работы с api
# в нем указываются методы, только которые и являются допустимыми,
# при попытке других - возвращается ошибка 5**.
@api_view(['GET', 'POST'])
def cat_list(request):
    #  если метод в запросе метод POST, то...
    if request.method == 'POST':
        # создать объект сериализатора, передав ему в data - данные из реквеста
        serializer = CatSerializer(data=request.data)
        # вызвать метод .is_valid сериализатора.
        # если он вернет True, т.е. данные валидны, то...
        if serializer.is_valid():
            #  ... создать новый объект БД. (НЕ ОБНОВИТЬ ИМЕЮЩИЙСЯ!)
            serializer.save()
            # Вызвать метод .data объекта сериализатора, в котором будет
            # только что записанный в базу объект сериализации,
            # и вернуть ответ пользователю. С нужным кодом ответа.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #  ..., а если в запросе метод GET, то...
    #  запросить из базы кверисет со всеми объектами модели
    cats = Cat.objects.all()
    #  создать объект сериализатора, передав в него
    #  только что созданный кверисет, а также параметр many в True.
    serializer = CatSerializer(cats, many=True)
    # Вызвать метод .data объекта сериализатора, в котором будет
    # только что взятый из базы объект сериализации,
    # и вернуть ответ пользователю.
    return Response(serializer.data)
