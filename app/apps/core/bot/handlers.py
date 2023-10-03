from typing import Union

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
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
        reply_markup=keyboards.MainKeyboard().as_markup(resize_keyboard=True),
    )


@router.callback_query(keyboards.MainKeyboard.Callback.filter())
async def back_main_menu_callback_query_handler(query: CallbackQuery) -> None:
    if query.message is None:
        return

    await query.answer()

    await query.message.delete()
    await query.message.answer(
        text=texts.BACK_MAIN_MENU,
        reply_markup=keyboards.MainKeyboard().as_markup(resize_keyboard=True),
    )


@router.message(F.text == keyboards.MainKeyboard.freshman_button)
@router.callback_query(keyboards.FreshmanKeyboard.Callback.filter(F.mode == "menu"))
async def freshman_message_handler(query_message: Union[CallbackQuery, Message]) -> None:
    if isinstance(query_message, Message):
        await query_message.answer(
            text=texts.FRESHMAN_MENU,
            reply_markup=keyboards.FreshmanKeyboard().as_markup(),
        )
    else:
        if not query_message.message:
            return

        await query_message.answer()

        await query_message.message.edit_text(
            text=texts.FRESHMAN_MENU,
            reply_markup=keyboards.FreshmanKeyboard().as_markup(),
        )


@router.callback_query(keyboards.FreshmanKeyboard.Callback.filter(F.mode == "register"))
async def freshman_register_callback_query_handler(query: CallbackQuery) -> None:
    if query.message is None:
        return

    await query.answer()

    try:
        await query.message.edit_text(
            text=texts.FRESHMAN_REGISTER,
            reply_markup=keyboards.FreshmanKeyboard(back=True).as_markup(),
        )
    except TelegramBadRequest:
        pass


@router.callback_query(keyboards.PlaceKeyboard.Callback.filter())
@router.callback_query(keyboards.PlaceKeyboard.GroupCallback.filter())
@router.callback_query(keyboards.PlaceKeyboard.LocationCallback.filter())
async def places_callback_query_handler(
    query: CallbackQuery,
    callback_data: Union[
        keyboards.PlaceKeyboard.Callback,
        keyboards.PlaceKeyboard.GroupCallback,
        keyboards.PlaceKeyboard.LocationCallback,
    ],
) -> None:
    if query.message is None:
        return

    await query.answer()

    if isinstance(callback_data, keyboards.PlaceKeyboard.Callback):
        await query.message.edit_reply_markup(
            reply_markup=keyboards.PlaceKeyboard(mode="group").as_markup(
                resize_keyboard=True
            )
        )
    elif isinstance(callback_data, keyboards.PlaceKeyboard.GroupCallback):
        places = [
            place async for place in Place.objects.filter(group=callback_data.group).all()
        ]

        await query.message.edit_reply_markup(
            reply_markup=keyboards.PlaceKeyboard(
                mode="location", places=places
            ).as_markup()
        )
    elif isinstance(callback_data, keyboards.PlaceKeyboard.LocationCallback):
        await query.message.answer_location(
            latitude=callback_data.latitude,
            longitude=callback_data.longitude,
        )
        await query.message.delete()
        await query.message.send_copy(chat_id=query.from_user.id)


@router.message(F.text == keyboards.MainKeyboard.place_button)
async def places_message_handler(message: Message) -> None:
    await message.answer(
        text=texts.PLACE,
        reply_markup=keyboards.PlaceKeyboard(mode="group").as_markup(
            resize_keyboard=True
        ),
    )
