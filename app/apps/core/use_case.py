from typing import Final

from .models import TGUser

# The `UseCase` classes are used to separate the business logic from the rest of the code.
# Also, because of this, we can easily use the same business logic in different places.
# For example, in the bot and in the web application.

# The main reason to use classes instead of functions is that
# the `UseCase` classes may depend on different services.


class CoreUseCase:
    @staticmethod
    async def register_bot_user(
        user_id: int,
        username: str | None,
        full_name: str,
    ) -> tuple[TGUser, bool]:
        return await TGUser.objects.aupdate_or_create(
            id=user_id,
            defaults={
                "username": username,
                "full_name": full_name,
            },
        )


# Alternative: use a DI middleware to inject the use case into the handler.
# To provide DI middleware, you need to use a third-party library.
# For example, https://github.com/MaximZayats/aiogram-di
CORE_USE_CASE: Final[CoreUseCase] = CoreUseCase()
