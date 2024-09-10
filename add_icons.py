import sys

import fontforge
import psMat


ICONS = {
    0xE100: "timer-outline",
    0xE101: "arrow-left-bottom",
    0xE102: "alert-rhombus",
    0xE103: "clock-outline",
    0xE104: "snake",
    0xE105: "source-branch",
    0xE106: "arrow-up-down",
    0xE107: "arrow-up",
    0xE108: "arrow-down",
    0xE109: "file-plus-outline",
    0xE10A: "file-minus-outline",
    0xE10B: "alert-octagon-outline",
}

def edit(filename):
    font = fontforge.open(filename)

    for codepoint, name in ICONS.items():
        glyph = font.createChar(codepoint, name)
        glyph.importOutlines(f"MaterialDesign/svg/{name}.svg")
        glyph.transform(psMat.scale(1200 / glyph.width))

    font.generate(filename)
    font.close()


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        edit(filename)
