from typing import Any, Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from ..models import Course, Place


def right_to_left_markup(old_list: list[Any]) -> list[Any]:
    new_list = []
    for i in range(0, len(old_list) // 2):
        new_list.append(old_list[i * 2 + 1])
        new_list.append(old_list[i * 2])

    if len(old_list) % 2 != 0:
        new_list.append(old_list[-1])

    return new_list


class MainKeyboard(ReplyKeyboardBuilder):
    freshman_button = "Freshman"
    place_button = "Place"
    course_button = "Course"
    back_button = "Back"

    class Callback(CallbackData, prefix="main_menu"):
        pass

    def __init__(self) -> None:
        super().__init__()
        self.button(text=self.freshman_button)
        self.button(text=self.course_button)
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


class CourseKeyboard(InlineKeyboardBuilder):
    courses_by_semester_button = "Courses by semester"
    courses_by_type_button = "Courses by type"

    class CoursesFilterCallback(CallbackData, prefix="courses"):
        filter_by: Optional[str] = None
        value: Optional[int] = None

    class CourseCallback(CallbackData, prefix="course"):
        filter_by: str
        id: int

    def __init__(
        self,
        filter_by: Optional[str] = None,
        course: Optional[Course] = None,
        courses: Optional[list[Course]] = None,
    ) -> None:
        super().__init__()

        if filter_by is None:
            self.button(
                text=self.courses_by_semester_button,
                callback_data=self.CoursesFilterCallback(filter_by="semester"),
            )
            self.button(
                text=self.courses_by_type_button,
                callback_data=self.CoursesFilterCallback(filter_by="type"),
            )
            self.adjust(1)
            return

        if filter_by == "semester":
            markup_length = self._filter_by_semester(
                course=course,
                courses=courses,
            )
        elif filter_by == "type":
            markup_length = self._filter_by_type(
                course=course,
                courses=courses,
            )
        else:
            markup_length = 0

        if markup_length % 2:
            self.adjust(*[2 for _ in range(markup_length // 2)] + [1, 1])
        else:
            self.adjust(2)

    def _filter_by_semester(
        self,
        course: Optional[Course],
        courses: Optional[list[Course]],
    ) -> int:
        if course is not None:
            markup_length = 0
            self.button(
                text=MainKeyboard.back_button,
                callback_data=self.CoursesFilterCallback(
                    filter_by="semester", value=course.offering_semester
                ),
            )
        elif courses is not None:
            markup_length = len(courses)
            for _course in courses:
                self.button(
                    text=_course.fa_title,
                    callback_data=self.CourseCallback(
                        filter_by="semester", id=_course.id
                    ),
                )
            self.button(
                text=MainKeyboard.back_button,
                callback_data=self.CoursesFilterCallback(filter_by="semester"),
            )
        else:
            semesters = list(range(1, 8 + 1))
            markup_length = len(semesters)
            for offering_semester in right_to_left_markup(semesters):
                self.button(
                    text=f"Semester {offering_semester}",
                    callback_data=self.CoursesFilterCallback(
                        filter_by="semester", value=offering_semester
                    ),
                )
            self.button(
                text=MainKeyboard.back_button,
                callback_data=self.CoursesFilterCallback(),
            )
        return markup_length

    def _filter_by_type(
        self,
        course: Optional[Course],
        courses: Optional[list[Course]],
    ) -> int:
        if course is not None:
            markup_length = 0
            self.button(
                text=MainKeyboard.back_button,
                callback_data=self.CoursesFilterCallback(
                    filter_by="type", value=course.course_type
                ),
            )
        elif courses is not None:
            markup_length = len(courses)
            for _course in courses:
                self.button(
                    text=_course.fa_title,
                    callback_data=self.CourseCallback(filter_by="type", id=_course.id),
                )
            self.button(
                text=MainKeyboard.back_button,
                callback_data=self.CoursesFilterCallback(filter_by="type"),
            )
        else:
            course_types = Course.CourseType.choices
            markup_length = len(course_types)
            for course_type_id, course_type_name in course_types:
                self.button(
                    text=str(course_type_name),
                    callback_data=self.CoursesFilterCallback(
                        filter_by="type", value=course_type_id
                    ),
                )
            self.button(
                text=MainKeyboard.back_button,
                callback_data=self.CoursesFilterCallback(),
            )
        return markup_length


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
        mode: Optional[str] = None,
        places: Optional[list[Place]] = None,
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
