from typing import Any, Tuple
from dataclasses import dataclass, field

from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware

from tgbot.models.language import Language

@dataclass
class LanguageData:
    flag: str
    title: str
    label: str = field(init=False, default=None)

    def __post_init__(self):
        self.label = f"{self.flag} {self.title}"


class I18nMiddleware(BaseI18nMiddleware):

    AVAILABLE_LANGUAGE = {
        i.value.get("id"): LanguageData(i.value.get("name"), i.value.get("id")) for i in Language
    }

    def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        *_, data = args
        user = data["user"]
        user_language: user.language or self.default

        data["i18n"] = self
        data["_"] = self.gettext

        return user_language
