from django.db import models


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
