from dataclasses import dataclass
from enum import Enum
from typing import Union


class Frequency(Enum):
    RARELY = 0.2
    ANNUALLY = 0.5
    MONTHLY = 0.7
    WEEKLY = 1


class HobbyType(Enum):
    SPORTS = "rgb(228,26,28)"  # red
    LEISURE = "rgb(77,175,74)"  # green
    ENRICHMENT = "rgb(55,126,184)"  # blue


@dataclass
class Hobby:
    name: str
    proficiency: Union[int, float]
    enjoyment: Union[int, float]
    frequency: Frequency
    type: HobbyType


hobbies = [
    Hobby("Badminton", 5.8, 9, Frequency.WEEKLY, HobbyType.SPORTS),
    Hobby("Climbing", 5.5, 5.5, Frequency.ANNUALLY, HobbyType.SPORTS),
    Hobby("Pickleball", 4, 7.3, Frequency.ANNUALLY, HobbyType.SPORTS),
    Hobby("Skiing", 1.5, 6.8, Frequency.ANNUALLY, HobbyType.SPORTS),
    Hobby("Swimming", 7, 6, Frequency.ANNUALLY, HobbyType.SPORTS),
    Hobby("Squash", 2, 5.5, Frequency.ANNUALLY, HobbyType.SPORTS),
    Hobby("Crochet", 3.5, 8, Frequency.ANNUALLY, HobbyType.LEISURE),
    Hobby("Gaming", 6, 4, Frequency.RARELY, HobbyType.LEISURE),
    Hobby("Keyboard", 9, 8.7, Frequency.MONTHLY, HobbyType.LEISURE),
    Hobby("Arduino", 6, 7, Frequency.RARELY, HobbyType.ENRICHMENT),
    Hobby("Reading", 7, 9.5, Frequency.WEEKLY, HobbyType.ENRICHMENT),
]
