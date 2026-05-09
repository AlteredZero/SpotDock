import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from app import SpotDockUi

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("assets/SpotDockIcon.png"))

window = SpotDockUi()
window.show()

sys.exit(app.exec_())