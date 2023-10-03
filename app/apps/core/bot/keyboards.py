from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from ..models import Place


class MainMenu(ReplyKeyboardBuilder):
    places = "جایی می‌خوای بری؟"
    back = "🔙 بازگشت"

    class Callback(CallbackData, prefix="main_menu"):
        pass

    def __init__(self) -> None:
        super().__init__()
        self.button(text=self.places)
        self.adjust(1)


class Places(InlineKeyboardBuilder):
    class Callback(CallbackData, prefix="place"):
        pass

    class GroupCallback(CallbackData, prefix="place"):
        group: int

    class LocationCallback(CallbackData, prefix="place"):
        latitude: float
        longitude: float

    def __init__(
        self,
        mode: str | None = None,
        places: list[Place] | None = None,
    ) -> None:
        super().__init__()

        i = 0
        if mode == "group":
            i = len(Place.Group.choices)
            for group_id, group_name in Place.Group.choices:
                self.button(
                    text=str(group_name),
                    callback_data=self.GroupCallback(group=group_id),
                )
            self.button(text=MainMenu.back, callback_data=MainMenu.Callback())
        elif mode == "location":
            if places:
                i = len(places)
                for place in places:
                    self.button(
                        text=place.name,
                        callback_data=self.LocationCallback(
                            latitude=place.latitude, longitude=place.longitude
                        ),
                    )
                self.button(text=MainMenu.back, callback_data=self.Callback())

        if i % 2:
            self.adjust(*[2 for _ in range(i // 2)] + [1, 1])
        else:
            self.adjust(2)
