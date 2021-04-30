from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins

from ..models import News, Author
from ..serializers import NewsSerializer, NewsCreateSerializer, AuthorSerializer


class NewsListAPIView(APIView):
    def get_permissions(self):
        if self.request.method.lower() == 'post':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user.author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NewsDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method.lower() == 'get':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_object(self, id):
        try:
            return News.objects.get(id=id)
        except News.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

    def put(self, request, pk):
        news = self.get_object(pk)
        if news.author.user == request.user or request.user.is_staff:
            serializer = NewsCreateSerializer(instance=news, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({'error': serializer.errors})
        return Response({'error': "You do not have permission to perform this action"})

    def delete(self, request, pk):
        news = self.get_object(pk)
        if news.author.user == request.user or request.user.is_staff:
            news.delete()
            return Response({'deleted': True})
        return Response({'error': "You do not have permission to perform this action"})


class AuthorViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]
