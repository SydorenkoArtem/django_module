from order.architecture.DatabaseExecutor import DatabaseExecutor


class OrderProcessor:
    @classmethod
    def create_order(cls, product_id: int, quantity: int):
        product = DatabaseExecutor.get_product_by_id(product_id)

        if product.amount < quantity:
            return ...

        if not DatabaseExecutor.create_order(product, quantity):
            return ...

        return ...