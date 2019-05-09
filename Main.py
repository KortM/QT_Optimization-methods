
import sys
import pyqtgraph.opengl as gl

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d, Axes3D

from PyQt5.QtCore import Qt, QMimeData, QSize
from PyQt5.QtGui import QPixmap, QIcon, QFont, QDrag
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QSizePolicy, \
    QTableWidgetItem
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit
from PyQt5.QtWidgets import QGridLayout, QComboBox
from PyQt5.QtWidgets import QTabWidget, QTableWidget


from Handle import Handler
from matplotlib import pylab

class LoginWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        # self.main = root
        self.UI()

    def UI(self):
        self.setWindowTitle("Авторизация")
        self.setGeometry(20, 20, 200, 50)
        self.setFixedSize(200, 250)
        self.layout = QVBoxLayout(self)
        self.lab_icon = QLabel()
        pixmap = QPixmap('login.png')
        self.lab_icon.setPixmap(pixmap)
        self.lab_icon.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lab_icon)
        self.label = QLabel("Login")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.lab_2 = QLabel("Password")
        self.lab_2.setAlignment(Qt.AlignCenter)
        self.user_name_field = QLineEdit()

        self.layout.addWidget(self.user_name_field)
        self.user_pwd_field = QLineEdit()
        self.user_pwd_field.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.lab_2)
        self.layout.addWidget(self.user_pwd_field)

        self.login_button = QPushButton("Войти")
        self.layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.login)
        self.setWindowModality(Qt.WindowModal)

        self.isAuth = False

        self.show()

    def login(self):
        user = self.user_name_field.text()
        pwd = self.user_pwd_field.text()

        print(user)
        print(pwd)

        f = open('users', 'r').readlines()
        isUser = False
        p = ""
        for line in f:
            str = line.split(';')
            if str[0] == user:
                isUser = True
                p = str[1]
            else:
                isUser = False

        if p == pwd:
            self.hide()
            self.parent().show()

        if user == "admin" and pwd =="admin":
            self.hide()
            self.parent().hide()
            ap = AdminPanel(self.parent())

    def closeEvent(self, e):
        sys.exit()

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.graph =PlotCanvas3d(self, width=1, height=1)
        self.graph_2 = PlotCanvas(self, width=1, height=1)
        f = open('style.css', 'r')

        self.setStyleSheet(f.read())
        f.close()
        login = LoginWindow(self)
        self.createGui()

    def createGui(self):
        self.setGeometry(10, 30, 600, 300)
        self.setWindowTitle("Test")
        self.tabs = QTabWidget()
        self.tab = QWidget()
        self.tab_result = QWidget()
        self.tabs.addTab(self.tab, "Главное")
        self.tabs.addTab(self.tab_result, "Таблица значений")
        # self.tab = QTabWidget()
        # self.tab.addTab(self, "Главное окно")
        self.tools_panel = QVBoxLayout()
        self.lab_method = QLabel("Метод оптимизации")
        self.lab_method.setAlignment(Qt.AlignCenter)
        self.select_method = QComboBox()
        self.select_method.addItem("Полный перебор")
        self.select_method.addItem("Сканнирование с переменным шагом")
        self.lab_var = QLabel("Вариант")
        self.lab_var.setAlignment(Qt.AlignCenter)
        self.select_var = QComboBox()
        self.select_var.addItem("11")
        self.lab_select_temterature = QLabel("Ограничения температуры")
        self.temp_layout = QHBoxLayout()
        self.temp_layout_2 = QHBoxLayout()
        self.lab_T1min = QLabel("Tmin")
        self.lab_T1max = QLabel("Tmax")
        self.lab_T2min = QLabel("T2min")
        self.lab_T2max = QLabel("T2max")
        self.T2min = QLineEdit()
        self.T2min.setText("-0.5")
        self.T2max = QLineEdit()
        self.T2max.setText("3")
        self.value_T1 = QLineEdit()
        self.value_T1.setText("-3")
        self.value_T2 = QLineEdit()
        self.value_T2.setText("0.5")
        self.temp_layout.addWidget(self.lab_T1min)
        self.temp_layout.addWidget(self.value_T1)
        self.temp_layout.addWidget(self.lab_T1max)
        self.temp_layout.addWidget(self.value_T2)
        self.temp_layout_2.addWidget(self.lab_T2min)
        self.temp_layout_2.addWidget(self.T2min)
        self.temp_layout_2.addWidget(self.lab_T2max)
        self.temp_layout_2.addWidget(self.T2max)

        self.lim_layout = QHBoxLayout()
        self.lim_layout_2 = QHBoxLayout()
        self.lab_lim = QLabel("Ограничения 2-го рода:")
        self.lim_value = QLineEdit()
        self.lab_count = QLabel("Кол-во устройств:")
        self.count = QLineEdit()
        self.lim_value.setText("T2-T1 <= 3")
        self.lim_value.setEnabled(False)
        self.count.setText("2")
        self.count.setEnabled(False)
        self.lim_layout.addWidget(self.lim_value)
        self.lim_layout.addWidget(self.count)
        self.lim_layout_2.addWidget(self.lab_lim)
        self.lim_layout_2.addWidget(self.lab_count)


        self.lab_accuracy = QLabel("Точность нахождения решения:")
        self.accuracy = QLineEdit()
        self.accuracy.setText("0.01")


        self.lab_mult = QLabel("Нормирующие множители:")
        self.mult_layout_1 = QHBoxLayout()
        self.lab_alfa = QLabel("\u03B1")
        self.alfa = QLineEdit()
        self.alfa.setText("1")
        self.lab_beta = QLabel("\u03B2")
        self.beta = QLineEdit()
        self.beta.setText("1")
        self.lab_y = QLabel("y")
        self.y = QLineEdit()
        self.y.setText("3.14")
        self.mult_layout_1.addWidget(self.lab_alfa)
        self.mult_layout_1.addWidget(self.alfa)
        self.mult_layout_1.addWidget(self.lab_beta)
        self.mult_layout_1.addWidget(self.beta)
        self.mult_layout_1.addWidget(self.lab_y)
        self.mult_layout_1.addWidget(self.y)


        self.lab_volume = QLabel("Величина перепада давлений Кпа:")
        self.lab_P1 = QLabel("\u0394 P1")
        self.lab_P2 = QLabel("\u0394 P2")
        self.P1 = QLineEdit()
        self.P1.setText("1")
        self.P2 = QLineEdit()
        self.P2.setText("1")
        self.volume_layout = QHBoxLayout()
        self.volume_layout.addWidget(self.lab_P1)
        self.volume_layout.addWidget(self.P1)
        self.volume_layout.addWidget(self.lab_P2)
        self.volume_layout.addWidget(self.P2)

        self.tools_panel.contentsMargins().top()
        self.tools_panel.addWidget(self.lab_method)
        self.tools_panel.addWidget(self.select_method)
        self.tools_panel.addWidget(self.lab_var)
        self.tools_panel.addWidget(self.select_var)
        self.tools_panel.addWidget(self.lab_select_temterature)
        self.tools_panel.addLayout(self.temp_layout)
        self.tools_panel.addLayout(self.temp_layout_2)
        self.tools_panel.addLayout(self.lim_layout_2)
        self.tools_panel.addLayout(self.lim_layout)
        self.tools_panel.addWidget(self.lab_accuracy)
        self.tools_panel.addWidget(self.accuracy)
        self.tools_panel.addWidget(self.lab_mult)
        self.tools_panel.addLayout(self.mult_layout_1)

        self.tools_panel.addWidget(self.lab_volume)
        self.tools_panel.addLayout(self.volume_layout)
        self.tools_panel.addStretch(1)

        self.result_layout = QHBoxLayout()
        self.result_line = QLineEdit()
        self.result_line.setEnabled(False)
        self.result_line.setMinimumSize(200, 30)
        self.result_lab = QLabel("Результат: ")
        self.result_lab.setFont(QFont('', 10))
        self.result_layout.addWidget(self.result_lab)
        self.result_layout.addWidget(self.result_line)

        self.layout = QGridLayout()
        self.layout.addLayout(self.tools_panel, 0, 1)

        self.buttons_panel = QHBoxLayout()
        self.start_button = QPushButton('Решить задачу')
        self.start_button.clicked.connect(self.plotGraph)
        self.buttons_panel.addWidget(self.start_button)

        self.name_graph = QLabel("3-D График критерия качества оптимизации")
        self.name_graph.setAlignment(Qt.AlignCenter)
        self.graph_layout = QVBoxLayout()

        self.graph_layout.addWidget(self.name_graph)
        self.graph_layout.addWidget(self.graph)

        self.third_graph_lay = QVBoxLayout()
        self.lab_tihrd_graph = QLabel("Контурный график критерия качества оптимизации")
        self.lab_tihrd_graph.setAlignment(Qt.AlignCenter)
        self.third_graph = gl.GLViewWidget()
        self.third_graph.setGeometry(0, 110, 1920, 500)
        self.third_graph_lay.addWidget(self.lab_tihrd_graph)
        self.third_graph_lay.addWidget(self.graph_2)

        self.graph_layout.addLayout(self.third_graph_lay)
        self.layout.addLayout(self.graph_layout, 2, 1)
        self.layout.addLayout(self.result_layout, 1, 1)
        self.layout.addLayout(self.buttons_panel, 3, 1)

        # self.layout.addLayout(self.buttons_panel, 1,1)
        # self.tab.addTab(self, "Tab")
        self.table = QTableWidget()
        self.table.setColumnCount(2000)
        self.table.setRowCount(2000)
        self.table_layout = QVBoxLayout()
        self.table_layout.addWidget(self.table)
        self.tab_result.setLayout(self.table_layout)

        self.tab.setLayout(self.layout)
        self.lay_tab_1 = QVBoxLayout()
        self.lay_tab_1.addWidget(self.tabs)
        self.setLayout(self.lay_tab_1)
        # self.setLayout(self.layout)
        self.setAcceptDrops(True)
        #self.show()

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        self.button.move(position)
        e.setDropAction(Qt.MoveAction)
        e.accept()
    def plotGraph(self):
        print("plot")
        T_min = float(self.value_T1.text())
        T_max = float(self.value_T2.text())
        print("qwe")
        accuracy =float(self.accuracy.text())
        a = float(self.alfa.text())
        b = float(self.beta.text())
        y = float(self.y.text())
        print("asd")
        P1 = float(self.P1.text())
        P2 = float(self.P2.text())
        print(a, b, y, P1, P2)
        h = Handler(a, b, y, P1, P2)
        self.result_line.setText(h.full(T_min, T_max, T_min, T_max, accuracy))
        self.graph.plot(h.xgrid, h.ygrid, h.zgrid)
        self.graph_2.plot(h.xgrid, h.ygrid, h.zgrid)
        self.update_table(h.xgrid, h.ygrid, h.arr_d)
    def update_table(self, arr1, arr2, arr3):
        for x in range(len(arr1)):
            for y in range(len(arr2)):
                self.table.setItem(x, y, QTableWidgetItem(str(arr3[x][y])))
class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
       # self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def plot(self, x, y, z):
        ax = self.figure.add_subplot(111, )
        ax.contourf(x,y,z,cmap=pylab.cm.rainbow)
        ax.set_xlabel("Температура T1")
        ax.set_ylabel("Температура T2")
        self.draw()

class PlotCanvas3d(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = Axes3D(fig)

        self.axes.set_title("Количество получаеого компонента", loc='center')
        FigureCanvas.__init__(self, figure=fig)
       # self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def plot(self, x, y, z):
        self.axes.clear()
        self.axes.plot_surface(x, y, z)
        self.axes.set_xlabel("Температура T1")
        self.axes.set_ylabel("Температура T2")
        self.draw()

class AdminPanel(QDialog):
    def __init__(self,parent ):
        super().__init__(parent)
        self.GUI()
    def GUI(self):
        self.setWindowTitle("Admin")
        self.setGeometry(0,0, 100, 100)
        self.setFixedSize(300, 250)
        self.tools_layput = QVBoxLayout()

        self.lab_add_user  = QLabel("Добавление или удаление пользователя")
        self.lab_add_user.setFont(QFont("arial", 10))
        self.tools_layput.addWidget(self.lab_add_user)

        self.lab_login = QLabel("Login")
        self.tools_layput.addWidget(self.lab_login)
        self.user_login = QLineEdit()
        self.tools_layput.addWidget(self.user_login)
        self.lab_pwd = QLabel("Password")
        self.tools_layput.addWidget(self.lab_pwd)
        self.user_pwd = QLineEdit()
        self.user_pwd.setEchoMode(QLineEdit.Password)
        self.tools_layput.addWidget(self.user_pwd)
        self.user_add_button = QPushButton("Добавить")
        self.user_add_button.clicked.connect(self.add_user)
        self.tools_layput.addWidget(self.user_add_button)
        self.user_rem_button = QPushButton("Удалить")
        self.user_rem_button.clicked.connect(self.remove_user)
        self.tools_layput.addWidget(self.user_rem_button)


        self.setLayout(self.tools_layput)
        self.show()
    def add_user(self):
        f = open('users', 'a')
        name = self.user_login.text()
        password = self.user_pwd.text()
        f.write("\n{0};{1}".format(name, password))
        f.close()
        print("Закрыт файл")
    def remove_user(self):
        try:
            f = open('users','r')
            line = f.readlines()
            name = self.user_login.text()
            for i in f:
                str = i.split(";")
                if str[0] == name:
                    line.pop(i)

        except:
            print("errror")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec())
