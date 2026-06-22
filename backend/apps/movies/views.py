from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Movie.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params.get("q", "")
        if query:
            movies = self.get_queryset().filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        else:
            movies = self.get_queryset()

        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_status(self, request):
        status = request.query_params.get("status", "")
        if status:
            movies = self.get_queryset().filter(status=status)
        else:
            movies = self.get_queryset()

        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        queryset = self.get_queryset()
        return Response(
            {
                "total_movies": queryset.count(),
                "watched": queryset.filter(status="watched").count(),
                "watching": queryset.filter(status="watching").count(),
                "wishlist": queryset.filter(status="wishlist").count(),
            }
        )
