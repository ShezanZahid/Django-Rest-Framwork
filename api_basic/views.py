from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
# Create your views here.


#Generic Class Based API View
#============================
class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin,mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset= Article.objects.all()
    lookup_field = 'id'

    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self,request,id=None):
        return self.create(request)

    def put(self,request,id=None):
        return self.update(request,id)

    def delete(self,request,id = None):
        return self.destroy(request,id)

    
class GenericAPIViewList(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ArticleSerializer
    queryset= Article.objects.all()

    def get(self,request):
        return self.list(request)


#Class Based API View
#======================
class ArticleAPIView(APIView):
    def get(self,request):
        articles = Article.objects.all()
        serializer = ArticleSerializer (articles, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ArticleSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status =status.HTTP_200_OK)
        return Response(serializer.errors,status =status.HTTP_400_BAD_REQUEST)

class ArticalDetails(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
    
        except Article.DoesNotExist:
            return HttpResponse(status = status.HTTP_404_NOT_FOUND)
    
    def get(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer (article)
        return Response(serializer.data)
    
    def put(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST) 
                
    def delete(self,request,id):
        article = self.get_object(id)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


#function based  API View/Reguler Django Views 
#=============================================

# @csrf_exempt
# def artical_list(request):

#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = ArticleSerializer (articles, many=True)
#         return JsonResponse(serializer.data,safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ArticleSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data,status =201)
#         return JsonResponse(serializer.errors,status =400)

# @csrf_exempt
# def artical_details(request,pk):
#     try:
#         article = Article.objects.get(pk=pk)
    
#     except Article.DoesNotExist:
#         return HttpResponse(status = 404)

#     if request.method == 'GET':
#         serializer = ArticleSerializer (article)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = ArticleSerializer(article, data=data)
#         if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors,status = 400) 
            
    
#     elif request.method == 'DELETE':
#         article.delete()
#         return HttpResponse(status = 204)
        


#Rest_Framwork API View
#======================

@api_view(['GET','POST'])
def artical_list(request):

    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer (articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status =status.HTTP_200_OK)
        return Response(serializer.errors,status =status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def artical_details(request,pk):
    try:
        article = Article.objects.get(pk=pk)
    
    except Article.DoesNotExist:
        return HttpResponse(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer (article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST) 
            
    
    elif request.method == 'DELETE':
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


