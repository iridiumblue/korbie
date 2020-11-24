# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import code
import sys
import math
import signal
import traceback
sys.excepthook = traceback.print_exception
from math import sqrt

PRESENTATION_MODE=True
PRESENTATION_WIDTH=1


from PyQt5 import QtCore, QtGui, QtWidgets,Qt
#from QtCore import QTimer
import pyqtgraph.opengl as gl
import pyqtgraph as pg

#import numpy as np
import numpy as np
CUDA=False
#import cupy as np

#input("WARNING - CUDA is off.")


import ctypes
from ctypes import c_double,c_float

t_evs,c_t_evs,c_arr_out = None,None, None

DEFAULT_STEPS=220
NUM_STEPS=DEFAULT_STEPS

NUM_ORBITS=1
NUM_SCALARS=3

REVS=20

lib = ctypes.cdll.LoadLibrary('./libkorbie.so')



def alert(line):
   msgBox = QtWidgets.QMessageBox()
   msgBox.setIcon(QtWidgets.QMessageBox.Information)
   msgBox.setText(line)
   msgBox.setWindowTitle("Message")
   msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok )
   msgBox.exec()

# intercept up/down arrows in order to replot immediately
# https://stackoverflow.com/questions/47874952/qspinbox-signal-for-arrow-buttons
class SpinBox(QtWidgets.QDoubleSpinBox):
    stepChanged = QtCore.pyqtSignal()

    def stepBy(self, step):
        value = self.value()
        super(SpinBox, self).stepBy(step)
        if self.value() != value:
            self.stepChanged.emit()

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.spin = SpinBox()
        self.spin.editingFinished.connect(self.handleSpinChanged)
        self.spin.stepChanged.connect(self.handleSpinChanged)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.spin)

    def handleSpinChanged(self):
        alert(self.spin.value())

def setIncrements(w,start,selection,num=3):
    w.addItem(start)  
    for xx in range(num):   
       start = start.replace("1","01")          
       w.addItem(start.replace("1","5"))
       w.addItem(start.replace("1","2"))
       w.addItem(start)        
    w.setCurrentText(selection)

class Ui_MainWindow(object):
    def resizeEvent(self, event):
        system.exit(0)
        #alert("Resize")
        QtGui.QMainWindow.resizeEvent(self, event)
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 913)
        

        self.high_accuracy_alert=True
        self.animationFrame=0
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        if True : #So editors can collapse this block of display code.
            #self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
            #self.groupBox_2.setGeometry(QtCore.QRect(270, 30, 145, 181))
            #p = self.groupBox_2.palette()
            #p.setColor(self.groupBox_2.backgroundRole(), Qt.QColor(188, 188, 188))
            #self.groupBox_2.setAutoFillBackground(True)
            #self.groupBox_2.setPalette(p)
            #self.groupBox_2.setObjectName("groupBox_2")
            
            self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
            self.comboBox_3.setGeometry(QtCore.QRect(280, 61, 75, 20))
            self.comboBox_3.setObjectName("comboBox_3")
            setIncrements(self.comboBox_3,".001","0.0001")
            #ee=".001"
            #for xx in range(3):    
            #   ee = ee.replace("1","01")
            #   self.comboBox_3.addItem(ee)           
            #   self.comboBox_3.addItem(ee.replace("1","5"))
            #   self.comboBox_3.addItem(ee.replace("1","2"))
               
               
               

            #self.comboBox_3.addItem(".001")
            #self.comboBox_3.addItem(".0001"); 
            #self.comboBox_3.addItem(".00001")
            #self.comboBox_3.setCurrentText("0.0001")
            self.comboBox_3.currentTextChanged.connect(lambda x: self.intervalCB(x, self.doubleSpinBox))
                
            self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
            self.comboBox_4.setGeometry(QtCore.QRect(280, 91, 65, 20))
            self.comboBox_4.setObjectName("comboBox_4")

            setIncrements(self.comboBox_4,".01",".001")
            self.comboBox_4.currentTextChanged.connect(lambda x: self.intervalCB(x, self.doubleSpinBox_p))


            self.comboBox_5 = QtWidgets.QComboBox(self.centralwidget)
            self.comboBox_5.setGeometry(QtCore.QRect(280, 131, 65, 20))
            self.comboBox_5.setObjectName("comboBox_5")
            setIncrements(self.comboBox_5,".01",".001",4)

            self.comboBox_5.currentTextChanged.connect(lambda x: self.intervalCB(x, self.doubleSpinBox_e))

            self.comboBox_6 = QtWidgets.QComboBox(self.centralwidget)
            self.comboBox_6.setGeometry(QtCore.QRect(280, 161, 65, 20))
            self.comboBox_6.setObjectName("comboBox_6")
            setIncrements(self.comboBox_6,".1",".1")
            self.comboBox_6.currentTextChanged.connect(lambda x: self.intervalCB(x, self.doubleSpinBox_angle))



        self.openGLWidget = gl.GLViewWidget(self.centralwidget)
        self.openGLWidget.setGeometry(QtCore.QRect(70, 220, 800, 600))
        self.openGLWidget.setObjectName("openGLWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 681, 20))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans Mono")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.accuracy = QtWidgets.QCheckBox(self.centralwidget)

        #self.accuracy.setNotchesVisible(True)
        self.accuracy.setGeometry(QtCore.QRect(580, 180, 100, 20))
        #self.accuracy.setOrientation(QtCore.Qt.Vertical)
        self.accuracy.setObjectName("High Accuracy")
        self.accuracy.stateChanged.connect(self.sliderCB)


        
        #self.revs.setTickPosition(QtWidgets.QDial.TicksAbove)
        #self.revs.setNotchesVisible(True)

        self.doubleSpinBox = SpinBox(self.centralwidget,value=0.5)
        self.doubleSpinBox.setSingleStep(0.001)
        self.doubleSpinBox.setDecimals(6)
        self.doubleSpinBox.setGeometry(QtCore.QRect(180, 60, 82, 22))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox.stepChanged.connect(self.handleArrowChanged)
        self.doubleSpinBox.valueChanged.connect(self.handleArrowChanged)
        self.doubleSpinBox_p = SpinBox(self.centralwidget,value=6.350)
        self.doubleSpinBox_p.stepChanged.connect(self.handleArrowChanged)
        self.doubleSpinBox_p.valueChanged.connect(self.handleArrowChanged)
        self.doubleSpinBox_p.setSingleStep(0.01)
        self.doubleSpinBox_p.setDecimals(4)
        self.doubleSpinBox_p.setGeometry(QtCore.QRect(180, 90, 62, 22))
        self.doubleSpinBox_p.setObjectName("doubleSpinBox_p")
        self.doubleSpinBox_e = SpinBox(self.centralwidget,value=0.10)
        self.doubleSpinBox_e.stepChanged.connect(self.handleArrowChanged)
        self.doubleSpinBox_e.valueChanged.connect(self.handleArrowChanged)
        self.doubleSpinBox_e.setSingleStep(0.001) 
        self.doubleSpinBox_e.setDecimals(4)
        self.doubleSpinBox_e.setGeometry(QtCore.QRect(180, 130, 62, 22))
        self.doubleSpinBox_e.setObjectName("doubleSpinBox_e")
        self.doubleSpinBox_angle = SpinBox(self.centralwidget,value=15)
        self.doubleSpinBox_angle.stepChanged.connect(self.handleArrowChanged)
        self.doubleSpinBox_angle.valueChanged.connect(self.handleArrowChanged)
        self.doubleSpinBox_angle.setSingleStep(0.10)
        self.doubleSpinBox_angle.setDecimals(3)
        self.doubleSpinBox_angle.setGeometry(QtCore.QRect(180, 160, 62, 22))
        self.doubleSpinBox_angle.setObjectName("doubleSpinBox_angle")



        self.rev_label = QtWidgets.QLabel(self.centralwidget)
        self.rev_label.setGeometry(QtCore.QRect(480, 48, 120, 18))

        self.revs = QtWidgets.QSlider(self.centralwidget)
        self.revs.setValue(REVS)
        self.revs.setOrientation(QtCore.Qt.Horizontal)
        self.revs.valueChanged.connect(self.rev_display_update)
        #self.revs.sliderReleased.connect(self.rev_update)
        self.revs.setMinimum(0)
        self.revs.setMaximum(500)
        
        self.revs.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.revs.setGeometry(QtCore.QRect(480, 65, 180, 20))

        self.rev_value = QtWidgets.QLabel(self.centralwidget)
        self.rev_value.setGeometry(QtCore.QRect(670, 63, 20, 20))
        self.rev_value.setText(str(REVS))

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 63, 21, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 93, 21, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(160, 132, 16, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(160, 162, 16, 16))
        self.label_5.setObjectName("label_5")

        self.label_2_delta = QtWidgets.QLabel(self.centralwidget)
        self.label_2_delta.setGeometry(QtCore.QRect(362, 63, 21, 16))
        self.label_2_delta.setObjectName("label_2_delta")

        self.label_3_delta = QtWidgets.QLabel(self.centralwidget)
        self.label_3_delta.setGeometry(QtCore.QRect(352, 93, 21, 16))
        self.label_3_delta.setObjectName("label_3_delta")

        self.label_4_delta = QtWidgets.QLabel(self.centralwidget)
        self.label_4_delta.setGeometry(QtCore.QRect(352, 132, 21, 16))
        self.label_4_delta.setObjectName("label_4_delta")

        self.label_5_delta = QtWidgets.QLabel(self.centralwidget)
        self.label_5_delta.setGeometry(QtCore.QRect(352, 162, 21, 16))
        self.label_5_delta.setObjectName("label_5_delta")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.event_timer = QtCore.QTimer()
        self.event_timer.timeout.connect(lambda : Qt.QCoreApplication.processEvents())
        self.event_timer.start(20)


        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.animateStep)
        self.flight=None
        self.X_flight=None; self.Y_flight=None; self.Z_flight=None;
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.setSteps(NUM_STEPS)

    def intervalCB(self,val,widget):
        
        widget.setSingleStep(float(val))
        #widget.setValue(0.0)




    def rev_display_update(self):
        rev_num = self.revs.value()
        self.rev_value.setText(str(rev_num))
        self.rev_update()
    def rev_update(self):
        global REVS
        rev_num = self.revs.value()
        REVS=rev_num
        self.setSteps(NUM_STEPS)
        self.pushCB()
        
    def handleArrowChanged(self):
        self.pushCB()

       
    def setSteps(self,ns):
        global NUM_STEPS
        global t_evs,c_t_evs,c_arr_out
        self.timer.stop()
        NUM_STEPS=ns
        t_evs = np.linspace(0,REVS*math.pi,NUM_STEPS*REVS)
        c_t_evs = (c_double * (NUM_STEPS*REVS))(*t_evs)
        dim_product = REVS*NUM_STEPS*NUM_SCALARS
        c_arr_out = (c_double * dim_product)()


    def sliderCB(self):
        if self.accuracy.isChecked() :
           self.setSteps(5000)
           if self.high_accuracy_alert :
              self.high_accuracy_alert=False
              alert("About to recompute at 5x the precision.   Watch a piece of the graph carefully for any slight change.  A change signifies the orbital shape is an artifact of round-off error.  No change indicates the orbit is reliable and you can go back to normal accuracy by unchecking this box.")
        else:
            self.setSteps(1000)
        self.pushCB(reset_steps=False)
        return True
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Korbie : Kerr orbit explorer"))
        
        self.label_2.setText(_translate("MainWindow", "a "))
        self.label_2_delta.setText(_translate("MainWindow", "Δ a"))
        self.label_3.setText(_translate("MainWindow", "p"))
        self.label_3_delta.setText(_translate("MainWindow", "Δ p"))
        self.label_4.setText(_translate("MainWindow", "e"))
        self.label_4_delta.setText(_translate("MainWindow", "Δ e"))
        self.label_5.setText(_translate("MainWindow", "θ"))
        self.label_5_delta.setText(_translate("MainWindow", "Δ θ"))
        self.rev_label.setText(_translate("MainWindow", "# Revolutions"))
        self.accuracy.setText(_translate("MainWindow", "High accuracy"))

    def pushCB(self,reset_steps=True):
        global NUM_STEPS
        self.timer.stop()
        if self.flight : 
            g_w.removeItem(self.flight); self.flight=None
            g_w.removeItem(self.X_flight); self.X_flight=None
            g_w.removeItem(self.Z_flight); self.Z_flight=None
        if reset_steps : self.setSteps(DEFAULT_STEPS)

        self.animationFrame=0
        a=self.doubleSpinBox.value()
        p=self.doubleSpinBox_p.value()
        e=self.doubleSpinBox_e.value()
        theta=self.doubleSpinBox_angle.value()
        #alert("OK! "+str(a)+" "+str(p)+" "+str(e)+" "+str(theta))
        self.pts = do_plot(a,p,e,theta,NUM_STEPS)
        
        self.timer.start(1000)
        #code.interact(local=dict(globals(), **locals()))
        #pts = do_orbits()  # parameterize and parallelize here
    def animateStep(self):
        #sys.exit()
        #self.doubleSpinBox_8.value=self.animationFrame
        #self.doubleSpinBox_8.setProperty('value',self.animationFrame)
        self.timer.stop()
        
        self.animationFrame+=5
        TAIL_LENGTH=256
        head = self.animationFrame
        tail = max([0,head-TAIL_LENGTH])
        if (tail>len(self.pts)):
            self.animationFrame=0
            self.timer.start(500)
            return
        self.timer.start(90)
        old_flight=self.flight
        old_X,old_Y,old_Z = self.X_flight,self.Y_flight,self.Z_flight
        if old_flight : 
            try: g_w.removeItem(old_flight); self.flight=None 
            except: pass
            try: g_w.removeItem(old_X); self.X_flight=None 
            except:pass
            try: g_w.removeItem(old_Z); self.Z_flight=None 
            except: pass
        #... so the flight path shows next to the fixed orbital path, offset the flight
        #    by just a smidge
        flight_path = self.pts[tail:head]
        #no need to keep recalculating this, but it's quick.
        flight_path = flight_path+np.full_like(flight_path,0.05)
        fadeColors = np.array([(min([(i/TAIL_LENGTH)**1.5,0.3]),0,0,1) for i in range(TAIL_LENGTH)])
        if CUDA : fadeColors = fadeColors.get()
        projColors = np.array([(0.2,0.2,min([(i/TAIL_LENGTH)**1.5,0.5]),1) for i in range(TAIL_LENGTH)])
        self.flight = gl.GLLinePlotItem(width=5,pos=flight_path.get() if CUDA else flight_path,color=fadeColors) #, size=3,pxMode=True)
        
        X_flight_path = flight_path.copy(); X_flight_path[::,1]=-10
        self.X_flight=gl.GLLinePlotItem(width=1 if not PRESENTATION_MODE else PRESENTATION_WIDTH,pos=X_flight_path.get() if CUDA else X_flight_path,color=projColors)
        Z_flight_path = flight_path.copy(); Z_flight_path[::,2]=-10
        self.Z_flight=gl.GLLinePlotItem(width=1 if not PRESENTATION_MODE else PRESENTATION_WIDTH,pos=Z_flight_path.get() if CUDA else Z_flight_path,color=projColors)

        
        g_w.addItem(self.flight)
        g_w.addItem(self.X_flight)
        g_w.addItem(self.Z_flight)

        #g_last_plot=plot


# Calculate the constants of motion, Energy (E), Angular momentum (L_z), and Carter Constant (Q) 

def lay_grids(w):
    grid_color=(0,96,0,128)
    gx = gl.GLGridItem(color=grid_color)
    
    gx.rotate(90, 0, 1, 0)
    gx.translate(-10, 0, 0)
    w.addItem(gx)
    gy = gl.GLGridItem(color=grid_color)
    gy.rotate(90, 1, 0, 0)
    gy.translate(0, -10, 0)
    w.addItem(gy)
    gz = gl.GLGridItem(color=grid_color)
    gz.translate(0, 0, -10)
    w.addItem(gz)




def unwind_range(rng):
    #Just not in the mood for recursion with just 3 params :
    #
    param_space=[]
    a_r = np.linspace(rng['a'][0], rng['a'][1],rng['a'][2]) if len(rng['a'])>1 else np.array(rng['a'])
    p_r = np.linspace(rng['p'][0], rng['p'][1],rng['p'][2]) if len(rng['p'])>1 else np.array(rng['p'])
    t_r = np.linspace(rng['theta'][0], rng['theta'][1],rng['theta'][2]) if len(rng['theta'])>1 else np.array(rng['theta'])
    for a_i in a_r:
        for p_i in p_r:
            for t_i in t_r:
                #print(a_i,p_i,t_i)
                param_space.append((a_i.item(),p_i.item(),t_i.item()))
    #return np.array(param_space

g_w = None
g_last_plot=None
def do_plot(a,p,e,theta,nsteps):
    global g_last_plot
    global lib
    #rng={
    #    'a':[0,1,50],
    #    'p':[6],
    #    'theta':[16]
    #}
    #unwind_range(rng)
    #sys.exit(0)
    #code.interact(local=dict(globals(), **locals()))
    

    lib.go_4(c_float(a),c_float(p),c_float(e),c_float(theta),c_t_evs,c_arr_out,nsteps*REVS)
    pts = np.array(c_arr_out).reshape((nsteps*REVS,NUM_SCALARS))
    #Qt.QCoreApplication.processEvents()
    #pts = do_orbits()  # parameterize and parallelize here
    plot = gl.GLLinePlotItem(pos=pts.get() if CUDA else pts,color=pg.mkColor(128,128,128,255) if PRESENTATION_MODE else pg.mkColor(255,255,255,255), width=1 if not PRESENTATION_MODE else PRESENTATION_WIDTH) #, size=3,pxMode=True)
    plot.setDepthValue(10)
    if g_last_plot : g_w.removeItem(g_last_plot)
    g_w.addItem(plot)
    g_last_plot=plot
    return pts
def render(_w):
    global g_w
    w = _w.openGLWidget
    g_w = w
    w.opts['distance'] = 40
    w.show()
    w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
    lay_grids(w)
    _w.pushCB()
    #do_orbits(w)

null_timer=None

if __name__ == "__main__":    
    #pts = do_orbits()  # parameterize and parallelize here
    #pushCB()
    #sys.exit(0)


    
    import sys
    rng={
        'a':[0,1,50],
        'p':[6],
        'theta':[16]
    }
    param_space=unwind_range(rng)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    render(ui)
    #https://machinekoder.com/how-to-not-shoot-yourself-in-the-foot-using-python-qt/
    #--- do nothing timer to enable ctrl-C despite Qt event loop
    null_timer = QtCore.QTimer()
    null_timer.timeout.connect(lambda: None)
    null_timer.start(100)
    MainWindow.show()
    sys.exit(app.exec_())
