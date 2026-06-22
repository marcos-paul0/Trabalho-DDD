from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Rating
from .serializers import RatingSerializer


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if rating already exists
        content_type = serializer.validated_data["content_type"]
        object_id = serializer.validated_data["object_id"]

        existing_rating = Rating.objects.filter(
            user=request.user, content_type=content_type, object_id=object_id
        ).first()

        if existing_rating:
            # Update existing rating
            for attr, value in serializer.validated_data.items():
                setattr(existing_rating, attr, value)
            existing_rating.save()
            return Response(RatingSerializer(existing_rating).data)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
