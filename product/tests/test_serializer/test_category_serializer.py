import pytest
from product.serializers.category_serializer import CategorySerializer
from product.models.category import Category

@pytest.mark.django_db
def test_category_serializer():
    # Arrange - Criando uma instância de Category (no banco de teste)
    category = Category.objects.create(
        title="Aventura",
        slug="aventura",
        description="Categoria de livros de aventura",
        active=True,
    )

    # Act - Serializando o objeto
    serializer = CategorySerializer(instance=category)

    # Assert - Verificando se os dados estão corretos
    expected_data = {
        "title": "Aventura",
        "slug": "aventura",
        "description": "Categoria de livros de aventura",
        "active": True,
    }

    assert serializer.data == expected_data