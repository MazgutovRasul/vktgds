import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel


files = ["vk.py", "tg.py", "ds.py"]  # файлы, которые нужно запустить
for file in files:
    subprocess.Popen(args=["start", "python", file], shell=True, stdout=subprocess.PIPE)


class Card(QWidget):
    def __init__(self):
        super(Card, self).__init__()
        self.setWindowTitle('Боты')
        self.setGeometry(100, 100, 400, 250)
        self.maintext = QLabel(self)
        self.maintext.setText('Здравствуйте')
        self.maintext.move(140, 50)
        self.subtext = QLabel(self)
        self.subtext.setText('Я сделал 3 ботов в разных мессенджерах')
        self.subtext.move(35, 70)
        self.ansubtext = QLabel(self)
        self.ansubtext.setText('Тут вы можете протестировать ботов')
        self.ansubtext.move(50, 90)
        self.vklink = QLineEdit(self)
        self.vklink.setText('https://vk.com/club225546234')
        self.vklink.setGeometry(70, 110, 230, 30)
        self.tglink = QLineEdit(self)
        self.tglink.setText('https://t.me/rasulfilmsbot')
        self.tglink.setGeometry(90, 150, 190, 30)
        self.dslink = QLineEdit(self)
        self.dslink.setText('https://discord.gg/nSSVwDBd')
        self.dslink.setGeometry(75, 190, 220, 30)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Card()
    ex.show()
    sys.exit(app.exec())
