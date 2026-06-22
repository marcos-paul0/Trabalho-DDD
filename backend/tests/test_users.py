import pytest
from django.contrib.auth.models import User
from apps.users.serializers import UserRegistrationSerializer


pytestmark = pytest.mark.django_db


def test_user_registration_serializer_rejeita_senhas_diferentes():
    serializer = UserRegistrationSerializer(
        data={
            "username": "newuser",
            "email": "new@example.com",
            "password": "pass12345",
            "password_confirm": "pass54321",
        }
    )

    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors


def test_user_registration_serializer_cria_usuario_com_senha_hash():
    serializer = UserRegistrationSerializer(
        data={
            "username": "newuser",
            "email": "new@example.com",
            "password": "pass12345",
            "password_confirm": "pass12345",
        }
    )

    assert serializer.is_valid() is True
    user = serializer.save()

    assert isinstance(user, User)
    assert user.username == "newuser"
    assert user.email == "new@example.com"
    assert user.check_password("pass12345") is True


def test_user_profile_e_criado_automaticamente_no_create_user():
    user = User.objects.create_user(username="u1", password="pass12345")
    assert user.profile.user_id == user.id
