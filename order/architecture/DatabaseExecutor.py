from product.models import Product


class DatabaseExecutor:
    @classmethod
    def get_product_by_id(cls, product_id: int):
        return Product.objects.get(fid=product_id)

    @classmethod
    def create_order(cls, product: Product, amount):
        Product.amount = amount
