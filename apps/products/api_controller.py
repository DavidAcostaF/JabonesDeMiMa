from django.core.handlers.wsgi import WSGIRequest
from ninja_extra import api_controller, permissions, route
from ninja_extra.pagination import PaginatedResponseSchema, paginate
from ninja_jwt.authentication import JWTAuth
from .models import Product
from .schemas import ProductResponseSchema
@api_controller(
    "/products",
    tags=["Products"],
    auth=JWTAuth(),
    permissions=[permissions.IsAuthenticated],
)
class ProductsController:
    model = Product

    @route.get("/{product_id}", response={200: ProductResponseSchema})
    def retrieve_product(self, request: WSGIRequest, product_id: int):
        return 200 , self.model.objects.get(id = product_id)