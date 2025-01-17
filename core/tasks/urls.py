from django.urls import include, path

from core.tasks.api.query import router as query_router

urlpatterns = [
    path("query/", include(query_router.urls)),
]
