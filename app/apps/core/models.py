import re
from typing import Iterable

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Text(models.Model):
    class Meta:
        db_table = "text"

    name = models.CharField(
        max_length=64,
        verbose_name="Variable Name",
    )

    is_button = models.BooleanField(
        verbose_name="Is Button",
    )
    text = models.TextField(
        verbose_name="Text",
    )

    objects: models.manager.BaseManager["Text"]

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        self.name = self.name.upper()
        self.text = self.text.strip()

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def __str__(self) -> str:
        return f"{self.name}"


class TGUser(models.Model):
    class Meta:
        db_table = "tg_user"

    id = models.BigIntegerField(
        primary_key=True,
        verbose_name="Telegram ID",
    )
    full_name = models.CharField(
        max_length=64,
        verbose_name="Full Name",
    )
    username = models.CharField(
        max_length=64,
        null=True,
        verbose_name="Telegram Username",
    )

    objects: models.manager.BaseManager["TGUser"]

    def __str__(self) -> str:
        return f"{self.full_name}"


class Course(models.Model):
    class Meta:
        db_table = "course"

    class UnitType(models.IntegerChoices):
        THEORETICAL = 1, _("theoretical")
        PRACTICAL = 2, _("practical")

    class CourseType(models.IntegerChoices):
        GENERAL = 1, _("general")
        FOUNDATIONAL = 2, _("foundational")
        SPECIALIZED = 3, _("mandatory")
        OPTIONAL = 4, _("optional")

    fa_title = models.CharField(
        max_length=64,
        verbose_name="Course Persian Title",
    )
    en_title = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name="Course English Title",
    )
    offering_semester = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(8),
        ],
        verbose_name="Offering Semester",
    )
    credit = models.IntegerField(
        verbose_name="Course Credit",
    )
    quiz_credit = models.IntegerField(
        default=0,
        verbose_name="Course Quiz Credit",
    )
    prerequisite_course = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Prerequisite Course",
    )
    unit_type = models.IntegerField(
        choices=UnitType.choices,
        verbose_name="Unit Type",
    )
    course_type = models.IntegerField(
        choices=CourseType.choices,
        verbose_name="Course Type",
    )
    has_exam = models.BooleanField(
        default=True,
        verbose_name="Course Has Exam?",
    )
    has_project = models.BooleanField(
        default=False,
        verbose_name="Course Has Project?",
    )

    objects: models.manager.BaseManager["Course"]

    def __str__(self) -> str:
        return f"{self.fa_title}"


class Place(models.Model):
    class Meta:
        db_table = "place"

    class Group(models.IntegerChoices):
        GATE = 1, _("🚪 درب‌های ورودی")
        RESTAURANT = 2, _("🍕 غذاخوری‌ها")
        DORMITORY = 3, _("🛏 خوابگاه‌ها")
        FACULTY = 4, _("📚 دانشکده‌ها")
        BANK = 5, _("🏦 بانک‌ها")
        OFFICE_BUILDING = 6, _("🏢 ساختمان‌های اداری")
        OTHER = 7, _("🛟 مکان‌های رفاهی و تفریحی")

    name = models.CharField(
        max_length=64,
        verbose_name="Name",
    )
    group = models.IntegerField(
        choices=Group.choices,
        verbose_name="Group",
    )
    latitude = models.FloatField(
        verbose_name="Latitude",
    )
    longitude = models.FloatField(
        verbose_name="Longitude",
    )

    objects: models.manager.BaseManager["Place"]

    def __str__(self) -> str:
        return f"{self.name}"


class Phone(models.Model):
    class Meta:
        db_table = "phone"

    name = models.CharField(
        max_length=64,
        verbose_name="Name",
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(r"^((0|00|\+)?98|0)?(\d{10})$"),
        ],
        verbose_name="Phone Number",
    )

    objects: models.manager.BaseManager["Phone"]

    def __str__(self) -> str:
        return f"{self.name}"

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        phone_number_match = re.match(r"^((0|00|\+)?98|0)?(\d{10})$", self.phone_number)
        if phone_number_match:
            self.phone_number = "+98" + phone_number_match.group(3)

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


class Link(models.Model):
    class Meta:
        db_table = "link"

    name = models.CharField(
        max_length=64,
        verbose_name="Name",
    )
    address = models.URLField(
        verbose_name="URL Address",
    )

    objects: models.manager.BaseManager["Link"]

    def __str__(self) -> str:
        return f"{self.name}"
