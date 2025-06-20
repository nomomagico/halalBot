#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: quran_patched.py
# Created: Wednesday, 18th June 2025
# Author: Patched by nomomagico
# -----
# Source: Based on original quran.com wrapper by Rakibul Yeasin
# Modified to use quranenc.com API
###

import requests
from typing import Dict

class Quran:
    """
    quranenc.com API class (patched)

    Contains:
        get_chapter
    """

    def __init__(self) -> None:
        """
        Constructor for Quran API wrapper (patched version)

        returns
            None
        """
        self.base = "https://quranenc.com/api/v1/translation/sura/arabic_moyassar/"

    def get_chapter(self, chapter_number: int) -> str:
        """
        Get a full chapter's Arabic Moyassar translation from QuranEnc.

        args:
            chapter_number  Chapter ID (1 to 114)

        returns:
            String containing all ayahs joined by newlines
        """
        if not (1 <= chapter_number <= 114):
            raise ValueError("Número de capítulo fuera del rango (1-114)")

        url = f"{self.base}{chapter_number}"
        response = requests.get(url)

        if response.status_code != 200:
            raise ConnectionError(f"No se pudo obtener el capítulo: HTTP {response.status_code}")

        data = response.json()
        ayahs = data.get("result")

        if not ayahs:
            raise ValueError("Respuesta inválida o vacía de la API")

        return "\n".join(ayah["translation"] for ayah in ayahs)
