from decimal import Decimal

from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from application.catalog.games.dtos import (
    CreateGameDTO,
    RateGameDTO,
    RegisterPlaySessionDTO,
    UpdateGameDTO,
    UpdateGameProgressDTO,
)
from application.catalog.games.use_cases import (
    CreateGameUseCase,
    RateGameUseCase,
    RegisterPlaySessionUseCase,
    UpdateGameUseCase,
    UpdateGameProgressUseCase,
)
from domain.shared.exceptions import DomainException
from infrastructure.persistence.django_game_catalog_repository import (
    DjangoGameCatalogRepository,
)

from .models import Game
from .serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Game.objects.filter(user=self.request.user)

    def _repository(self):
        return DjangoGameCatalogRepository()

    def _build_update_dto(self, instance, data):
        """Monta um DTO completo combinando dados atuais e dados recebidos.

        Isso impede que o update padrão do Django grave estados inconsistentes
        ignorando a camada de domínio.
        """
        return UpdateGameDTO(
            user_id=self.request.user.id,
            game_id=instance.id,
            title=data.get("title", instance.title),
            description=data.get("description", instance.description),
            genres=data.get("genres", instance.genres),
            platform=data.get("platform", instance.platform),
            developer=data.get("developer", instance.developer),
            publisher=data.get("publisher", instance.publisher),
            release_year=data.get("release_year", instance.release_year),
            rating=data.get("rating", instance.rating),
            user_rating=data.get("user_rating", instance.user_rating),
            status=data.get("status", instance.status),
            progress=data.get("progress", instance.progress),
            hours_played=data.get("hours_played", instance.hours_played),
            completed_date=data.get("completed_date", instance.completed_date),
            cover_url=data.get("cover_url", instance.cover_url),
        )

    def update(self, request, *args, **kwargs):
        """Atualiza dados do jogo passando pela camada de domínio."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        dto = self._build_update_dto(instance, serializer.validated_data)
        try:
            domain_game = UpdateGameUseCase(self._repository()).execute(dto)
        except DomainException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        model = Game.objects.get(id=domain_game.id, user=request.user)
        return Response(self.get_serializer(model).data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Cria jogos passando pelas regras da camada de domínio."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        dto = CreateGameDTO(
            user_id=request.user.id,
            title=data.get("title"),
            description=data.get("description", ""),
            genres=data.get("genres", ""),
            platform=data.get("platform"),
            developer=data.get("developer", ""),
            publisher=data.get("publisher", ""),
            release_year=data.get("release_year"),
            rating=data.get("rating", Decimal("0")),
            user_rating=data.get("user_rating"),
            status=data.get("status", "wishlist"),
            progress=data.get("progress"),
            hours_played=data.get("hours_played", 0),
            completed_date=data.get("completed_date"),
            cover_url=data.get("cover_url", ""),
        )

        try:
            domain_game = CreateGameUseCase(self._repository()).execute(dto)
        except DomainException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        model = Game.objects.get(id=domain_game.id, user=request.user)
        output = self.get_serializer(model)
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["patch"])
    def update_progress(self, request, pk=None):
        """Atualiza o progresso usando o Domain Service GameProgressService."""
        try:
            progress = int(request.data.get("progress"))
        except (TypeError, ValueError):
            return Response(
                {"detail": "O progresso deve ser informado como número inteiro."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        dto = UpdateGameProgressDTO(
            user_id=request.user.id,
            game_id=int(pk),
            progress=progress,
        )

        try:
            domain_game = UpdateGameProgressUseCase(self._repository()).execute(dto)
        except DomainException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        model = Game.objects.get(id=domain_game.id, user=request.user)
        return Response(self.get_serializer(model).data)

    @action(detail=True, methods=["patch"])
    def register_session(self, request, pk=None):
        """Registra uma sessão de jogo com horas jogadas e progresso opcional."""
        try:
            raw_hours = request.data.get("hours", request.data.get("hours_played"))
            hours = int(raw_hours)
        except (TypeError, ValueError):
            return Response(
                {
                    "detail": "As horas da sessão devem ser informadas como número inteiro."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        raw_progress = request.data.get("progress")
        try:
            progress = int(raw_progress) if raw_progress is not None else None
        except (TypeError, ValueError):
            return Response(
                {"detail": "O progresso deve ser informado como número inteiro."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        dto = RegisterPlaySessionDTO(
            user_id=request.user.id,
            game_id=int(pk),
            hours=hours,
            progress=progress,
        )

        try:
            domain_game = RegisterPlaySessionUseCase(self._repository()).execute(dto)
        except DomainException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        model = Game.objects.get(id=domain_game.id, user=request.user)
        return Response(self.get_serializer(model).data)

    @action(detail=True, methods=["patch"])
    def rate(self, request, pk=None):
        """Registra a avaliação pessoal do usuário respeitando o Value Object GameRating."""
        try:
            rating = Decimal(str(request.data.get("user_rating")))
        except Exception:
            return Response(
                {"detail": "A avaliação deve ser informada como número."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        dto = RateGameDTO(
            user_id=request.user.id,
            game_id=int(pk),
            rating=rating,
        )

        try:
            domain_game = RateGameUseCase(self._repository()).execute(dto)
        except DomainException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        model = Game.objects.get(id=domain_game.id, user=request.user)
        return Response(self.get_serializer(model).data)

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params.get("q", "")
        if query:
            games = self.get_queryset().filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        else:
            games = self.get_queryset()

        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_platform(self, request):
        platform = request.query_params.get("platform", "")
        if platform:
            games = self.get_queryset().filter(platform=platform)
        else:
            games = self.get_queryset()

        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        queryset = self.get_queryset()
        return Response(
            {
                "total_games": queryset.count(),
                "completed": queryset.filter(status="completed").count(),
                "playing": queryset.filter(status="playing").count(),
                "wishlist": queryset.filter(status="wishlist").count(),
                "total_hours": sum([g.hours_played for g in queryset]),
            }
        )
