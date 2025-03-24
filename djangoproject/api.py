
from django.core.exceptions import ObjectDoesNotExist
from ninja.errors import ValidationError
from ninja_extra import NinjaExtraAPI

# Security / Authentication endpoints
from ninja_jwt.controller import NinjaJWTDefaultController
from apps.products.api_controller import ProductsController
# Registration of API Controllers
api = NinjaExtraAPI(csrf=False)  # CSRF Protection

api.register_controllers(ProductsController)