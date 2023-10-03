from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from ..models import Place


class MainKeyboard(ReplyKeyboardBuilder):
    freshman_button = "Freshman"
    place_button = "Place"
    back_button = "Back"

    class Callback(CallbackData, prefix="main_menu"):
        pass

    def __init__(self) -> None:
        super().__init__()
        self.button(text=self.freshman_button)
        self.button(text=self.place_button)
        self.adjust(1)


class FreshmanKeyboard(InlineKeyboardBuilder):
    register_button = "Freshman Register"

    class Callback(CallbackData, prefix="freshman"):
        mode: str

    def __init__(self, back: bool = False) -> None:
        super().__init__()
        if back:
            self.button(
                text=MainKeyboard.back_button,
                callback_data=self.Callback(mode="menu"),
            )
        else:
            self.button(
                text=self.register_button,
                callback_data=self.Callback(mode="register"),
            )
        self.adjust(1)


class PlaceKeyboard(InlineKeyboardBuilder):
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
            groups = Place.Group.choices
            i = len(groups)
            for group_id, group_name in groups:
                self.button(
                    text=str(group_name),
                    callback_data=self.GroupCallback(group=group_id),
                )
            self.button(
                text=MainKeyboard.back_button, callback_data=MainKeyboard.Callback()
            )
        elif mode == "location" and places:
            i = len(places)
            for place in places:
                self.button(
                    text=place.name,
                    callback_data=self.LocationCallback(
                        latitude=place.latitude, longitude=place.longitude
                    ),
                )
            self.button(text=MainKeyboard.back_button, callback_data=self.Callback())

        if i % 2:
            self.adjust(*[2 for _ in range(i // 2)] + [1, 1])
        else:
            self.adjust(2)
