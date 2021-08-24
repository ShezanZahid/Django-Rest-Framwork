from django.urls import path
from .views import artical_list,artical_details,ArticleAPIView,ArticalDetails,GenericAPIView,GenericAPIViewList

urlpatterns=[
    # path('article/',artical_list),
    # path('details/<int:pk>',artical_details),
    path('article/',ArticleAPIView.as_view()),
    # path('details/<int:id>',ArticalDetails.as_view()),
    path('generic/article/<int:id>/',GenericAPIView.as_view()),
    path('generic/article/',GenericAPIViewList.as_view()),
    

]