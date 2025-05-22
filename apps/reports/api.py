from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI
from ninja.security import django_auth

from apps.reports.router import router as reportes_router
api = NinjaExtraAPI(csrf=True, urls_namespace="reports")

api.register_controllers(NinjaJWTDefaultController)

# Routers
api.add_router("", reportes_router, tags=["Reportes"])

# Error handling
@api.exception_handler(ObjectDoesNotExist)
def handle_object_does_not_exist(request, exc):
    return api.create_response(
        request,
        {"message": "ObjectDoesNotExist", "detail": str(exc)},
        status=HTTPStatus.NOT_FOUND,
    )