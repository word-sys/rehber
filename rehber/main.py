import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from Rehber import *

uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()
import sqlite3

baglanti = sqlite3.connect("rehber.db")
islem = baglanti.cursor()
baglanti.commit()

table = islem.execute(
    "create table if not exists rehber (isim text, soyisim text, numara int)")
baglanti.commit()


def kayit_ekle():
    isim = ui.lneisim.text()
    soyisim = ui.lnesoyisim.text()
    numara = int(ui.lnenumara.text())

    try:
        ekle = "insert into rehber (isim, soyisim, numara) values (?,?,?)"
        islem.execute(ekle, (isim, soyisim, numara))
        baglanti.commit()
        kayit_listele()
        ui.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı", 10000)
        ui.lneisim.clear()
        ui.lnesoyisim.clear()
        ui.lnenumara.clear()
    except Exception as error:
        ui.statusbar.showMessage("Kayıt Eklenemedi Hata Çıktı === " + str(error))


def kayit_listele():
    ui.tableWidget.clear()
    ui.tableWidget.setHorizontalHeaderLabels(
        ("İsim","Soyisim","Numara"))
    ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    sorgu = "select * from rehber"
    islem.execute(sorgu)

    for indexSatir, kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tableWidget.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))


kayit_listele()

def kayit_sil():
    sil_mesaj = QMessageBox.question(pencere, "Silme Onayı", "Silmek İstediğinizden Emin Misiniz ?",
                                     QMessageBox.Yes | QMessageBox.No)

    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tableWidget.selectedItems()
        silinecek_kayit = secilen_kayit[0].text()

        sorgu = "delete from rehber where numara = ?"
        try:
            islem.execute(sorgu, (silinecek_kayit,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Başarıyla Silindi")
            kayit_listele()
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Silinirken Hata Çıktı === " + str(error))

    else:
        ui.statusbar.showMessage("Silme İşlemi İptal Edildi")


def kayit_guncelle():
    guncelle_mesaj = QMessageBox.question(pencere, "Güncelleme Onayı",
                                          "Bu kaydı Güncellemek istediğinizden Emin Misiniz ?",
                                          QMessageBox.Yes | QMessageBox.No)

    if guncelle_mesaj == QMessageBox.Yes:
        try:
            isim = ui.lneisim.text()
            soyisim = ui.lnesoyisim.text()
            numara = int(ui.lnenumara.text())

            if soyisim == "":
                islem.execute("update rehber set isim = ? where numara = ?", (isim, numara))
            elif isim == "":
                islem.execute("update rehber set soyisim = ? where numara = ?", (soyisim, numara))
            else:
                islem.execute("update rehber set isim = ?, soyisim = ? where numara = ?",(isim, soyisim, numara))
            baglanti.commit()
            kayit_listele()
            ui.statusbar.showMessage("Kayıt Başarıyla Güncellendi")
            ui.lneisim.clear()
            ui.lnesoyisim.clear()
            ui.lnenumara.clear()
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Güncellemede Hata Çıktı === " + str(error))
    else:
        ui.statusbar.showMessage("Güncelleme İptal Edildi")


def cikisYap():
    cikis_mesaj = QMessageBox.question(pencere, "Oturumu Kapatın", "Çıkış Yapmak İstediğinize Emin Misiniz ?",QMessageBox.Yes | QMessageBox.No)

    if cikis_mesaj == QMessageBox.Yes:
        uygulama.closeAllWindows()

    else:
        ui.statusbar.showMessage("Çıkış İptal Edildi")


ui.btnkaydet.clicked.connect(kayit_ekle)
ui.btnsil.clicked.connect(kayit_sil)
ui.btnguncelle.clicked.connect(kayit_guncelle)
ui.btncikis.clicked.connect(cikisYap)
sys.exit(uygulama.exec_())