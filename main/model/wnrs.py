from dataclasses import dataclass
from typing import Optional


@dataclass
class Deck:
    button_text: str
    button_id: str
    button_style: Optional[dict[str, str]] = None


# SWATCHES = [
#     "#25262b", "#868e96", "#fa5252", "#e64980", "#be4bdb", "#7950f2", "#4c6ef5",
#     "#228be6", "#15aabf", "#12b886", "#40c057", "#82c91e", "#fab005", "#fd7e14"
# ]

SWATCHES_TEXT = [
    "#FFFFFF",
    "#FAFAEE",
    "#F6CA69",
    "#BE001C",
    "#1695C8",
    "#4D1015",
    "#000000",
]
SWATCHES_BACKGROUND = [
    "#FAFAEE",
    "#F6CA69",
    "#EAD2E0",
    "#EEC4C5",
    "#EB744C",
    "#BE001C",
    "#AF2637",
    "#275835",
    "#4598BA",
    "#5F86b5",
    "#282C69",
    "#4D1015",
    "#000000",
]
