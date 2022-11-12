import asyncio
import json

import jwt
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.decorators import sync_and_async_middleware

from core.auth.models import RlcUser, UserProfile
from core.models import LoggedPath
from core.seedwork.api_layer import ErrorResponse

__all__ = [
    "custom_debug_toolbar_middleware",
    "logging_middleware",
    "authentication_middleware",
]


@sync_and_async_middleware
def custom_debug_toolbar_middleware(get_response):
    def create_response(request, response):
        if "debug" in request.GET and response["content-type"] == "application/json":
            content = json.dumps(json.loads(response.content), sort_keys=True, indent=2)
            new_response = HttpResponse(
                "<html><body><pre>{}</pre></body></html>".format(content)
            )
            return new_response
        return response

    if asyncio.iscoroutinefunction(get_response):

        async def middleware(request):
            response = await get_response(request)
            response = create_response(request, response)
            return response

    else:

        def middleware(request):
            response = get_response(request)
            response = create_response(request, response)
            return response

    return middleware


@sync_and_async_middleware
def logging_middleware(get_response):
    def create_data(request, response):
        data = {
            "user": request.user if request.user.is_authenticated else None,
            "path": request.get_full_path()[:200],
            "status": response.status_code if response.status_code else 0,
            "method": request.method if request.method else "UNKNOWN",
        }
        return data

    if asyncio.iscoroutinefunction(get_response):

        async def middleware(request):
            response = await get_response(request)
            data = create_data(request, response)
            await LoggedPath.objects.acreate(**data)
            return response

    else:

        def middleware(request):
            response = get_response(request)
            data = create_data(request, response)
            LoggedPath.objects.create(**data)
            return response

    return middleware


@sync_and_async_middleware
def authentication_middleware(get_response):
    def authenticate(request):
        if request.user.is_authenticated and hasattr(request.user, 'rlc_user'):
            key = request.session.get('private_key')
            cache.set(request.user.rlc_user.pk, key, 10)

        # header = request.META.get("HTTP_AUTHORIZATION")
        # if header:
        #     token = header.split(" ")[1]
        #     payload = jwt.decode(
        #         token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"]
        #     )
        #     user = UserProfile.objects.get(pk=payload["django_user"])
        #     request.user = user
        #     if hasattr(request.user, "rlc_user") and "key" in payload:
        #         cache.set(user.rlc_user.pk, payload["key"], 10)

        if (
            settings.TESTING
            and request.user
            and request.user.pk
            and request.user.email == "dummy@law-orga.de"
        ):
            private_key = RlcUser.get_dummy_user_private_key(request.user.rlc_user)
            cache.set(request.user.rlc_user.pk, private_key, 10)

        return request

    def clear_cache(request):
        pass
        # don't clear the cache for now as another request at the same time might delete the cache
        # if hasattr(request, "user") and hasattr(request.user, "rlc_user"):
        #     cache.delete(request.user.rlc_user.pk)

    if asyncio.iscoroutinefunction(get_response):

        async def middleware(request):
            try:
                request = await sync_to_async(authenticate)(request)
            except Exception as e:
                response = ErrorResponse(
                    err_type="JwtTokenFailed",
                    title="Authentication Failed",
                    status=401,
                    internal=str(e),
                )
            else:
                response = await get_response(request)
            await sync_to_async(clear_cache)(request)
            return response

    else:

        def middleware(request):
            try:
                request = authenticate(request)
            except Exception as e:
                response = ErrorResponse(
                    err_type="JwtTokenFailed",
                    title="Authentication Failed",
                    status=401,
                    internal=str(e),
                )
            else:
                response = get_response(request)
            clear_cache(request)
            return response

    return middleware
