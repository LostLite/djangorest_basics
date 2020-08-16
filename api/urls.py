from django.urls import path
from .views import get_articles, article_detail, ArticleAPIView, GenericAPIView

urlpatterns = [
    # path('article/', get_articles , name='get-articles'), # uses function views
    path('article/', ArticleAPIView.as_view() , name='get-articles'),
    # path('article/<int:pk>', article_detail, name='article-details'), # uses function view
    path('article/<int:pk>', ArticleAPIView.as_view(), name='article-details'),
    path('gen-article/', GenericAPIView.as_view() , name='gen-articles'),
    path('gen-article/<int:id>', GenericAPIView.as_view() , name='gen-articles'),
]