from typing import Literal
from .base import TranslationKeys
from .en import en_translations

TRANSLATIONS: dict[Literal["en"], TranslationKeys] = {
    "en": en_translations,
}
