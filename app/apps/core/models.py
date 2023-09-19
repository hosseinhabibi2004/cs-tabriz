from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


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
