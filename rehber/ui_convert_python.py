from PyQt5 import uic

with open("Rehber.py","w", encoding="utf-8") as fout:
    uic.compileUi("rehber.ui", fout)