from typing import Union

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from ..models import Place
from ..use_case import CORE_USE_CASE
from . import keyboards, texts

router = Router()


@router.message(Command(commands=["start"]))
async def start_message_handler(message: Message) -> None:
    if message.from_user is None:
        return

    _, is_new = await CORE_USE_CASE.register_bot_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
    )

    bot_name = (await message.bot.get_my_name()).name if message.bot else ""
    if is_new:
        text = texts.START_NEW_USER.format(
            full_name=message.from_user.full_name,
            bot_name=bot_name,
        )
    else:
        text = texts.START_EXISTED_USER.format(
            full_name=message.from_user.full_name,
            bot_name=bot_name,
        )
    await message.answer(
        text=text,
        reply_markup=keyboards.MainMenu().as_markup(resize_keyboard=True),
    )


@router.callback_query(keyboards.MainMenu.Callback.filter())
async def back_main_menu_callback_query_handler(query: CallbackQuery) -> None:
    if query.message is None:
        return

    await query.answer()

    await query.message.delete()
    await query.message.answer(
        text=texts.BACK_MAIN_MENU,
        reply_markup=keyboards.MainMenu().as_markup(resize_keyboard=True),
    )


@router.callback_query(keyboards.Places.Callback.filter())
@router.callback_query(keyboards.Places.GroupCallback.filter())
@router.callback_query(keyboards.Places.LocationCallback.filter())
async def place_callback_query_handler(
    query: CallbackQuery,
    callback_data: Union[
        keyboards.Places.Callback,
        keyboards.Places.GroupCallback,
        keyboards.Places.LocationCallback,
    ],
) -> None:
    if query.message is None:
        return

    await query.answer()

    if isinstance(callback_data, keyboards.Places.Callback):
        await query.message.edit_reply_markup(
            reply_markup=keyboards.Places(mode="group").as_markup(resize_keyboard=True)
        )
    elif isinstance(callback_data, keyboards.Places.GroupCallback):
        places = [
            place async for place in Place.objects.filter(group=callback_data.group).all()
        ]

        await query.message.edit_reply_markup(
            reply_markup=keyboards.Places(mode="location", places=places).as_markup()
        )
    elif isinstance(callback_data, keyboards.Places.LocationCallback):
        await query.message.answer_location(
            latitude=callback_data.latitude,
            longitude=callback_data.longitude,
        )
        await query.message.delete()
        await query.message.send_copy(chat_id=query.from_user.id)


@router.message(F.text == keyboards.MainMenu.places)
async def place_message_handler(message: Message) -> None:
    await message.answer(
        text=texts.PLACES,
        reply_markup=keyboards.Places(mode="group").as_markup(resize_keyboard=True),
    )
