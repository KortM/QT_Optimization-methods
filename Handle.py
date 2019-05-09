import math
import numpy
import pylab
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D


class Handler():
    def __init__(self, a, b, y, p1, p2):
        self.a = a
        self.b = b
        self.y = y
        self.p1 = p1
        self.p2 = p2
        self.V = 0

        self.xgrid= []
        self.ygrid = []
        self.zgrid = []
    #Метод расчета количества получаемого целевого компонента
    def Calc_formula(self, T1, T2):

        self.V = (self.a * (T1 - self.b * self.p1))*math.cos(self.y*self.p2*math.sqrt(math.pow(T1, 2)+math.pow(T2,2)))
        return round(self.V, 4)

    def full(self, T1_min, T1_max, T2_min, T2_max, step):

        tmp1 = math.fabs(T1_min) + math.fabs(T1_max)
        tmp2 = math.fabs(T2_min) + math.fabs(T2_max)

        arr_T1 = self.fill_m(T1_min, T1_max, step)
        arr_T2 = self.fill_m(T2_min, T2_max, step)


        self.arr_d = []
        for x in range(len(arr_T1)):
            self.arr_d.append([])
            for y in range(len(arr_T2)):
                self.arr_d[x].append(0)
        nMin = self.Calc_formula(arr_T1[0], arr_T2[0])
        nCount = 0
        xPos = 0
        yPos = 0

        kk1 = 0
        kk2 = 0
        for x in arr_T1:
            for y in arr_T2:
                #print(x, y)
                if y > x:
                    self.maxC= self.Calc_formula(x,y)
                    nCount +=1
                    self.arr_d[xPos][yPos] = self.maxC * 8 * 100

                    if self.maxC < nMin:
                        nMin = self.maxC
                        kk1 = x
                        kk2 = y
                yPos +=1
            xPos +=1
            yPos = 0
        nMin *=8
        self.create_matrix(T1_min, T1_max, T2_min, T2_max, step)
        self.plot()
        #self.plothit()
        return "T1: "+str(kk1)+" T2: "+str(kk2)+" V: "+str(nMin*100)



    def fill_m(self, T_min, T_max, step):
        mass = []
        while T_min <= T_max:
            mass.append(T_min)
            T_min = round(T_min+step, 2)
        if mass[-1] < T_max:
            mass.append(T_max)
        return mass

    def create_matrix(self, T1_min, T1_max, T2_min, T2_max, step):

        arr_1 = self.fill_m(T1_min, T1_max, step)
        arr_2 = self.fill_m(T2_min, T2_max, step)

        self.xgrid, self.ygrid = numpy.meshgrid(arr_1, arr_2)

        self.zgrid = numpy.zeros((len(self.xgrid), len(self.xgrid)))
        x1 = len(self.xgrid)
        x2 = len(self.xgrid[0])

        for x in range(x1):
            for xx in range(x2):
                zz = [self.xgrid[x][xx], self.ygrid[x][xx]]
                if zz[0] - zz[1] <= 3:
                    self.zgrid[x][xx] = self.Calc_formula(zz[0], zz[1])

    def plot(self):
        fig = pylab.figure()
        axes = Axes3D(fig)
        #print(self.xgrid, self.ygrid, self.zgrid)
        axes.plot_surface(self.xgrid,self.ygrid, self.zgrid)  # На вход - вектора + z-матрица
        print("test")
        axes.set_xlabel("Температура T1")  # Подписываем оси
        axes.set_ylabel("Температура T2")  # Подписываем оси
        axes.set_title("Количество получаеого компонента", loc='center')  # Подписываем заголовок
        pylab.show()
    def plothit(self):
        pyplot.figure()
        cs = pylab.contourf(self.xgrid, self.ygrid,self.zgrid,150, cmap=pylab.cm.rainbow)
        pylab.title("Количество получаеого компонента", loc='center')
        pylab.xlabel("Температура T1")
        pylab.ylabel("Температура T2")

        pyplot.show()

if __name__ =='__main__':
    h =Handler(1,1,1, 1,1)
    print(h.full(-3, 0.5, -3, 0.5, 0.01))


