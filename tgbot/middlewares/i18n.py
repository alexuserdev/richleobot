from typing import Any, Tuple
from dataclasses import dataclass, field

from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware
from aiogram import types

from tgbot.models.language import Language
from tgbot.misc.db_api.database import UsersDb

@dataclass
class LanguageData:
    flag: str
    title: str
    label: str = field(init=False, default=None)

    def __post_init__(self):
        self.label = f"{self.flag} {self.title}"


class I18nMiddleware(BaseI18nMiddleware):

    AVAILABLE_LANGUAGE = {
        i.value.get("id"): LanguageData(i.value.get("flag"), i.value.get("label")) for i in Language
    }

    def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        *_, data = args
        user = types.User.get_current()
        user_id = user.id
       
        # code of language 
        user_language = UsersDb.get_language(user_id)
        data["i18n"] = self
        data["_"] = self.gettext

        return user_language
