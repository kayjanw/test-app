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
        return f"https://api.iconify.design/{self.icon}.svg?height=500"


"""
Scale:

Proficiency
1: Absolute beginner
2-3: Tried < 10 times
4-5: Tried > 10 times
6-8: Decent at it
8-10: Good at it

Enjoyment
4: Not priority
5-6: If I'm free
7-8: Happy to do it
9-10: Anytime
"""

hobbies = [
    # Sports
    Hobby("Badminton", 5.8, 9, "openmoji:badminton", Freq.WEEKLY, Nature.SPORTS),
    Hobby("Climbing", 5.5, 6, "openmoji:woman-climbing", Freq.ANNUALLY, Nature.SPORTS),
    Hobby(
        "Golf",
        2,
        5.5,
        "streamline-ultimate-color:golf-ball",
        Freq.MONTHLY,
        Nature.SPORTS,
    ),
    Hobby("Gym", 6, 8.2, "icon-park:dumbbell", Freq.WEEKLY, Nature.SPORTS),
    Hobby(
        "Pickleball",
        4,
        7.3,
        "material-symbols:pickleball",
        Freq.ANNUALLY,
        Nature.SPORTS,
    ),
    Hobby("Skiing", 1, 6.8, "openmoji:skis", Freq.ANNUALLY, Nature.SPORTS),
    Hobby(
        "Swimming", 7, 6.5, "fluent-emoji-flat:goggles", Freq.ANNUALLY, Nature.SPORTS
    ),
    Hobby("Squash", 2.5, 6, "mdi:squash", Freq.ANNUALLY, Nature.SPORTS),
    # Leisure
    Hobby("Crochet", 3.5, 8, "openmoji:yarn", Freq.ANNUALLY, Nature.LEISURE),
    Hobby("Gaming", 6.5, 5.5, "openmoji:video-game", Freq.RARELY, Nature.LEISURE),
    Hobby(
        "Keyboard", 9, 8.7, "openmoji:musical-keyboard", Freq.MONTHLY, Nature.LEISURE
    ),
    Hobby("Netflix", 7, 4.5, "selfhst:netflix", Freq.MONTHLY, Nature.LEISURE),
    # Enrichment
    Hobby("Arduino", 3, 6.7, "devicon:arduino", Freq.RARELY, Nature.ENRICHMENT),
    Hobby(
        "Reading", 7, 9.5, "streamline-emojis:open-book", Freq.WEEKLY, Nature.ENRICHMENT
    ),
    Hobby("Theatre", 7, 8.5, "mdi:theatre", Freq.MONTHLY, Nature.ENRICHMENT),
]
