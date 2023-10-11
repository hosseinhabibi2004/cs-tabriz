from typing import Union

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async

from ..models import Course, Link, Phone, Place, PrerequisiteCourse
from ..use_case import CORE_USE_CASE, TEXT_USE_CASE
from . import keyboards

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
        text = await TEXT_USE_CASE.aget_text(
            "START_NEW_USER",
            full_name=message.from_user.full_name,
            bot_name=bot_name,
        )
    else:
        text = await TEXT_USE_CASE.aget_text(
            "START_EXISTED_USER",
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
        text=await TEXT_USE_CASE.aget_text("BACK_MAIN_MENU"),
        reply_markup=keyboards.MainKeyboard().as_markup(resize_keyboard=True),
    )


@router.message(F.text == keyboards.MainKeyboard.freshman_button)
@router.callback_query(keyboards.FreshmanKeyboard.Callback.filter(F.mode == "menu"))
async def freshman_message_handler(query_message: Union[CallbackQuery, Message]) -> None:
    if isinstance(query_message, Message):
        await query_message.answer(
            text=await TEXT_USE_CASE.aget_text("FRESHMAN_MENU"),
            reply_markup=keyboards.FreshmanKeyboard().as_markup(),
        )
    else:
        if not query_message.message:
            return

        await query_message.answer()

        await query_message.message.edit_text(
            text=await TEXT_USE_CASE.aget_text("FRESHMAN_MENU"),
            reply_markup=keyboards.FreshmanKeyboard().as_markup(),
        )


@router.callback_query(keyboards.FreshmanKeyboard.Callback.filter(F.mode == "register"))
async def freshman_register_callback_query_handler(query: CallbackQuery) -> None:
    if query.message is None:
        return

    await query.answer()

    try:
        await query.message.edit_text(
            text=await TEXT_USE_CASE.aget_text("FRESHMAN_REGISTER"),
            reply_markup=keyboards.FreshmanKeyboard(back=True).as_markup(),
        )
    except TelegramBadRequest:
        pass


@router.message(F.text == keyboards.MainKeyboard.course_button)
async def courses_message_handler(message: Message) -> None:
    await message.answer(
        text=await TEXT_USE_CASE.aget_text("COURSE_MENU"),
        reply_markup=keyboards.CourseKeyboard().as_markup(),
    )


@router.callback_query(keyboards.CourseKeyboard.CoursesFilterCallback.filter())
async def courses_filter_callback_query_handler(
    query: CallbackQuery,
    callback_data: keyboards.CourseKeyboard.CoursesFilterCallback,
) -> None:
    if query.message is None:
        return

    await query.answer()

    if callback_data.filter_by == "semester":
        if callback_data.value is not None:
            courses = [
                course
                async for course in Course.objects.filter(
                    offering_semester=callback_data.value
                ).all()
            ]
            text = await TEXT_USE_CASE.aget_text(
                "SEMESTER_COURSES_MENU",
                offering_semester=callback_data.value,
            )
        else:
            courses = None
            text = await TEXT_USE_CASE.aget_text("COURSES_BY_SEMESTER_MENU")
    elif callback_data.filter_by == "type":
        if callback_data.value is not None:
            courses = [
                course
                async for course in Course.objects.filter(
                    course_type=callback_data.value
                ).all()
            ]
            text = await TEXT_USE_CASE.aget_text(
                "TYPE_COURSES_MENU",
                course_type=Course.CourseType(callback_data.value).label,
            )
        else:
            courses = None
            text = await TEXT_USE_CASE.aget_text("COURSES_BY_TYPE_MENU")
    else:
        courses = None
        text = await TEXT_USE_CASE.aget_text("COURSE_MENU")

    await query.message.edit_text(
        text=text,
        reply_markup=keyboards.CourseKeyboard(
            filter_by=callback_data.filter_by, courses=courses
        ).as_markup(),
    )


@router.callback_query(keyboards.CourseKeyboard.CourseCallback.filter())
async def course_details_callback_query_handler(
    query: CallbackQuery,
    callback_data: keyboards.CourseKeyboard.CourseCallback,
) -> None:
    @sync_to_async
    def get_prerequisite_courses_text(_course: Course) -> str:
        prerequisite_courses = PrerequisiteCourse.objects.filter(course=_course).all()
        if prerequisite_courses:
            return "، ".join(
                [_.prerequisite_course.fa_title for _ in prerequisite_courses]
            )
        return "-"

    if query.message is None:
        return

    await query.answer()

    course = await Course.objects.aget(id=callback_data.id)

    text = await TEXT_USE_CASE.aget_text(
        "COURSE_DETAILS",
        fa_title=course.fa_title,
        en_title=course.en_title,
        offering_semester=(
            course.offering_semester if course.offering_semester is not None else "-"
        ),
        credit=course.credit,
        quiz_credit=course.quiz_credit,
        prerequisite_courses=await get_prerequisite_courses_text(_course=course),
        unit_type=Course.UnitType(course.unit_type).label,
        course_type=Course.CourseType(course.course_type).label,
        has_exam="✅" if course.has_exam else "❌",
        has_project="✅" if course.has_project else "❌",
    )
    await query.message.edit_text(
        text=text,
        reply_markup=keyboards.CourseKeyboard(
            filter_by=callback_data.filter_by, course=course
        ).as_markup(),
    )


@router.message(F.text == keyboards.MainKeyboard.place_button)
async def places_message_handler(message: Message) -> None:
    await message.answer(
        text=await TEXT_USE_CASE.aget_text("GROUPS"),
        reply_markup=keyboards.PlaceKeyboard(
            mode="group",
        ).as_markup(resize_keyboard=True),
    )


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
        await query.message.edit_text(
            text=await TEXT_USE_CASE.aget_text("GROUPS"),
            reply_markup=keyboards.PlaceKeyboard(
                mode="group",
            ).as_markup(resize_keyboard=True),
        )
    elif isinstance(callback_data, keyboards.PlaceKeyboard.GroupCallback):
        places = [
            place async for place in Place.objects.filter(group=callback_data.group).all()
        ]
        text = await TEXT_USE_CASE.aget_text(
            "GROUP_PLACES",
            group=Place.Group(callback_data.group).label,
        )
        await query.message.edit_text(
            text=text,
            reply_markup=keyboards.PlaceKeyboard(
                mode="location", places=places
            ).as_markup(),
        )
    elif isinstance(callback_data, keyboards.PlaceKeyboard.LocationCallback):
        place = await Place.objects.aget(
            latitude=callback_data.latitude,
            longitude=callback_data.longitude,
        )
        if place:
            await query.message.delete()
            await query.message.answer_location(
                latitude=place.latitude,
                longitude=place.longitude,
            )
            text = await TEXT_USE_CASE.aget_text(
                "PLACE",
                name=place.name,
                group=Place.Group(place.group).label,
            )
            await query.message.answer(text=text)
            await query.message.send_copy(chat_id=query.from_user.id)


@router.message(F.text == keyboards.MainKeyboard.phone_button)
async def phones_message_handler(message: Message) -> None:
    text = await TEXT_USE_CASE.aget_text(
        "PHONES",
        phones="\n\n".join(
            [
                await TEXT_USE_CASE.aget_text(
                    "PHONE_TEMPLATE",
                    name=phone.name,
                    phone_number=phone.phone_number,
                )
                async for phone in Phone.objects.filter().all()
            ]
        ),
    )
    await message.answer(text=text)


@router.message(F.text == keyboards.MainKeyboard.link_button)
async def links_message_handler(message: Message) -> None:
    text = await TEXT_USE_CASE.aget_text(
        "LINKS",
        links="\n\n".join(
            [
                await TEXT_USE_CASE.aget_text(
                    "LINK_TEMPLATE",
                    name=link.name,
                    address=link.address,
                )
                async for link in Link.objects.filter().all()
            ]
        ),
    )
    await message.answer(text=text)


@router.message(F.text == keyboards.MainKeyboard.about_button)
async def about_message_handler(message: Message) -> None:
    await message.answer(
        text=await TEXT_USE_CASE.aget_text("ABOUT"),
    )
