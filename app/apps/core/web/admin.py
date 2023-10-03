from typing import Optional

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http import HttpRequest

from ..models import Course, Place, TGUser


@admin.register(TGUser)
class TGUserAdmin(ModelAdmin[TGUser]):
    list_display = (
        "id",
        "full_name",
        "username",
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        super().has_add_permission(request)
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[TGUser] = None
    ) -> bool:
        super().has_change_permission(request, obj)
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[TGUser] = None
    ) -> bool:
        super().has_delete_permission(request, obj)
        return False


@admin.register(Course)
class CourseAdmin(ModelAdmin[Course]):
    list_display = (
        "fa_title",
        "course_type",
        "unit_type",
    )


@admin.register(Place)
class PlaceAdmin(ModelAdmin[Place]):
    list_display = (
        "name",
        "group",
        "latitude",
        "longitude",
    )
