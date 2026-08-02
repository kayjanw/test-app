from dataclasses import dataclass
from enum import Enum
from typing import Union


class Freq(Enum):
    """Frequency"""

    RARELY = 0.2
    ANNUALLY = 0.5
    MONTHLY = 0.7
    WEEKLY = 1


class Nature(Enum):
    """Hobby type"""

    SPORTS = "rgb(228,26,28)"  # red
    LEISURE = "rgb(77,175,74)"  # green
    ENRICHMENT = "rgb(55,126,184)"  # blue


@dataclass
class Hobby:
    name: str
    proficiency: Union[int, float]
    enjoyment: Union[int, float]
    icon: str
    frequency: Freq
    type: Nature

    @property
    def hovertext(self) -> str:
        return f"<b>{self.name}</b><br>{self.frequency.name.capitalize()}"

    @property
    def icon_link(self) -> str:
        return f"https://api.iconify.design/{self.icon}.svg?height=100"


hobbies = [
    Hobby("Badminton", 5.8, 9, "openmoji:badminton", Freq.WEEKLY, Nature.SPORTS),
    Hobby(
        "Climbing", 5.5, 5.5, "openmoji:woman-climbing", Freq.ANNUALLY, Nature.SPORTS
    ),
    Hobby(
        "Pickleball",
        4,
        7.3,
        "material-symbols:pickleball",
        Freq.ANNUALLY,
        Nature.SPORTS,
    ),
    Hobby("Skiing", 1.5, 6.8, "openmoji:skier", Freq.ANNUALLY, Nature.SPORTS),
    Hobby("Swimming", 7, 6, "openmoji:woman-swimming", Freq.ANNUALLY, Nature.SPORTS),
    Hobby("Squash", 2, 5.5, "mdi:squash", Freq.ANNUALLY, Nature.SPORTS),
    Hobby("Crochet", 3.5, 8, "openmoji:yarn", Freq.ANNUALLY, Nature.LEISURE),
    Hobby("Gaming", 6, 4, "openmoji:video-game", Freq.RARELY, Nature.LEISURE),
    Hobby(
        "Keyboard", 9, 8.7, "openmoji:musical-keyboard", Freq.MONTHLY, Nature.LEISURE
    ),
    Hobby("Arduino", 6, 7, "openmoji:arduino", Freq.RARELY, Nature.ENRICHMENT),
    Hobby("Reading", 7, 9.5, "openmoji:books", Freq.WEEKLY, Nature.ENRICHMENT),
]
