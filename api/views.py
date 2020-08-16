from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer, ArticleModelSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from  rest_framework import generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# this is a view that uses generic api view
class GenericAPIView(generics.GenericAPIView, 
    mixins.ListModelMixin, mixins.CreateModelMixin, 
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, 
    mixins.DestroyModelMixin):
    serializer_class = ArticleModelSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        
        if id:
            return self.retrieve(request,id)
        
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id):
        return self.update(request,id)

    def delete(self, request, id):
        return self.destroy(request, id)


# This is a class based view
class ArticleAPIView(APIView):
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)

        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, pk=None):
        if pk is None:
            # get list of records
            articles = Article.objects.all()
            serializer = ArticleModelSerializer(articles, many=True)

        else:
            # get single record    
            article = self.get_object(pk)
            serializer = ArticleModelSerializer(article)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return a serializer error message
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleModelSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Respose(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# These are function based views

# You can have functional and class based views.
# With functional views you have to do a lot more to confirm the request methods
@api_view(['GET','POST'])
def get_articles(request):
    if request.method == 'GET':
        articles = Article.objects.all()

        # once we get the result set, we can use the serializer to parse it
        # add many=True to instruct the serialization of a large result set
        serializer = ArticleModelSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # return a serializer error message
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)

