import pytest
from order.serializers import OrderSerializer
from order.factories import OrderFactory
from product.factories import ProductFactory

@pytest.mark.django_db
def test_order_serializer_with_products():
    # Cria dois produtos falsos
    product1 = ProductFactory(price=10.00)
    product2 = ProductFactory(price=15.00)

    # Cria um pedido com esses dois produtos
    order = OrderFactory(product=[product1, product2])

    # Serializa o pedido
    serializer = OrderSerializer(order)

    # Verifica se os produtos estão no serializer
    assert len(serializer.data["product"]) == 2

    # Verifica se o total está correto
    assert serializer.data["total"] == 25.00
