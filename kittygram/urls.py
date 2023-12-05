from django.urls import path

from cats.views import cat_list
from cats.views import APICat
from cats.views import CatList, CatDetail

urlpatterns = [
   # эндпойнт, реализованный на вью-функции
   path('cats/', cat_list),
   # эндпойнт, реализованный на низкоуровневом вью-классе
   path('cats2/', APICat.as_view()),
   # эндпойнт, реализованный на дженериках
   path('cats3/', CatList.as_view()),
   path('cats3/<int:pk>/', CatDetail.as_view()),
]
