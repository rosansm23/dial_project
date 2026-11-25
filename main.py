
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import Rotary

page0 = None
rotary = None
start_scherm = True
lblTitel = None
lblSubtitel = None

kleuren = [
    0xFF0000,  # Rood
    0xff7700,  # Oranje
    0xFFFF00,  # Geel
    0x00FF00,  # Groen
    0x0000FF,  # Blauw
    0x800080,  # Paars
    0xfc03ba   # Roze
]

kleur_index = 0
vorige_waarde = 0


def setup():
    global page0, rotary, vorige_waarde, lblTitel, lblSubtitel

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()

    page0 = m5ui.M5Page(bg_c=0xFFFFFF)

    lblTitel = m5ui.M5Label(
        "Het Regenboog Rad",
        x=35,
        y=105,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0
    )
    
    lblSubtitel = m5ui.M5Label(
    "Klik en draai!",
    x=65,
    y=135,
    text_c=0x555555,
    bg_c=0xFFFFFF,
    bg_opa=0,
    font=lv.font_montserrat_14,
    parent=page0
)

    page0.screen_load()

    rotary = Rotary()
    rotary.reset_rotary_value()
    vorige_waarde = rotary.get_rotary_value()


def loop():
    global kleur_index, vorige_waarde, start_scherm

    M5.update()

    if start_scherm:
        if BtnA.wasClicked():
            start_scherm = False
            lblTitel.delete()
            lblSubtitel.delete()

            page0.set_bg_color(
                lv.color_hex(kleuren[0]),
                255,
                lv.PART.MAIN | lv.STATE.DEFAULT
            )

            kleur_index = 0
            rotary.reset_rotary_value()
            vorige_waarde = rotary.get_rotary_value()

        return

    huidige_waarde = rotary.get_rotary_value()

    verschil = huidige_waarde - vorige_waarde

    if verschil != 0:

        if verschil > 0:
            kleur_index = (kleur_index + 1) % len(kleuren)
        else:
            kleur_index = (kleur_index - 1) % len(kleuren)

        page0.set_bg_color(
            lv.color_hex(kleuren[kleur_index]),
            255,
            lv.PART.MAIN | lv.STATE.DEFAULT
        )

        vorige_waarde = huidige_waarde



if __name__ == '__main__':
    try:
        setup()
        while True:
            loop()

    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg
            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
