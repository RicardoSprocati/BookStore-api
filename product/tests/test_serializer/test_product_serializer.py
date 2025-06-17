import pytest
from product.models.product import Product, Category
from product.serializers.product_serializer import ProductSerializer

@pytest.mark.django_db
def test_product_serializer_with_categories():
    # Arrange - cria categorias
    category1 = Category.objects.create(
        title="Ficção", slug="ficcao", description="Livros de ficção", active=True
    )
    category2 = Category.objects.create(
        title="Suspense", slug="suspense", description="Livros de suspense", active=True
    )

    # Cria produto e associa categorias
    product = Product.objects.create(
        title="Livro X",
        description="Um ótimo livro",
        price=59,
        active=True
    )
    product.category.set([category1, category2])

    # Act - Serializa o produto
    serializer = ProductSerializer(instance=product)

    # Assert - Verifica os dados
    expected_data = {
        "title": "Livro X",
        "description": "Um ótimo livro",
        "price": 59, 
        "active": True,
        "category": [
            {
                "title": "Ficção",
                "slug": "ficcao",
                "description": "Livros de ficção",
                "active": True
            },
            {
                "title": "Suspense",
                "slug": "suspense",
                "description": "Livros de suspense",
                "active": True
            },
        ]
    }

    assert serializer.data == expected_data