from typing import Any, Final, Optional

from .models import Text, TGUser

# The `UseCase` classes are used to separate the business logic from the rest of the code.
# Also, because of this, we can easily use the same business logic in different places.
# For example, in the bot and in the web application.

# The main reason to use classes instead of functions is that
# the `UseCase` classes may depend on different services.


class CoreUseCase:
    @staticmethod
    async def register_bot_user(
        user_id: int,
        username: Optional[str],
        full_name: str,
    ) -> tuple[TGUser, bool]:
        return await TGUser.objects.aupdate_or_create(
            id=user_id,
            defaults={
                "username": username,
                "full_name": full_name,
            },
        )


class TextUseCase:
    @staticmethod
    def get_text(_name: str, is_button: bool = False, **kwargs: Any) -> str:
        if Text.objects.filter(name=_name, is_button=is_button).exists():
            text = Text.objects.get(name=_name, is_button=is_button).text
            if text:
                for old, new in kwargs.items():
                    text = text.replace("{" + str(old) + "}", str(new))
                return text
        return ""

    @staticmethod
    async def aget_text(_name: str, is_button: bool = False, **kwargs: Any) -> str:
        if await Text.objects.filter(name=_name, is_button=is_button).aexists():
            text = (await Text.objects.aget(name=_name, is_button=is_button)).text
            if text:
                for old, new in kwargs.items():
                    text = text.replace("{" + str(old) + "}", str(new))
                return text
        return ""


# Alternative: use a DI middleware to inject the use case into the handler.
# To provide DI middleware, you need to use a third-party library.
# For example, https://github.com/MaximZayats/aiogram-di
CORE_USE_CASE: Final[CoreUseCase] = CoreUseCase()
TEXT_USE_CASE: Final[TextUseCase] = TextUseCase()
