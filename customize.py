import sys

import fontforge
import psMat

from fontedit import OpenType, TrueType


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
}


def generate_icon_fonts(filename: str, ext: str) -> None:
    for codepoint, name in ICONS.items():
        font = fontforge.open(filename)

        glyph = font.createChar(codepoint, name)
        glyph.importOutlines(f"MaterialDesign/svg/{name}.svg")
        [xmin, ymin, xmax, ymax] = glyph.boundingBox()
        glyph.transform(psMat.translate(-xmin, -ymin / 3))

        font.generate(f"icon-{name}.{ext}")
        font.close()


def replace_zero_otf(font: OpenType) -> None:
    dotted_zero_idx = font.cff.charset.value.index("zero") + 1
    dotted_zero_tosf_idx = font.cff.charset.value.index("zero.tosf") + 1
    slashed_zero_idx = font.cff.charset.value.index("zero.zero") + 1
    slashed_zero_tosf_idx = font.cff.charset.value.index("zero.tosf.zero") + 1
    
    dotted_zero = font.cff.charstrings[dotted_zero_idx]
    dotted_zero_tosf = font.cff.charstrings[dotted_zero_tosf_idx]
    slashed_zero = font.cff.charstrings[slashed_zero_idx]
    slashed_zero_tosf = font.cff.charstrings[slashed_zero_tosf_idx]

    font.cff.charstrings[dotted_zero_idx] = slashed_zero
    font.cff.charstrings[dotted_zero_tosf_idx] = slashed_zero_tosf
    font.cff.charstrings[slashed_zero_idx] = dotted_zero
    font.cff.charstrings[slashed_zero_tosf_idx] = dotted_zero_tosf


def replace_zero_ttf(font: TrueType) -> None:
    dotted_zero_idx = next(key for key, value in font.post.glyph_id_to_string_map.items() if value == "zero")
    dotted_zero_tosf_idx = next(key for key, value in font.post.glyph_id_to_string_map.items() if value == "zero.tosf")
    slashed_zero_idx = next(key for key, value in font.post.glyph_id_to_string_map.items() if value == "zero.zero")
    slashed_zero_tosf_idx = next(key for key, value in font.post.glyph_id_to_string_map.items() if value == "zero.tosf.zero")

    dotted_zero = font.glyf.glyphs[dotted_zero_idx]
    dotted_zero_tosf = font.glyf.glyphs[dotted_zero_tosf_idx]
    slashed_zero = font.glyf.glyphs[slashed_zero_idx]
    slashed_zero_tosf = font.glyf.glyphs[slashed_zero_tosf_idx]

    font.glyf.glyphs[dotted_zero_idx] = slashed_zero
    font.glyf.glyphs[dotted_zero_tosf_idx] = slashed_zero_tosf
    font.glyf.glyphs[slashed_zero_idx] = dotted_zero
    font.glyf.glyphs[slashed_zero_tosf_idx] = dotted_zero_tosf


def update_name(font: OpenType | TrueType) -> None:
    for name_rec in font.name.names.values():
        if name_rec.name_id != 7:  # keep trademark notice intact
            name_rec.name = name_rec.name.replace("Fira", "Fyra")
    if isinstance(font, OpenType):
        font.cff.names.names = [name.replace("Fira", "Fyra") for name in font.cff.names.names]
        font.cff.top_dict.full_name = font.cff.top_dict.full_name.replace("Fira", "Fyra")


if __name__ == "__main__":
    match sys.argv:
        case [_, filename]:
            write = False
        case [_, "-w", filename]:
            write = True
        case _:
            print(f"Usage: {sys.argv[0]} [-w] <FILENAME>", file=sys.stderr)
            sys.exit(1)

    if filename.endswith(".otf"):
        ext = "otf"
        font_cls = OpenType
        replace_zero = replace_zero_otf
    elif filename.endswith(".ttf"):
        ext = "ttf"
        font_cls = TrueType
        replace_zero = replace_zero_ttf

    else:
        raise Exception("unknown format")

    with open(filename, "rb") as file:
        font = font_cls.from_bytes(file.read())

    generate_icon_fonts(filename, ext)

    for codepoint, name in ICONS.items():
        with open(f"icon-{name}.{ext}", "rb") as file:
            icon_font = font_cls.from_bytes(file.read())

        glyph_id = icon_font.cmap.char_code_to_glyph_id_map[codepoint]
        if ext == "otf":
            charstring = icon_font.cff.charstrings[glyph_id]
            font.add_glyph(codepoint, name, charstring)
        else:
            glyph = icon_font.glyf.glyphs[glyph_id]
            font.add_glyph(codepoint, name, glyph)

    replace_zero(font)
    update_name(font)

    if write:
        sys.stdout.buffer.write(font.to_bytes())
