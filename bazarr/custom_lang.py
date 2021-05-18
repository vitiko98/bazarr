# -*- coding: utf-8 -*-

import logging
import os

logger = logging.getLogger(__name__)


class CustomLanguage:
    """Base class for custom languages."""

    alpha2 = "pb"
    alpha3 = "pob"
    language = "pt-BR"
    official_alpha2 = "pt"
    official_alpha3 = "por"
    name = "Brazilian Portuguese"
    iso = "BR"
    _possible_matches = ("pt-br", "pob", "pb", "brazilian", "brasil", "brazil")
    _extensions = (".pt-br", ".pob", "pb")
    _extensions_forced = (".pt-br.forced", ".pob.forced", "pb.forced")

    def get_subzero_language_params(self) -> tuple:
        return self.official_alpha2, self.iso

    @classmethod
    def from_value(cls, value, attr="alpha3"):
        """Return a custom language subclass by value and attribute
        if found, otherwise return None.

        :param value:
        :param attr:
        """
        logger.debug("Looking for custom language: %s: %s", attr, value)
        for sub in cls.__subclasses__():
            if getattr(sub, attr) == str(value):
                logger.debug("%s found", sub.name)
                return cls()

        return None

    def get_subzero_ietf(self, language_code):  # Consistency
        assert language_code
        return None

    def register(self, database):
        params = (self.alpha3, self.alpha2, self.name)
        database.execute(
            "INSERT OR IGNORE INTO table_settings_languages "
            "(code3, code2, name) VALUES (?,?,?)",
            params,
        )

    def get_alpha_type(self, subtitle: str, subtitle_path=None):
        assert subtitle_path is not None

        extension = str(os.path.splitext(subtitle)[0]).lower()
        to_return = None

        if extension.endswith(self._extensions):
            to_return = self.alpha2

        if extension.endswith(self._extensions_forced):
            to_return = f"{self.alpha2}:forced"

        if to_return is not None:
            logging.debug("BAZARR external subtitles detected: %s", to_return)

        return to_return

    def get_alpha3_from_ffprobe(self, detected_language: dict) -> str:
        alpha3 = str(detected_language["language"].alpha3)
        if alpha3 != self.alpha3:
            return alpha3

        name = detected_language.get("name", "").lower()
        if not name:
            return alpha3

        if any(ext in name for ext in self._possible_matches):
            return self.alpha3

        return alpha3


class BrazilianPortuguese(CustomLanguage):
    pass


class ChineseTraditional(CustomLanguage):
    alpha2 = "zt"
    alpha3 = "zht"
    language = "zh-TW"
    official_alpha2 = "zh"
    official_alpha3 = "zho"
    name = "Chinese Traditional"
    iso = "TW"
    _babelfish = ("cht", "tc", "zht", "hant", "big5", "繁", "雙語")
    _babelfish_disamb = ("chs", "sc", "zhs", "hans", "gb", "简", "双语")
    _extensions = (
        ".cht",
        ".tc",
        ".zh-tw",
        ".zht",
        ".zh-hant",
        ".zhhant",
        ".zh_hant",
        ".hant",
        ".big5",
        ".traditional",
    )
    _extensions_forced = (
        ".cht.forced",
        ".tc.forced",
        ".zht.forced",
        "hant.forced",
        ".big5.forced",
        "繁體中文.forced",
        "雙語.forced",
        "zh-tw.forced",
    )
    _extensions_fuzzy = ("繁", "雙語")
    _extensions_disamb_fuzzy = ("简", "双语")
    _extensions_disamb = (
        ".chs",
        ".sc",
        ".zhs",
        ".zh-hans",
        ".hans",
        ".zh_hans",
        ".zhhans",
        ".gb",
        ".simplified",
    )
    _extensions_disamb_forced = (
        ".chs.forced",
        ".sc.forced",
        ".zhs.forced",
        "hans.forced",
        ".gb.forced",
        "简体中文.forced",
        "双语.forced",
    )

    def get_alpha_type(self, subtitle, subtitle_path=None):
        subtitle_path = str(subtitle_path).lower()
        extension = str(os.path.splitext(subtitle)[0]).lower()

        to_return = None

        # Simplified chinese
        if (
            extension.endswith(self._extensions_disamb)
            or subtitle_path in self._extensions_disamb_fuzzy
        ):
            to_return = "zh"

        elif any(ext in extension[-12:] for ext in self._extensions_disamb_forced):
            to_return = "zh:forced"

        # Traditional chinese
        elif (
            extension.endswith(self._extensions)
            or subtitle_path[:-5] in self._extensions_fuzzy
        ):
            to_return = "zt"

        elif any(ext in extension[-12:] for ext in self._extensions_forced):
            to_return = "zt:forced"

        if to_return is not None:
            logging.debug("BAZARR external subtitles detected: %s", to_return)

        return to_return

    def get_subzero_ietf(self, language_code):
        simpl = any(ext in str(language_code) for ext in self._babelfish_disamb)
        trad = any(ext in str(language_code) for ext in self._babelfish)

        if simpl or trad:
            return "zh"

        return None


class LatinAmericanSpanish(CustomLanguage):
    alpha2 = "ea"  # Only one available I can think of
    alpha3 = "spl"
    language = "es-LA"
    official_alpha2 = "es"
    official_alpha3 = "spa"
    name = "Latin American Spanish"
    iso = "MX"  # Not fair, but ok
    _possible_matches = (
        "es-la",
        "spa-la",
        "spl",
        "mx",
        "latin",
        "mexic",
        "argent",
        "latam",
    )
    _extensions = (".es-la", ".spl", "spa-la", "ea")
    _extensions_forced = (".es-la.forced", ".spl.forced", "spa-la.forced")
