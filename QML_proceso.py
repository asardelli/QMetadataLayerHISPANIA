# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QMetadataLayerHISPANIA
                                 A QGIS plugin
                              -------------------
        begin                : 2023-08-30
        copyright            : (C) 2023 by Aldo Sardelli
        email                : asardelli@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *  This program is covered by the terms of the GNU General Public License *
 *  <https://www.gnu.org/licenses/>.                                       *
 *                                                                         *
 ***************************************************************************/
"""
import sys
import os
from qgis.core import *
import processing
from qgis.utils import iface
from qgis.PyQt import QtCore, QtGui, QtWidgets
from qgis.PyQt.QtCore import QVariant, Qt
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtCore import pyqtSignal, QSettings, QTranslator, qVersion, QCoreApplication, Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QColor, QImage, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtXml import QDomDocument, QDomElement
from datetime import date, time, datetime
import webbrowser


# Import the code for the DockWidget
import os.path

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'QMetadataLayerHISPANIA.ui'))


class QwebDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(QwebDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()


class QML:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        #añadir un toolbar
        self.Qoilbar=self.iface.addToolBar("QMetadataLayer")
        #crear los botones
        icon_QMS_path = QIcon(os.path.dirname(__file__) + "/icono.png")
        self.action = QAction(icon_QMS_path,"Metadatos", self.iface.mainWindow())
        self.action.triggered.connect(self.runQMS)
        self.Qoilbar.addAction(self.action)
        self.iface.addPluginToMenu("QMetadataLayer", self.action)
        self.dockwidget = QwebDockWidget()
        #agregar items de visualización
        self.welcome()
        self.dockwidget.comboBoxTIPOMETADATO.currentTextChanged.connect(self.welcome)
        self.items1()
        self.dockwidget.pushButtonHOME1.clicked.connect(self.itemH)
        self.dockwidget.pushButtonINFO1.clicked.connect(self.itemIP)
        self.dockwidget.pushButtonIDENT1.clicked.connect(self.itemI)
        self.dockwidget.pushButtonEXT1.clicked.connect(self.itemE)
        self.dockwidget.pushButtonACCESS1.clicked.connect(self.itemA)
        self.dockwidget.pushButtonCONTACT.clicked.connect(self.itemC)
        self.dockwidget.pushButtonLINK1.clicked.connect(self.itemL)
        self.dockwidget.pushButtonHISTORY1.clicked.connect(self.itemHi)
        self.items2()
        self.dockwidget.toolBoxESCRIBIRMETA.currentChanged.connect(self.items2)
        self.dockwidget.pushButtonMASMENU.clicked.connect(self.changeItems2)
        self.dockwidget.comboBoxTIPOMETADATO.currentTextChanged.connect(self.leermeta1)
        iface.currentLayerChanged.connect(self.leermeta1)
        self.ActiveIcon()
        self.icon()
        self.dockwidget.radioButtonANCLARCAPA.clicked.connect(self.ActiveIcon)
        self.dockwidget.comboBoxACCION.currentTextChanged.connect(self.ActivePushboton2)
        self.dockwidget.tabWidgetMETADATO.currentChanged.connect(self.comboboxList)
        iface.currentLayerChanged.connect(self.comboboxList)
        self.dockwidget.comboBoxCAPASEL.currentTextChanged.connect(self.comboboxList)
        self.dockwidget.comboBoxCATEGORIA.currentTextChanged.connect(self.addCat)
        self.dockwidget.pushButtonVERABS.clicked.connect(self.readAbstract)
        self.dockwidget.lineEditCONCEPTOPC.textChanged.connect(self.keywordsBotton)
        self.dockwidget.lineEditITEMSPC.textChanged.connect(self.keywordsBotton)
        self.dockwidget.pushButtonAGREGARPC.clicked.connect(self.addkeywords)
        self.dockwidget.pushButtonCALCULARXYCAPA.clicked.connect(self.XYlayer)
        self.dockwidget.comboBoxCAPAEXT.currentTextChanged.connect(self.extendBotton)
        self.dockwidget.pushButtonCALCULOZMAXMIN.clicked.connect(self.Zmaxmin)
        self.dockwidget.comboBoxCAMPOZ.currentTextChanged.connect(self.zvalueBotton)
        self.dockwidget.pushButtonAGREGARLIC.clicked.connect(self.addLicences)
        self.dockwidget.comboBoxLICENCIAS.currentTextChanged.connect(self.licenseBotton)
        self.dockwidget.comboBoxROL.currentTextChanged.connect(self.addRol)
        self.dockwidget.tabWidgetMETADATO.currentChanged.connect(self.readLayer2)
        iface.currentLayerChanged.connect(self.readLayer2)
        self.dockwidget.radioButtonANCLARCAPA.clicked.connect(self.readLayer2)
        self.dockwidget.pushButtonVARIABLES.clicked.connect(self.readvariable)
        self.dockwidget.pushButtonLEERMETA.clicked.connect(self.leermetaSeleccionada)
        self.dockwidget.pushButtonLEERMETAOTRO.clicked.connect(self.leermetaOtra)
        self.dockwidget.pushButtonLIMPIAR.clicked.connect(self.clear2)
        self.dockwidget.comboBoxACCION.currentTextChanged.connect(self.resumenMetadato)
        self.dockwidget.pushButtonAGREGARMETADATO.clicked.connect(self.setMetadatos)
        self.autocomplet()
        self.dockwidget.lineEditCIUDAD.textChanged.connect(self.cityPOSTAL)
        self.activeLayer()
        iface.currentLayerChanged.connect(self.activeLayer)
        self.dockwidget.pushButtonLOAD3.clicked.connect(self.loadMetadata)
        self.dockwidget.pushButtonSAVE3.clicked.connect(self.saveMetadata)
        self.dockwidget.pushButtonOPEN3.clicked.connect(self.openFile)
        self.dockwidget.pushButtonSAVEEDIT3.clicked.connect(self.saveFile)
        QgsProject.instance().readProject.connect(self.newProject)
    
    
    
    #-------------------------------------------------------------------Previo
    def icon(self):
        #home
        data11 = QIcon(os.path.dirname(__file__) + "/img/home.png")
        self.dockwidget.pushButtonHOME1.setIcon(data11)
        self.dockwidget.pushButtonHOME1.setStyleSheet("background-color: #3399FF ")
        #Information
        data12 = QIcon(os.path.dirname(__file__) + "/img/information.png")
        self.dockwidget.pushButtonINFO1.setIcon(data12)
        #read variable
        data21 = QIcon(os.path.dirname(__file__) + "/img/read_variable.png")
        self.dockwidget.pushButtonVARIABLES.setIcon(data21)
        self.dockwidget.pushButtonVARIABLES.setIconSize(QSize(30,15))
        #read metadata 
        data22 = QIcon(os.path.dirname(__file__) + "/img/read_md.png")
        self.dockwidget.pushButtonLEERMETA.setIcon(data22)
        self.dockwidget.pushButtonLEERMETA.setIconSize(QSize(30,15))
        #read metadata other
        data23 = QIcon(os.path.dirname(__file__) + "/img/read_md_other.png")
        self.dockwidget.pushButtonLEERMETAOTRO.setIcon(data23)
        self.dockwidget.pushButtonLEERMETAOTRO.setIconSize(QSize(30,15))
        #clear
        data24 = QIcon(os.path.dirname(__file__) + "/img/clear.png")
        self.dockwidget.pushButtonLIMPIAR.setIcon(data24)
        self.dockwidget.pushButtonLIMPIAR.setIconSize(QSize(30,15))
        #identification
        data25 = QIcon(os.path.dirname(__file__) + "/img/identification.png")
        self.dockwidget.pushButtonIDENT1.setIcon(data25)
        self.dockwidget.toolBoxESCRIBIRMETA.setItemIcon(0,data25)
        #extent
        data26 = QIcon(os.path.dirname(__file__) + "/img/extent.png")
        self.dockwidget.pushButtonEXT1.setIcon(data26)
        self.dockwidget.toolBoxESCRIBIRMETA.setItemIcon(1,data26)
        #access
        data27 = QIcon(os.path.dirname(__file__) + "/img/access.png")
        self.dockwidget.pushButtonACCESS1.setIcon(data27)
        self.dockwidget.toolBoxESCRIBIRMETA.setItemIcon(2,data27)
        #contact
        data28 = QIcon(os.path.dirname(__file__) + "/img/contact.png")
        self.dockwidget.pushButtonCONTACT.setIcon(data28)
        self.dockwidget.toolBoxESCRIBIRMETA.setItemIcon(3,data28)
        #link
        data29 = QIcon(os.path.dirname(__file__) + "/img/link.png")
        self.dockwidget.pushButtonLINK1.setIcon(data29)
        self.dockwidget.toolBoxESCRIBIRMETA.setItemIcon(4,data29)
        #history
        data210 = QIcon(os.path.dirname(__file__) + "/img/history.png")
        self.dockwidget.pushButtonHISTORY1.setIcon(data210)
        self.dockwidget.toolBoxESCRIBIRMETA.setItemIcon(5,data210)
        #astract
        data211 = QIcon(os.path.dirname(__file__) + "/img/astract.png")
        self.dockwidget.toolBoxESCRIBIRMETA.setItemIcon(6,data211)
        #Load File
        data31 = QIcon(os.path.dirname(__file__) + "/img/load_file.png")
        self.dockwidget.pushButtonLOAD3.setIcon(data31)
        self.dockwidget.pushButtonLOAD3.setIconSize(QSize(50,50))
        #Open File
        data32 = QIcon(os.path.dirname(__file__) + "/img/open_file.png")
        self.dockwidget.pushButtonOPEN3.setIcon(data32)
        self.dockwidget.pushButtonOPEN3.setIconSize(QSize(50,50))
        #Save File
        data33 = QIcon(os.path.dirname(__file__) + "/img/save_file.png")
        self.dockwidget.pushButtonSAVE3.setIcon(data33)
        self.dockwidget.pushButtonSAVE3.setIconSize(QSize(50,50))
        #Save edit
        data34 = QIcon(os.path.dirname(__file__) + "/img/save_edit.png")
        self.dockwidget.pushButtonSAVEEDIT3.setIcon(data34)
        self.dockwidget.pushButtonSAVEEDIT3.setIconSize(QSize(50,50))
        
    #-------------------------------------------------------------------Pestaña 1
    def welcome(self):
        Items=serie=self.dockwidget.comboBoxTIPOMETADATO.currentText()
        #Información del proveedor
        if Items=='Seleccionar':
            self.dockwidget.textBrowserLEERMETA.clear()
            self.dockwidget.textBrowserLEERMETA.append(' '*12+'___'+' '*23+'___'+' '*6)
            self.dockwidget.textBrowserLEERMETA.append(' '*11+'/\__\ '+' '*20+'/\    \    ')
            self.dockwidget.textBrowserLEERMETA.append(' '*10+'/::|    |'+' '*17+' /::\    \   ')
            self.dockwidget.textBrowserLEERMETA.append(' '*9+'/:|:|    |'+' '*15+' /:/\:\    \  ')
            self.dockwidget.textBrowserLEERMETA.append(' '*8+'/:/|:|__|___        /:/   \:\__\ ')
            self.dockwidget.textBrowserLEERMETA.append(' '*7+'/:/ |:::::::\__\     /:/_/  \:|__|')
            self.dockwidget.textBrowserLEERMETA.append(' '*7+'\/__/~~ /:/   /     \:\  \  /:/    /')
            self.dockwidget.textBrowserLEERMETA.append(' '*20+'/:/   /        \:\  /:/    / ')
            self.dockwidget.textBrowserLEERMETA.append(' '*19+'/:/   /          \:\/:/    /  ')
            self.dockwidget.textBrowserLEERMETA.append(' '*18+'/:/   /            \::/__/   ')
            self.dockwidget.textBrowserLEERMETA.append(' '*18+'\/__/              ~        ')
            self.dockwidget.textBrowserLEERMETA.append(' '*21+'QMetadataLayer')
            self.dockwidget.textBrowserLEERMETA.append('')
            self.dockwidget.textBrowserLEERMETA.append(' '*5+'+'*23)
            self.dockwidget.textBrowserLEERMETA.append(' '*5+"+"+" "*10+'H  I   S   P   A   N   I  A'+' '*11+'+')
            self.dockwidget.textBrowserLEERMETA.append(' '*5+'+'*23)
            self.dockwidget.textBrowserLEERMETA.append(' '*53+'asardelli')
        else:
            pass
    
    
    def items1(self):
        #se limpian las listas
        self.dockwidget.comboBoxTIPOMETADATO.clear()
        self.dockwidget.comboBoxTIPOMETADATO.addItem('Seleccionar')
        Items=['Información del proveedor','Identificación','Extensión','Acceso', 'Contactos','Enlaces','Historia']
        for s in Items:
            self.dockwidget.comboBoxTIPOMETADATO.addItem(s)
            
    def colorBotton1(self,colorH, colorIP, colorI, colorE, colorA, colorC, colorL, colorHi):
        self.dockwidget.pushButtonHOME1.setStyleSheet(f"background-color: {colorH}")
        self.dockwidget.pushButtonINFO1.setStyleSheet(f"background-color: {colorIP}")
        self.dockwidget.pushButtonIDENT1.setStyleSheet(f"background-color: {colorI}")
        self.dockwidget.pushButtonEXT1.setStyleSheet(f"background-color: {colorE}")
        self.dockwidget.pushButtonACCESS1.setStyleSheet(f"background-color: {colorA}")
        self.dockwidget.pushButtonCONTACT.setStyleSheet(f"background-color: {colorC}")
        self.dockwidget.pushButtonLINK1.setStyleSheet(f"background-color: {colorL}")
        self.dockwidget.pushButtonHISTORY1.setStyleSheet(f"background-color: {colorHi}")
    
    
    def itemH(self):
        self.dockwidget.comboBoxTIPOMETADATO.setCurrentText('Seleccionar')
        
    def itemIP(self):
        self.dockwidget.comboBoxTIPOMETADATO.setCurrentText('Información del proveedor')
        
    def itemI(self):
        self.dockwidget.comboBoxTIPOMETADATO.setCurrentText('Identificación')
        
    def itemE(self):
        self.dockwidget.comboBoxTIPOMETADATO.setCurrentText('Extensión')
        
    def itemA(self):
        self.dockwidget.comboBoxTIPOMETADATO.setCurrentText('Acceso')
        
    def itemC(self):
        self.dockwidget.comboBoxTIPOMETADATO.setCurrentText('Contactos')
        
    def itemL(self):
        self.dockwidget.comboBoxTIPOMETADATO.setCurrentText('Enlaces')
        
    def itemHi(self):
        self.dockwidget.comboBoxTIPOMETADATO.setCurrentText('Historia')
    
    def leermeta1(self):
        try:
            # Obtener la capa actualmente seleccionada en QGIS
            capa = iface.activeLayer()
            nameC=capa.name()
            #Se lee el combobox
            Items=serie=self.dockwidget.comboBoxTIPOMETADATO.currentText()
            #Información del proveedor
            if Items=='Información del proveedor':
                self.colorBotton1(None, "#3399FF", None, None, None, None, None, None)
                self.dockwidget.textBrowserLEERMETA.clear()
                nombreC=capa.name()
                self.dockwidget.textBrowserLEERMETA.append(f'<b>Nombre:</b> {nombreC}')
                self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                fuenteC=capa.source()
                self.dockwidget.textBrowserLEERMETA.append(f'<b>Fuente:</b> {fuenteC}')
                self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                almacenamientoC=capa.storageType()
                self.dockwidget.textBrowserLEERMETA.append(f'<b>Almacenamiento:</b> {almacenamientoC}')
                self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                comentarioC=capa.dataComment()
                self.dockwidget.textBrowserLEERMETA.append(f'<b>Comentario:</b> {comentarioC}')
                self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                codificacionC=capa.dataProvider().encoding()
                self.dockwidget.textBrowserLEERMETA.append(f'<b>Codificación:</b> {codificacionC}')
                self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                part=capa.wkbType()
                if part==6:
                    Text='Polígono(MultiPolygon)'
                elif part==5:
                    Text='Línea(MultiLineString)'
                elif part==4:
                    Text='Punto(MultiPoint)'
                elif part==3:
                    Text='Polígono(Polygon)'
                elif part==2:
                    Text='Línea(LineString)'
                elif part==1:
                    Text='Punto(Point)'
                else:
                    Text=None
                self.dockwidget.textBrowserLEERMETA.append(f'<b>Geometría:</b> {Text}')
                self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                CRS=capa.metadata().crs().authid()
                CRS_Desc=capa.crs().description()
                self.dockwidget.textBrowserLEERMETA.append(f'<b>SRC:</b> {CRS} - {CRS_Desc}')
                self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                ext=capa.extent()
                xmin = ext.xMinimum()
                xmax = ext.xMaximum()
                ymin = ext.yMinimum()
                ymax = ext.yMaximum()
                coords = "%f,%f:%f,%f" %(xmin,ymin, xmax, ymax)
                self.dockwidget.textBrowserLEERMETA.append(f'<b>Extensión:</b> {coords}')
                self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
    #            unidadC=capa.unit()
    #            self.dockwidget.textBrowserLEERMETA.append(f'Unidad: {unidadC}')
    #            self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                numfeatures=capa.featureCount()
                self.dockwidget.textBrowserLEERMETA.append(f'<b>Número de objetos:</b> {numfeatures}')
                self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
            #Identificación
            elif Items=='Identificación':
                self.colorBotton1(None, None, "#3399FF", None, None, None, None, None)
                self.dockwidget.textBrowserLEERMETA.clear()
                #Se crean las listas
                datos={}
                clave=['Identificador','Identificador Origen','Título','Tipo','Idioma','Resumen',\
                'Categoría','Palabras Clave']
                valor=[]
                #se lee los datos
                if capa is not None:
                    ident=capa.metadata().identifier()
                    text =f'<b>Identificador:</b> {ident}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    iden_origen=capa.metadata().parentIdentifier()
                    text =f'<b>Identificador Origen:</b> {iden_origen}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    titulo=capa.metadata().title()
                    text =f'<b>Título:</b> {titulo}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    tipo_D=capa.metadata().type()
                    text =f'<b>Tipo:</b> {tipo_D}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    idioma=capa.metadata().language()
                    text =f'<b>Idioma:</b> {idioma}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    Resumen=capa.metadata().abstract()
                    text =f'<b>Resumen:</b> {Resumen}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    Categoria=capa.metadata().categories()
                    Keywords=capa.metadata().keywords()
                    self.dockwidget.textBrowserLEERMETA.append(f'<b>Categorías</b>')
                    for c in Categoria:
                        self.dockwidget.textBrowserLEERMETA.append(c)
                    self.dockwidget.textBrowserLEERMETA.append(f'<b>Palabras Clave</b>')
                    for d in Keywords:
                        self.dockwidget.textBrowserLEERMETA.append(f'<u>{d}</u>')
                        for x in Keywords[d]:
                            text =f'{x}'
                            self.dockwidget.textBrowserLEERMETA.append(text)
                else:
                    pass
                
                self.dockwidget.textBrowserLEERMETA.append('')
                self.dockwidget.textBrowserLEERMETA.append('***********************************')
                self.dockwidget.textBrowserLEERMETA.append(f'Capa: <b>{nameC}</b>')
            elif Items=='Extensión':
                self.colorBotton1(None, None, None, "#3399FF", None, None, None, None)
                self.dockwidget.textBrowserLEERMETA.clear()
                nume_SP=len(capa.metadata().extent().spatialExtents())
                for s in range (nume_SP):
                    v=s+1
                    self.dockwidget.textBrowserLEERMETA.append(f'<u>Extensión {v}</u>')
                    self.dockwidget.textBrowserLEERMETA.append(f'')
                    self.dockwidget.textBrowserLEERMETA.append(f'<b>Extensión Espacial</b>')
                    CRS=capa.metadata().crs().authid()
                    CRS_Desc=capa.crs().description()
                    text=f'<b>CRS:</b> {CRS} - {CRS_Desc}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    Xmin=capa.metadata().extent().spatialExtents()[s].bounds.xMinimum()
                    text =f'<b>X Mínimo:</b> {Xmin}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    Ymin=capa.metadata().extent().spatialExtents()[s].bounds.yMinimum()
                    text =f'<b>Y Mínimo:</b> {Ymin}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    Xmax=capa.metadata().extent().spatialExtents()[s].bounds.xMaximum()
                    text =f'<b>X Maxímo:</b> {Xmax}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    Ymax=capa.metadata().extent().spatialExtents()[s].bounds.yMaximum()
                    text =f'<b>Y Maxímo:</b> {Ymax}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    Zmax=capa.metadata().extent().spatialExtents()[s].bounds.zMaximum()
                    text =f'<b>Z Maxímo:</b> {Zmax}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    Zmin=capa.metadata().extent().spatialExtents()[s].bounds.zMinimum()
                    text =f'<b>Z Mínimo:</b> {Zmin}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                    self.dockwidget.textBrowserLEERMETA.append(f'<b>Extensión Temporal</b>')
                    start=capa.metadata().extent().temporalExtents()[s].begin().toString()
                    text =f'<b>Desde:</b> {start}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    end=capa.metadata().extent().temporalExtents()[s].end().toString()
                    text =f'<b>Hasta:</b> {end}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    self.dockwidget.textBrowserLEERMETA.append('============================')
                self.dockwidget.textBrowserLEERMETA.append('')
                self.dockwidget.textBrowserLEERMETA.append('***********************************')
                self.dockwidget.textBrowserLEERMETA.append(f'Capa: <b>{nameC}</b>')
            elif Items=='Acceso':
                self.colorBotton1(None, None, None, None, "#3399FF", None, None, None)
                self.dockwidget.textBrowserLEERMETA.clear()
                #se lee los datos
                if capa is not None:
                    Cuota=capa.metadata().fees()
                    text =f'<b>Cuota:</b> {Cuota}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    Licencias=capa.metadata().licenses()
                    text =f'<b>Licencias:</b> {Licencias}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    Derechos=capa.metadata().rights()
                    text =f'<b>Derechos:</b> {Derechos}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    self.dockwidget.textBrowserLEERMETA.append(f'<b>Restricciones:</b>')
                    #numero de restricciones
                    num_R=len(capa.metadata().constraints())
                    for r in range (num_R):
                        k=r+1
                        self.dockwidget.textBrowserLEERMETA.append(f'<u>Restricción {k}</u>')
                        Restriccion=capa.metadata().constraints()[r].constraint
                        tipoR=capa.metadata().constraints()[r].type
                        text =f'<b>{tipoR}:</b> {Restriccion}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                else:
                    pass
                self.dockwidget.textBrowserLEERMETA.append('')
                self.dockwidget.textBrowserLEERMETA.append('***********************************')
                self.dockwidget.textBrowserLEERMETA.append(f'Capa: <b>{nameC}</b>')
            elif Items=='Contactos':
                self.colorBotton1(None, None, None, None, None, "#3399FF", None, None)
                self.dockwidget.textBrowserLEERMETA.clear()
                #Se ddetermina el numero de contactos y el numero de direccioanes por contacto
                num_C=len(capa.metadata().contacts())
                #se lee los datos
                for n in range(num_C):
                    if capa is not None:
                        s=n+1
                        self.dockwidget.textBrowserLEERMETA.append(f'<u> Contacto {s}</u>')
                        Nombre=capa.metadata().contacts()[n].name
                        text =f' <b>Nombre:</b> {Nombre}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        Rol=capa.metadata().contacts()[n]. role
                        text =f'<b>Rol:</b> {Rol}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        Organización=capa.metadata().contacts()[n].organization
                        text =f'<b>Organizaciónl:</b> {Organización}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        Posicion=capa.metadata().contacts()[n].position
                        text =f'<b>Posición:</b> {Posicion}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        Email=capa.metadata().contacts()[n].email
                        text =f'<b>Correo Electrónico:</b> {Email}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        Phone1=capa.metadata().contacts()[n].voice
                        text =f'<b>Número Telefónico:</b> {Phone1}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        Phone2=capa.metadata().contacts()[n].fax
                        text =f'<b>Otro Número:</b> {Phone2}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                        #direccion
                        num_D=len(capa.metadata().contacts()[n].addresses)
                        for d in range(num_D):
                            f=d+1
                            self.dockwidget.textBrowserLEERMETA.append(f'<u>Dirección {f} del contacto {s}</u>')
                            TipoD=capa.metadata().contacts()[n].addresses[d].type
                            text =f'<b>Tipo de dirección:</b> {TipoD}'
                            self.dockwidget.textBrowserLEERMETA.append(text)
                            CodPos=capa.metadata().contacts()[n].addresses[d].postalCode
                            text =f'<b>Código Postal:</b> {CodPos}'
                            self.dockwidget.textBrowserLEERMETA.append(text)
                            Dirección=capa.metadata().contacts()[n].addresses[d].address
                            text =f'<b>Dirección:</b> {Dirección}'
                            self.dockwidget.textBrowserLEERMETA.append(text)
                            Pais=capa.metadata().contacts()[n].addresses[d].country
                            text =f'<b>País:</b> {Pais}'
                            self.dockwidget.textBrowserLEERMETA.append(text)
                            Areadmin=capa.metadata().contacts()[n].addresses[d].administrativeArea
                            text =f'<b>Área Administrativa:</b> {Areadmin}'
                            self.dockwidget.textBrowserLEERMETA.append(text)
                            Ciudad=capa.metadata().contacts()[n].addresses[d].city
                            text =f'<b>Ciudad:</b> {Ciudad}'
                            self.dockwidget.textBrowserLEERMETA.append(text)
                            self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                        self.dockwidget.textBrowserLEERMETA.append('============================')
                    else:
                        pass
                self.dockwidget.textBrowserLEERMETA.append('')
                self.dockwidget.textBrowserLEERMETA.append('***********************************')
                self.dockwidget.textBrowserLEERMETA.append(f'Capa: <b>{nameC}</b>')
            elif Items=='Enlaces':
                self.colorBotton1(None, None, None, None, None, None, "#3399FF", None)
                self.dockwidget.textBrowserLEERMETA.clear()
                #se determina el numero de link
                num_L=len(capa.metadata().links())
                #se lee los datos
                for l in range (num_L):
                    if capa is not None:
                        e=l+1
                        self.dockwidget.textBrowserLEERMETA.append(f'<u>Enlace {e}</u>')
                        NombreE=capa.metadata().links()[l].name
                        text =f'<b>Nombre:</b> {NombreE}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        TipoE=capa.metadata().links()[l].type
                        text =f'<b>Tipo:</b> {TipoE}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        URL=capa.metadata().links()[l].url
                        text =f'<b>URL:</b> {URL}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        DescripcionE=capa.metadata().links()[l].description
                        text =f'<b>Descripción:</b> {DescripcionE}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        Formato=capa.metadata().links()[l].format
                        text =f'<b>Formato:</b> {Formato}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        MIME=capa.metadata().links()[l].mimeType
                        text =f'<b>MIME:</b> {MIME}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        Tamano=capa.metadata().links()[l].size
                        text =f'<b>Tamaño:</b> {Tamano}'
                        self.dockwidget.textBrowserLEERMETA.append(text)
                        self.dockwidget.textBrowserLEERMETA.append('============================')
                    else:
                        pass
                self.dockwidget.textBrowserLEERMETA.append('')
                self.dockwidget.textBrowserLEERMETA.append('***********************************')
                self.dockwidget.textBrowserLEERMETA.append(f'Capa: <b>{nameC}</b>')
            elif Items=='Historia':
                self.colorBotton1(None, None, None, None, None, None, None, "#3399FF")
                self.dockwidget.textBrowserLEERMETA.clear()
                #se lee los datos
                if capa is not None:
                    Hist=capa.metadata().history()
                else:
                    pass
                for s in range (len(Hist)):
                    d=Hist[s]
                    a=s+1
                    text =f'<b>{a}:</b> {d}'
                    self.dockwidget.textBrowserLEERMETA.append(text)
                    self.dockwidget.textBrowserLEERMETA.append('-------------------------------')
                self.dockwidget.textBrowserLEERMETA.append('')
                self.dockwidget.textBrowserLEERMETA.append('***********************************')
                self.dockwidget.textBrowserLEERMETA.append(f'Capa: <b>{nameC}</b>')
            else:
                self.colorBotton1("#3399FF", None, None, None, None, None, None, None)
        except:
            pass
    
    #-------------------------------------------------------------------Pestaña 2
    
    def cityPOSTAL(self):
        #se abre el archivo
        archivoCC = open (os.path.dirname(__file__) + f"/default/ciudades_es.txt" , "r",encoding='utf-8-sig')
        #se lee
        contenidoCC = archivoCC . read ( )
        archivoCC.close()
        #se repara
        contenidoCC = contenidoCC . replace ('"','')
        contenidoCC = contenidoCC . replace ("'","")
        city_cpListVe=contenidoCC. split (",")
        cityDicKeyVe=[]
        cityDicValorVe=[]
        cityDicVe={}
        n=0
        for c in city_cpListVe:
            n1=n%2
            if n1==0:
                cityDicKeyVe.append(c)
            else:
                c = c . replace (" ","")
                cityDicValorVe.append(c)
            n=n+1
        city=self.dockwidget.lineEditCIUDAD.text()
        city=str(city)
        if city in cityDicKeyVe:
            idc=cityDicKeyVe.index(city)
            self.dockwidget.lineEditCODIGOPOSTAL.setText(cityDicValorVe[idc])
    
    
    def ActiveIcon(self):
        # set QImagen as label
        if self.dockwidget.radioButtonANCLARCAPA.isChecked()==False:
            data = QImage(os.path.dirname(__file__) + "/img/inactivo.png")
            pixmap = QPixmap(data).scaledToHeight(15, Qt.SmoothTransformation)
            self.dockwidget.labelACTIVO.setPixmap(pixmap)
            self.dockwidget.label_MENSAJE2.setStyleSheet("background-color: None")
            self.dockwidget.label_MENSAJE2.setText('')
        else:
            data = QImage(os.path.dirname(__file__) + "/img/activo.png")
            pixmap = QPixmap(data).scaledToHeight(15, Qt.SmoothTransformation)
            self.dockwidget.labelACTIVO.setPixmap(pixmap)
            self.dockwidget.label_MENSAJE2.setStyleSheet("background-color: #ff8000")
            self.dockwidget.label_MENSAJE2.setText('<b>¡CUIDADO!</b>. Capa fijada, <b><u>NO</u></b> debe eliminarla del proyecto.')
    
    def keywordsBotton(self):
        concepKeywords=self.dockwidget.lineEditCONCEPTOPC.text()
        itmesKeywords=self.dockwidget.lineEditITEMSPC.text()
        if len(concepKeywords)>0 and len(itmesKeywords)>0:
            self.dockwidget.pushButtonAGREGARPC.setStyleSheet("background-color: #3399FF")
        else:
            self.dockwidget.pushButtonAGREGARPC.setStyleSheet("background-color: none")
    
    def extendBotton(self):
        extend = self.dockwidget.comboBoxCAPAEXT.currentText()
        if extend!='...':
            self.dockwidget.pushButtonCALCULARXYCAPA.setStyleSheet("background-color: #3399FF")
        else:
            self.dockwidget.pushButtonCALCULARXYCAPA.setStyleSheet("background-color: none")
            
    def zvalueBotton(self):
        zvalue = self.dockwidget.comboBoxCAMPOZ.currentText()
        if zvalue!='Seleccionar':
            self.dockwidget.pushButtonCALCULOZMAXMIN.setStyleSheet("background-color: #3399FF")
        else:
            self.dockwidget.pushButtonCALCULOZMAXMIN.setStyleSheet("background-color: none")
            
    def licenseBotton(self):
        license = self.dockwidget.comboBoxLICENCIAS.currentText()
        if license!='Seleccionar':
            self.dockwidget.pushButtonAGREGARLIC.setStyleSheet("background-color: #3399FF")
        else:
            self.dockwidget.pushButtonAGREGARLIC.setStyleSheet("background-color: none")
    
    def items2(self):
        #Se agrega el icono
        data1 = QIcon(os.path.dirname(__file__) + "/img/mas.png")
        self.dockwidget.pushButtonMASMENU.setIcon(data1)
        self.dockwidget.pushButtonMASMENU.setIconSize(QSize(16,16))
        #se limpian las listas
        self.dockwidget.comboBoxACCION.clear()
        self.dockwidget.comboBoxACCION.addItem('Seleccionar')
        Items=['Agregar Metadatos','Adicionar Palabras Clave','Adicionar Restriciones',\
        'Adicionar un Contacto','Adicionar una Dirección','Adicionar un Link',\
        'Adicionar Historias']
        for s in Items:
            self.dockwidget.comboBoxACCION.addItem(s)
        self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(True)
        numitem=self.dockwidget.comboBoxACCION.count()
    
    def changeItems2(self):
        numitem=self.dockwidget.comboBoxACCION.count()
        if numitem==8:
            #Se agrega el icono
            data1 = QIcon(os.path.dirname(__file__) + "/img/menos.png")
            self.dockwidget.pushButtonMASMENU.setIcon(data1)
            self.dockwidget.pushButtonMASMENU.setIconSize(QSize(16,16))
            #se limpian las listas
            self.dockwidget.comboBoxACCION.clear()
            self.dockwidget.comboBoxACCION.addItem('Seleccionar')
            Items=['Agregar Metadatos','Adicionar Palabras Clave','Adicionar Restriciones',\
            'Adicionar un Contacto','Adicionar una Dirección','Adicionar un Link',\
            'Adicionar Historias','Modificar Metadatos','Remover Palabra Clave','Remover Restricción',\
            'Remover un Contacto','Remover una Dirección','Remover un Link','Remover Metadatos']
            for s in Items:
                self.dockwidget.comboBoxACCION.addItem(s)
            self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(True)
        else:
            #Se agrega el icono
            data1 = QIcon(os.path.dirname(__file__) + "/img/mas.png")
            self.dockwidget.pushButtonMASMENU.setIcon(data1)
            self.dockwidget.pushButtonMASMENU.setIconSize(QSize(16,16))
            #se limpian las listas
            self.dockwidget.comboBoxACCION.clear()
            self.dockwidget.comboBoxACCION.addItem('Seleccionar')
            Items=['Agregar Metadatos','Adicionar Palabras Clave','Adicionar Restriciones',\
            'Adicionar un Contacto','Adicionar una Dirección','Adicionar un Link',\
            'Adicionar Historias']
            for s in Items:
                self.dockwidget.comboBoxACCION.addItem(s)
            self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(True)
    
    
    def ActivePushboton2(self):
        accion=self.dockwidget.comboBoxACCION.currentText()
        if accion=='Seleccionar':
            self.dockwidget.textBrowserRESUMEN.clear()
            self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(True)
        else:
            self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(False)
            
    
    def dateHistory(self):
        fecha = date.today()
        self.dockwidget.textEditHISTORIA.append(f'{fecha}:')
    
    def readLayer2(self):
        try:
            if self.dockwidget.tabWidgetMETADATO.currentIndex()==1:
                if self.dockwidget.radioButtonANCLARCAPA.isChecked()==False:
                    capa=iface.activeLayer()
                    name=capa.name()
                    self.dockwidget.comboBoxCAPASEL.clear()
                    self.dockwidget.comboBoxCAPAEXT.clear()
                    self.dockwidget.comboBoxCAPASEL.addItem('...')
                    self.dockwidget.comboBoxCAPAEXT.addItem('...')
                    #se itera la lista de mapas que estan cargadas
                    for i in QgsProject.instance().mapLayers().values():
                        #se añaden los nombres al combobox
                        self.dockwidget.comboBoxCAPASEL.addItem(i.name(),i)
                        self.dockwidget.comboBoxCAPAEXT.addItem(i.name(),i)
                    self.dockwidget.comboBoxCAPASEL.setCurrentText(name)
                    self.dockwidget.comboBoxCAPAEXT.setCurrentText(name)
                else:
                    pass
            else:
                pass
        except:
            pass
    
    
    def comboboxList(self):
        try:
            if self.dockwidget.tabWidgetMETADATO.currentIndex()==1:
                if self.dockwidget.radioButtonANCLARCAPA.isChecked()==False:
                    # Obtener la capa seleccionada en QGIS
                    try:
                        capa = self.dockwidget.comboBoxCAPASEL.currentData()
                    except:
                        capa=iface.activeLayer()

                    lengList=['abk','aar','afr','aka','sqi','amh','ara','arg','hye','asm','ava','ave','aym',\
                    'aze','bam','bak','eus','bel','ben','bih','bis','bos','bre','bul','mya','cat','cha','che',\
                    'nya','zho','chv','cor','cos','cre','hrv','ces','dan','div','nld','dzo','eng','epo','est',\
                    'ewe','fao','fij','fin','fra','ful','glg','kat','deu','ell','grn','guj','hat','hau','heb',\
                    'her','hin','hmo','hun','ina','ind','ile','gle','ibo','ipk','ido','isl','ita','iku','jpn',\
                    'jav','kal','kan','kau','kas','kaz','khm','kik','kin','kir','kom','kon','kor','kur','kua',\
                    'lat','ltz','lug','lim','lin','lao','lit','lub','lav','glv','mkd','mlg','msa','mal','mlt',\
                    'mri','mar','mah','mon','nau','nav','nob','nde','nep','ndo','nno','nor','iii','nbl','oci',\
                    'oji','chu','orm','ori','oss','pan','pli','fas','pol','pus','por','que','roh','run','ron',\
                    'rus','san','srd','snd','sme','smo','sag','srp','gla','sna','sin','slk','slv','som','sot',\
                    'spa','sun','swa','ssw','swe','tam','tel','tgk','tha','tir','bod','tuk','tgl','tsn','ton',\
                    'tur','tso','tat','twi','tah','uig','ukr','urd','uzb','ven','vie','vol','wln','cym','wol',\
                    'fry','xho','yid','yor','zha','zul']
                    
                    country2List=['ABW','AFG','AGO','AIA','ALA','ALB','AND','ARE','ARG','ARM','ASM','ATA','ATF',\
                    'ATG','AUS','AUT','AZE','BDI','BEL','BEN','BES','BFA','BGD','BGR','BHR','BHS','BIH','BLM','BLR',\
                    'BLZ','BMU','BOL','BRA','BRB','BRN','BTN','BVT','BWA','CAF','CAN','CCK','CHE','CHL','CHN','CIV',\
                    'CMR','COD','COG','COK','COL','COM','CPV','CRI','CUB','CUW','CXR','CYM','CYP','CZE','DEU','DJI',\
                    'DMA','DNK','DOM','DZA','ECU','EGY','ERI','ESH','ESP','EST','ETH','FIN','FJI','FLK','FRA','FRO',\
                    'FSM','GAB','GBR','GEO','GGY','GHA','GIB','GIN','GLP','GMB','GNB','GNQ','GRC','GRD','GRL','GTM',\
                    'GUF','GUM','GUY','HKG','HMD','HND','HRV','HTI','HUN','IDN','IMN','IND','IOT','IRL','IRN','IRQ',\
                    'ISL','ISR','ITA','JAM','JEY','JOR','JPN','KAZ','KEN','KGZ','KHM','KIR','KNA','KOR','KWT','LAO',\
                    'LBN','LBR','LBY','LCA','LIE','LKA','LSO','LTU','LUX','LVA','MAC','MAF','MAR','MCO','MDA','MDG',\
                    'MDV','MEX','MHL','MKD','MLI','MLT','MMR','MNE','MNG','MNP','MOZ','MRT','MSR','MTQ','MUS','MWI',\
                    'MYS','MYT','NAM','NCL','NER','NFK','NGA','NIC','NIU','NLD','NOR','NPL','NRU','NZL','OMN','PAK',\
                    'PAN','PCN','PER','PHL','PLW','PNG','POL','PRI','PRK','PRT','PRY','PSE','PYF','QAT','REU','ROU',\
                    'RUS','RWA','SAU','SDN','SEN','SGP','SGS','SHN','SJM','SLB','SLE','SLV','SMR','SOM','SPM','SRB',\
                    'SSD','STP','SUR','SVK','SVN','SWE','SWZ','SXM','SYC','SYR','TCA','TCD','TGO','THA','TJK','TKL',\
                    'TKM','TLS','TON','TTO','TUN','TUR','TUV','TWN','TZA','UGA','UKR','UMI','URY','USA','UZB','VAT',\
                    'VCT','VEN','VGB','VIR','VNM','VUT','WLF','WSM','YEM','ZAF','ZMB','ZWE']
                    
                    categoryListES=['Administración Pública y Gobierno','Agricultura','Aguas interiores','Biota',\
                    'Climatología, meteorología y atmósfera.','Cobertura de la Tierra con mapas básicos e imágenes',\
                    'Cuadrículas geográficas','Cubierta terrestre','Direcciones','Distribución de la población y demografía',\
                    'Distribución de las especies','Economía','Edificios','Elevación','Energía','Estructura','Geología',\
                    'Hábitats y biotopos','Hidrografía','Información geocientífica','Instalaciones de control del medioambiente',\
                    'Instalaciones de la agricultura y la acuicultura','Instalaciones industriales y de producción',\
                    'Inteligencia y militar','Justicia y Lenguaje','Límites','Localización','Lugares protegidos','Movilidad',\
                    'Medio ambiente','Nombres geográficos','Océanos','Ortoimágenes','Parcelas catastrales','Pérdida Climática',\
                    'Planeamiento catastral','Rasgos geográficos oceanográficos','Recursos energéticos','Recursos minerales',\
                    'Redes de suministro','Regiones biogeográficas','Regiones marinas','Salud y seguridad humanas',\
                    'Servicios de utilidad pública y estatales','Sistemas de coordenadas de referencia','Sociedad','Suelo',\
                    'Transporte','Unidades administrativas','Unidades estadísticas','Uso del suelo','Zonas de riesgos naturales',\
                    'Zonas sujetas a ordenación/a restricciones/reglamentaciones y unidades de notificación','Distribución',\
                    'Exploración y prospección','Información Oil & Gas','Ingeniería ','Instalaciones en Superficie',\
                    'Modelo de Yacimientos','Núcleos y Muestras','Oportunidad exploratoria','Perforación',\
                    'Planificación Presupuesto Gestion','Pozo','Producción','Proyectos pilotos','Recuperación Mejorada de Hidrocarburos',\
                    'Refinación','Seguridad  Higiene Ambiente','Well Log','Yacimientos',
]
                    
                    licencesList=['CC Zero','CC BY','CC BY-NC',\
                    'CC BY-NC-SA','CC Attribution 4.0','CC BY-SA 4.0',\
                    'Public Domain Dedication and Licence','Attribution License',\
                    'Open Database License']
                    
                    rolList=['author','coAuthor','collaborator','contributor','custodian','distribuidor','editor','funder','mediator','originator','owner','pointOfContact','principalInvestigator','processor','publisher','resourceProvider','rightsHolder','sponsor','stakeholder','user']
                    
                    postalcodList=['Postal','Virtual']
                    
                    linktypeList=['OGC:CSW','OGC:SOS','OGC:SPS','OGC:SAS','OGC:WNS','OGC:WCS','OGC:WFS',\
                    'OGC:WMS','OGC:WMS-C','OGC:WMTS','OGC:WPS','OGC:ODS','OGC:OGS','OGC:OUS','OGC:OPS',\
                    'OGC:ORS','OGC:CT','OGC:WFS-G','OGC:OWC','OGC:GPKG','OGC:IoT','ESRI:ArcIMS','ESRI:ArcGIS',\
                    'ESRI:MPK','OPeNDAP:OPeNDAP','OPeNDAP:Hyrax','UNIDATA:NCSS','UNIDATA:CDM',\
                    'UNIDATA:CdmRemote','UNIDATA:CdmrfEATURE','UNIDATA:THREDDS','OGC:GML','WWW:LINK',\
                    'WWW:WSDL','WWW:SPARQL:1.1','OpenSearch1.1','OpenSearch1.1:Description','information',\
                    'template','download','service','order','search','esip:CollectionCast','tilejson:2.0.0',\
                    'iris:fdsnws-event','QuakeML1.2','file','ISO 195:2003/19139','ISO-USGIN','http','https',\
                    'ftp','IETF:GeoJSON','GIT','OKFN:datapackage','boundless:geogig','OASIS:OData:4.0',\
                    'maxogden:dat','geoserver:rest','google:protocol-buffers','google:fusion-tables','NOAA:LAS',\
                    'OSM','ERDDAP:griddap','ERDDAP:tabledap','OASIS:AMQP']
                    
                    
                    #Rellenar combobox
                    #Language cod2
                    self.dockwidget.comboBoxIDIOMAID.clear()
                    self.dockwidget.comboBoxIDIOMAID.addItem('...')
                    for s in lengList:
                        self.dockwidget.comboBoxIDIOMAID.addItem(s)
                    
                    #Country cod2
                    self.dockwidget.comboBoxIDIOMAPAIS.clear()
                    self.dockwidget.comboBoxIDIOMAPAIS.addItem('...')
                    for s in country2List:
                        self.dockwidget.comboBoxIDIOMAPAIS.addItem(s)
                    
                    #Category spanish
                    self.dockwidget.comboBoxCATEGORIA.clear()
                    self.dockwidget.comboBoxCATEGORIA.addItem('Seleccionar')
                    for s in categoryListES:
                        self.dockwidget.comboBoxCATEGORIA.addItem(s)
                    #Field Z
                    try:
                        #se crea una listas de QgsField
                        fieldsLayer=capa.fields().toList()
                        #se itera la lista QgsFields
                        fields=[f.name() for f in fieldsLayer]
                        self.dockwidget.comboBoxCAMPOZ.clear()
                        self.dockwidget.comboBoxCAMPOZ.addItem('Seleccionar')
                        for field in capa.fields():
                            id=fields.index(field.name())
                            alia=capa.attributeAlias(id)
                            if len(alia)>0:
                                if field.type()==6 or field.type()==2:
                                    self.dockwidget.comboBoxCAMPOZ.addItem(alia,field)
                                else:
                                    pass
                            else:
                                if field.type()==6 or field.type()==2:
                                    self.dockwidget.comboBoxCAMPOZ.addItem(field.name(),field)
                                else:
                                    pass
                    except:
                        pass
                    #Licences
                    self.dockwidget.comboBoxLICENCIAS.clear()
                    self.dockwidget.comboBoxLICENCIAS.addItem('Seleccionar')
                    for s in licencesList:
                        self.dockwidget.comboBoxLICENCIAS.addItem(s)
                    #Rol
                    self.dockwidget.comboBoxROL.clear()
                    self.dockwidget.comboBoxROL.addItem('Seleccionar')
                    for s in rolList:
                        self.dockwidget.comboBoxROL.addItem(s)
                    #Address type
                    self.dockwidget.comboBoxTIPODIRECCION.clear()
                    self.dockwidget.comboBoxTIPODIRECCION.addItem('...')
                    for s in postalcodList:
                        self.dockwidget.comboBoxTIPODIRECCION.addItem(s)
                    #Link type
                    self.dockwidget.comboBoxTIPOENL.clear()
                    self.dockwidget.comboBoxTIPOENL.addItem('...')
                    for s in linktypeList:
                        self.dockwidget.comboBoxTIPOENL.addItem(s)
                        
                    self.clearI()
                    self.clearE()
                    self.clearA()
                    self.clearC()
                    self.clearL()
                    self.clearH()
                    self.clearR()
                else:
                    pass
            else:
                pass
        except:
            pass
    
    
    def clearI(self):
        #Limpiar los lineEdit 
        self.dockwidget.lineEditIDENTIFICADOR.clear()
        self.dockwidget.lineEditIDENTIFICADOR_ORIGEN.clear()
        self.dockwidget.lineEditTITULO.clear()
        self.dockwidget.lineEditTIPO.clear()
        self.dockwidget.comboBoxIDIOMAID.setCurrentText('...')
        self.dockwidget.comboBoxIDIOMAPAIS.setCurrentText('...')
        self.dockwidget.lineEditRESUMEN.clear()
        self.dockwidget.comboBoxCATEGORIA.setCurrentText('Seleccionar')
        self.dockwidget.lineEditCATEGORIA.clear()
        self.dockwidget.lineEditCONCEPTOPC.clear()
        self.dockwidget.lineEditITEMSPC.clear()
        self.dockwidget.lineEditPALABRASCLAVES.clear()
    
    def clearE(self):
        self.dockwidget.lineEditCRS.setText('EPSG:')
        self.dockwidget.lineEditXMIN.clear()
        self.dockwidget.lineEditYMIN.clear()
        self.dockwidget.lineEditXMAX.clear()
        self.dockwidget.lineEditYMAX.clear()
        self.dockwidget.comboBoxCAMPOZ.setCurrentText('Seleccionar')
        self.dockwidget.doubleSpinBoxZMAX.setValue(99999.99)
        self.dockwidget.doubleSpinBoxZMIN.setValue(99999.99)
        date_time_str='01/01/23 12:00:00'
        date_time_object = datetime.strptime(date_time_str, "%d/%m/%y %H:%M:%S")
        self.dockwidget.dateTimeEditINICIO.setDateTime(date_time_object)
        self.dockwidget.dateTimeEditFINAL.setDateTime(date_time_object)
        
    def clearA(self):
        self.dockwidget.lineEditCUOTAS.clear()
        self.dockwidget.comboBoxLICENCIAS.setCurrentText('Seleccionar')
        self.dockwidget.lineEditLICENCIAS.clear()
        self.dockwidget.lineEditDERECHOS.clear()
        self.dockwidget.lineEditACCESO.clear()
        self.dockwidget.lineEditUSO.clear()
        self.dockwidget.lineEditOTRO.clear()
        
    def clearC(self):
        self.dockwidget.lineEditNOMBRE.clear()
        self.dockwidget.lineEditROL.clear()
        self.dockwidget.lineEditORGANIZACION.clear()
        self.dockwidget.lineEditPOSICION.clear()
        self.dockwidget.lineEditEMAIL.clear()
        self.dockwidget.lineEditTELEFONO.clear()
        self.dockwidget.lineEditOTRONUMERO.clear()
        self.dockwidget.comboBoxTIPODIRECCION.setCurrentText('...')
        self.dockwidget.lineEditCODIGOPOSTAL.clear()
        self.dockwidget.lineEditDIRECCION.clear()
        self.dockwidget.lineEditPAIS.clear()
        self.dockwidget.lineEditAREAADMIN.clear()
        self.dockwidget.lineEditCIUDAD.clear()
        
    def clearL(self):
        self.dockwidget.lineEditNOMBREENL.clear()
        self.dockwidget.comboBoxTIPOENL.setCurrentText('...')
        self.dockwidget.lineEditURL.clear()
        self.dockwidget.lineEditDESCRIP.clear()
        self.dockwidget.lineEditFORMATO.clear()
        self.dockwidget.lineEditMIME.clear()
        self.dockwidget.lineEditTAMANOENL.clear()
        
    def clearH(self):
        self.dockwidget.textEditHISTORIA.clear()
        self.dateHistory()
        
    def clearR(self):
        self.dockwidget.comboBoxACCION.setCurrentText('Seleccionar')
        self.dockwidget.textBrowserRESUMEN.clear()
            
    
    def addCat(self):
        cat_add=self.dockwidget.comboBoxCATEGORIA.currentText()
        cat_data=self.dockwidget.lineEditCATEGORIA.text()
        listcat = cat_data. split (",")
        if cat_add!='Seleccionar' and cat_add not in listcat:
            if len(cat_data)==0:
                catlist=cat_add
            else:
                catlist=cat_data+','+cat_add
            self.dockwidget.lineEditCATEGORIA.setText(catlist)
            self.dockwidget.comboBoxCATEGORIA.setCurrentText('Seleccionar')
        else:
            self.dockwidget.comboBoxCATEGORIA.setCurrentText('Seleccionar')
        
    def readAbstract(self):
        abstract=self.dockwidget.lineEditRESUMEN.text()
        #ventana emergente para seguir en la ventana o salir
        data = QImage(os.path.dirname(__file__) + "/icono.png")
        pixmap = QPixmap(data).scaledToHeight(54, Qt.SmoothTransformation)
        msg = QMessageBox()
        msg.setWindowTitle("Resumen")
        msg.setIconPixmap(pixmap)
        msg.setText('<b>Esto es lo que ha escrito...</b>')
        msg.setInformativeText(f'<i>{abstract}</i>')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
        
    def readvariable(self):
        # Obtener la capa seleccionada en QGIS
        try:
            capa = self.dockwidget.comboBoxCAPASEL.currentData()
            #identificar las variables globales
            Scope_s=QgsExpressionContextUtils.globalScope()
            if self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==0:
                try:
                    fuenteC=capa.source()
                    self.dockwidget.lineEditIDENTIFICADOR.setText(fuenteC)
                except:
                    pass
                try:
                    Varia_idioma=Scope_s.variable('user_language(lan)')
                    self.dockwidget.comboBoxIDIOMAID.setCurrentText(Varia_idioma)
                except:
                    pass
                try:
                    Varia_country2L=Scope_s.variable('user_country(COU)')
                    self.dockwidget.comboBoxIDIOMAPAIS.setCurrentText(Varia_country2L)
                except:
                    pass
            elif self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==1:
                try:
                    CRS=capa.crs().authid()
                    self.dockwidget.lineEditCRS.setText(CRS)
                except:
                    pass
            elif self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==3:
                try:
                    Varia_name=Scope_s.variable('contact_name')
                    self.dockwidget.lineEditNOMBRE.setText(Varia_name)
                except:
                    pass
                try:
                    Varia_rol=Scope_s.variable('contact_rol')
                    self.dockwidget.lineEditROL.setText(Varia_rol)
                except:
                    pass
                try:
                    Varia_org=Scope_s.variable('contact_organitation')
                    self.dockwidget.lineEditORGANIZACION.setText(Varia_org)
                except:
                    pass
                try:
                    Varia_pos=Scope_s.variable('contact_position')
                    self.dockwidget.lineEditPOSICION.setText(Varia_pos)
                except:
                    pass
                try:
                    Varia_email=Scope_s.variable('contact_email')
                    self.dockwidget.lineEditEMAIL.setText(Varia_email)
                except:
                    pass
                try:
                    Varia_pho1=Scope_s.variable('contact_phone1')
                    self.dockwidget.lineEditTELEFONO.setText(Varia_pho1)
                except:
                    pass
                try:
                    Varia_pho2=Scope_s.variable('contact_phone2')
                    self.dockwidget.lineEditOTRONUMERO.setText(Varia_pho2)
                except:
                    pass
                try:
                    Varia_typeA=Scope_s.variable('address_type')
                    Varia_typeA=Varia_typeA.title()
                    self.dockwidget.comboBoxTIPODIRECCION.setCurrentText(Varia_typeA)
                except:
                    pass
                try:
                    Varia_copo=Scope_s.variable('address_postalCode')
                    self.dockwidget.lineEditCODIGOPOSTAL.setText(Varia_copo)
                except:
                    pass
                try:
                    Varia_addr=Scope_s.variable('address_address')
                    self.dockwidget.lineEditDIRECCION.setText(Varia_addr)
                except:
                    pass
                try:
                    Varia_city=Scope_s.variable('address_city')
                    self.dockwidget.lineEditCIUDAD.setText(Varia_city)
                except:
                    pass
                try:
                    Varia_admA=Scope_s.variable('address_administrativeArea')
                    self.dockwidget.lineEditAREAADMIN.setText(Varia_admA)
                except:
                    pass
                try:
                    Varia_pais=Scope_s.variable('address_country')
                    self.dockwidget.lineEditPAIS.setText(Varia_pais)
                except:
                    pass
            else:
                pass
        except:
            pass
                
    def leermeta2(self,capa):
        try:
            # Obtener la capa actualmente seleccionada en QGIS
            nameC=capa.name()
            if self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==0:
                #se lee los datos
                if capa is not None:
                    try:
                        ident=capa.metadata().identifier()
                        self.dockwidget.lineEditIDENTIFICADOR.setText(ident)
                    except:
                        pass
                    try:
                        iden_origen=capa.metadata().parentIdentifier()
                        self.dockwidget.lineEditIDENTIFICADOR_ORIGEN.setText(iden_origen)
                    except:
                        pass
                    try:
                        titulo=capa.metadata().title()
                        self.dockwidget.lineEditTITULO.setText(titulo)
                    except:
                        pass
                    try:
                        tipo_D=capa.metadata().type()
                        self.dockwidget.lineEditTIPO.setText(titulo)
                    except:
                        pass
                    try:
                        idioma=capa.metadata().language()
                        idiomalist=idioma. split ("-")
                        self.dockwidget.comboBoxIDIOMAID.setCurrentText(idiomalist[0])
                        self.dockwidget.comboBoxIDIOMAPAIS.setCurrentText(idiomalist[1])
                    except:
                        pass
                    try:
                        Resumen=capa.metadata().abstract()
                        self.dockwidget.lineEditRESUMEN.setText(Resumen)
                    except:
                        pass
                    try:
                        Categoria=capa.metadata().categories()
                        n=0
                        for c in range (len(Categoria)):
                            if n==0:
                                textCat = Categoria[c]
                            else:
                                textCat = textCat +',' + Categoria[c]
                            n=n+1
                        self.dockwidget.lineEditCATEGORIA.setText(textCat)
                    except:
                        pass
                    try:
                        Keywords=capa.metadata().keywords()
                        n=0
                        for name in Keywords.keys():
                            if name=='gmd:topicCategory':
                                pass
                            else:
                                if n==0:
                                    textCat =f'{name}:{Keywords[name]}'
                                else:
                                    textCat = textCat +';' + f'{name}:{Keywords[name]}'
                            n=n+1
                        self.dockwidget.lineEditPALABRASCLAVES.setText(textCat)
                    except:
                        pass
                    
            elif self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==1:
                try:
                    CRS=capa.crs().authid()
                    if len(CRS)>0:
                        self.dockwidget.lineEditCRS.setText(CRS)
                    else:
                        self.dockwidget.lineEditCRS.setText('EPSG:')
                except:
                    pass
                try:
                    Xmin=capa.metadata().extent().spatialExtents()[0].bounds.xMinimum()
                    self.dockwidget.lineEditXMIN.setText(str(Xmin))
                except:
                    pass
                try:
                    Ymin=capa.metadata().extent().spatialExtents()[0].bounds.yMinimum()
                    self.dockwidget.lineEditYMIN.setText(str(Ymin))
                except:
                    pass
                try:
                    Xmax=capa.metadata().extent().spatialExtents()[0].bounds.xMaximum()
                    self.dockwidget.lineEditXMAX.setText(str(Xmax))
                except:
                    pass
                try:
                    Ymax=capa.metadata().extent().spatialExtents()[0].bounds.yMaximum()
                    self.dockwidget.lineEditYMAX.setText(str(Ymax))
                except:
                    pass
                try:
                    Zmax=capa.metadata().extent().spatialExtents()[0].bounds.zMaximum()
                    self.dockwidget.doubleSpinBoxZMAX.setValue(Zmax)
                except:
                    pass
                try:
                    Zmin=capa.metadata().extent().spatialExtents()[0].bounds.zMinimum()
                    self.dockwidget.doubleSpinBoxZMIN.setValue(Zmin)
                except:
                    pass
                try:
                    start=capa.metadata().extent().temporalExtents()[0].begin()
                    self.dockwidget.dateTimeEditINICIO.setDateTime (start)
                except:
                    pass
                try:
                    end=capa.metadata().extent().temporalExtents()[0].end()
                    self.dockwidget.dateTimeEditFINAL.setDateTime (end)
                except:
                    pass
            elif self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==2:
                #se lee los datos
                if capa is not None:
                    try:
                        Cuota=capa.metadata().fees()
                        self.dockwidget.lineEditCUOTAS.setText(Cuota)
                    except:
                        pass
                    try:
                        Licencias=capa.metadata().licenses()
                        n=0
                        for c in range (len(Licencias)):
                            if n==0:
                                textLic = Licencias[c]
                            else:
                                textLic = f'{textLic},{Licencias[c]}'
                            n=n+1
                        self.dockwidget.lineEditLICENCIAS.setText(textLic)
                    except:
                        pass
                    try:
                        Derechos=capa.metadata().rights()
                        n=0
                        for c in range (len(Derechos)):
                            if n==0:
                                textDer = Derechos[c]
                            else:
                                textDer = f'{textDer},{Derechos[c]}'
                            n=n+1
                        self.dockwidget.lineEditDERECHOS.setText(textDer)
                    except:
                        pass
                    try:
                        ResNum=len(capa.metadata().constraints())
                        for r in range(ResNum):
                            tipoR=capa.metadata().constraints()[r].type
                            tipoR=tipoR.title()
                            Restriccion=capa.metadata().constraints()[r].constraint
                            if tipoR=='Access':
                                self.dockwidget.lineEditACCESO.setText(Restriccion)
                            elif tipoR=='Use':
                                self.dockwidget.lineEditUSO.setText(Restriccion)
                            elif tipoR=='Other':
                                self.dockwidget.lineEditOTRO.setText(Restriccion)
                            else:
                                pass
                    except:
                        pass
                else:
                    pass
            elif self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==3:
                if capa is not None:
                    ContactsNum=len(capa.metadata().contacts())
                    if ContactsNum>1:
                        ContactsList=[f'{capa.metadata().contacts()[c].name}' for c in range(ContactsNum)]
                        contact, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona un contacto","Contacto:",ContactsList,0,False)
                        idc=ContactsList.index(contact)
                    else:
                        idc=0
                    try:
                        Nombre=capa.metadata().contacts()[idc].name
                        self.dockwidget.lineEditNOMBRE.setText(Nombre)
                    except:
                        pass
                    try:
                        Rol=capa.metadata().contacts()[idc]. role
                        self.dockwidget.lineEditROL.setText(Rol)
                    except:
                        pass
                    try:
                        Organización=capa.metadata().contacts()[idc].organization
                        self.dockwidget.lineEditORGANIZACION.setText(Organización)
                    except:
                        pass
                    try:
                        Posicion=capa.metadata().contacts()[idc].position
                        self.dockwidget.lineEditPOSICION.setText(Posicion)
                    except:
                        pass
                    try:
                        Email=capa.metadata().contacts()[idc].email
                        self.dockwidget.lineEditEMAIL.setText(Email)
                    except:
                        pass
                    try:
                        Phone1=capa.metadata().contacts()[idc].voice
                        self.dockwidget.lineEditTELEFONO.setText(Phone1)
                    except:
                        pass
                    try:
                        Phone2=capa.metadata().contacts()[idc].fax
                        self.dockwidget.lineEditOTRONUMERO.setText(Phone2)
                    except:
                        pass
                    try:
                        AdressesNum=len(capa.metadata().contacts()[idc].addresses)
                        if AdressesNum>1:
                            AdressesList=[f'Dirección {f+1}' for f in range(AdressesNum)]
                            addresses, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona una dirección","Dirección:",AdressesList,0,False)
                            id=AdressesList.index(addresses)
                        else:
                            id=0
                        try:
                            TipoD=capa.metadata().contacts()[idc].addresses[id].type
                            TipoD=TipoD.title()
                            self.dockwidget.comboBoxTIPODIRECCION.setCurrentText(TipoD)
                        except:
                            pass
                        try:
                            CodPos=capa.metadata().contacts()[idc].addresses[id].postalCode
                            self.dockwidget.lineEditCODIGOPOSTAL.setText(CodPos)
                        except:
                            pass
                        try:
                            Dirección=capa.metadata().contacts()[idc].addresses[id].address
                            self.dockwidget.lineEditDIRECCION.setText(Dirección)
                        except:
                            pass
                        try:
                            Pais=capa.metadata().contacts()[idc].addresses[id].country
                            self.dockwidget.lineEditPAIS.setText(Pais)
                        except:
                            pass
                        try:
                            Areadmin=capa.metadata().contacts()[idc].addresses[id].administrativeArea
                            self.dockwidget.lineEditAREAADMIN.setText(Areadmin)
                        except:
                            pass
                        try:
                            Ciudad=capa.metadata().contacts()[idc].addresses[id].city
                            self.dockwidget.lineEditCIUDAD.setText(Ciudad)
                        except:
                            pass
                    except:
                        pass
                else:
                    pass
            elif self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==4:
                try:
                    LinkNum=len(capa.metadata().links())
                    if LinkNum>1:
                        LinkList=[f'{capa.metadata().links()[l].name}' for l in range(LinkNum)]
                        Links, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona un Link","Link:",LinkList,0,False)
                        id=LinkList.index(Links)
                    else:
                        id=0
                    if capa is not None:
                        try:
                            NombreE=capa.metadata().links()[id].name
                            self.dockwidget.lineEditNOMBREENL.setText(NombreE)
                        except:
                            pass
                        try:
                            TipoE=capa.metadata().links()[id].type
                            self.dockwidget.comboBoxTIPOENL.setCurrentText(TipoE)
                        except:
                            pass
                        try:
                            URL=capa.metadata().links()[id].url
                            self.dockwidget.lineEditURL.setText(URL)
                        except:
                            pass
                        try:
                            DescripcionE=capa.metadata().links()[id].description
                            self.dockwidget.lineEditDESCRIP.setText(DescripcionE)
                        except:
                            pass
                        try:
                            Formato=capa.metadata().links()[id].format
                            self.dockwidget.lineEditFORMATO.setText(Formato)
                        except:
                            pass
                        try:
                            MIME=capa.metadata().links()[id].mimeType
                            self.dockwidget.lineEditMIME.setText(MIME)
                        except:
                            pass
                        try:
                            Tamano=capa.metadata().links()[id].size
                            self.dockwidget.lineEditTAMANOENL.setText(Tamano)
                        except:
                            pass
                    else:
                        pass
                except:
                    pass
            elif self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==5:
                self.dockwidget.textEditHISTORIA.clear()
                try:
                    #se lee los datos
                    if capa is not None:
                        Hist=capa.metadata().history()
                    else:
                        pass
                    for s in range (len(Hist)):
                        if Hist[s]==Hist[-1]:
                            d=f'{Hist[s]}'
                        else:
                            d=f'{Hist[s]},'
                        self.dockwidget.textEditHISTORIA.append(d)
                except:
                    pass
            else:
                pass
        except:
            pass
    
    def leermetaSeleccionada(self):
        if self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()!=6:
            # Obtener la capa actualmente seleccionada en QGIS
            capa = self.dockwidget.comboBoxCAPASEL.currentData()
            self.leermeta2(capa)
        else:
            pass
        
    def leermetaOtra(self):
        if self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()!=6:
            layers =QgsProject.instance().mapLayers().values()
            layerData=[l for l in layers]
            layerList=[l.name() for l in layers]
            layern, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona una capa","Capa:",layerList,0,False)
            idd=layerList.index(layern)
            capa=layerData[idd]
            self.leermeta2(capa)
        else:
            pass
    
    def clear2(self):
        #Limpiar los lineEdit 
        if self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==0:
            self.clearI()
        elif self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==1:
            self.clearE()
        elif self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==2:
            self.clearA()
        elif self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==3:
            self.clearC()
        elif self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==4:
            self.clearL()
        elif self.dockwidget.toolBoxESCRIBIRMETA.currentIndex()==5:
            self.clearH()
        else:
            self.clearR()
            
    def addkeywords(self):
        concepKeywords=self.dockwidget.lineEditCONCEPTOPC.text()
        itmesKeywords=self.dockwidget.lineEditITEMSPC.text()
        if len(concepKeywords)>0 and len(itmesKeywords)>0:
            listitem = itmesKeywords. split (",")
            listitemS=[]
            for i in listitem:
                i=f'{i}'
                listitemS.append(i)
            Keywords=self.dockwidget.lineEditPALABRASCLAVES.text()
            keyword=(f"'{concepKeywords}':{listitemS}")
            if len(Keywords)==0:
                keylist=keyword
            else:
                keylist=Keywords+';'+keyword
            self.dockwidget.lineEditPALABRASCLAVES.setText(keylist)
            concepKeywords=self.dockwidget.lineEditCONCEPTOPC.clear()
            itmesKeywords=self.dockwidget.lineEditITEMSPC.clear()
        else:
            QMessageBox.warning(None, 'QMetadaLayer', '<b>ATENCIÓN</b> Complete los parámetros, Ej. <u>Concepto</u>:<u>[Palabras, Clave]</u>.')
    
    def XYlayer(self):
        self.dockwidget.lineEditXMIN.clear()
        self.dockwidget.lineEditYMIN.clear()
        self.dockwidget.lineEditXMAX.clear()
        self.dockwidget.lineEditYMAX.clear()
        try:
            capa=self.dockwidget.comboBoxCAPAEXT.currentData()
            ext=capa.extent()
            xmin = ext.xMinimum()
            self.dockwidget.lineEditXMIN.setText(f'{xmin}')
            xmax = ext.xMaximum()
            self.dockwidget.lineEditXMAX.setText(f'{xmax}')
            ymin = ext.yMinimum()
            self.dockwidget.lineEditYMIN.setText(f'{ymin}')
            ymax = ext.yMaximum()
            self.dockwidget.lineEditYMAX.setText(f'{ymax}')
        except:
            pass
    def Zmaxmin(self):
        self.dockwidget.doubleSpinBoxZMAX.setValue(99999.99)
        self.dockwidget.doubleSpinBoxZMIN.setValue(99999.99)
        try:
            field=self.dockwidget.comboBoxCAMPOZ.currentText()
            maximo=max([f[f"{field}"] for f in iface.activeLayer().getFeatures()])
            self.dockwidget.doubleSpinBoxZMAX.setValue(float(maximo))
            minimo=min([f[f"{field}"] for f in iface.activeLayer().getFeatures()])
            self.dockwidget.doubleSpinBoxZMIN.setValue(float(minimo))
        except:
            pass
            
    def addLicences(self):
        licences=self.dockwidget.comboBoxLICENCIAS.currentText()
        lic_data=self.dockwidget.lineEditLICENCIAS.text()
        listlic = lic_data. split (",")
        if licences!='Seleccionar' and licences not in listlic:
            if len(lic_data)==0:
                liclist=licences
            else:
                liclist=lic_data+','+licences
            self.dockwidget.lineEditLICENCIAS.setText(liclist)
            self.dockwidget.comboBoxLICENCIAS.setCurrentText('Seleccionar')
        else:
            pass
        
    def addRol(self):
        rol=self.dockwidget.comboBoxROL.currentText()
        if rol!= 'Seleccionar':
            self.dockwidget.lineEditROL.setText(rol)
            self.dockwidget.comboBoxROL.setCurrentText('Seleccionar')
            
        else:
            pass
    
    def datosIdentifier(self, Identifier, ParentIdentifier, Title, Type, LanguageId, LanguageCt, Abstract, Categorieslist, Keywordslist, accion):
        p=0
        list=[Identifier, ParentIdentifier, Title, Type, LanguageId, LanguageCt, Abstract, Categorieslist, Keywordslist]
        dicI={0:'Identificador', 1:'Identificador Origen', 2:'Título', 3:'Tipo de Datos', 4:'Idioma', 6:'Resumen', 7:'Categoría ISO', 8:'Palabras Clave'}
        idi=0
        for v in list:
            print(v)
            if len(f'{v}')>0:
                if v==LanguageId:
                    try:
                        if LanguageId!='...' and LanguageCt!='...':
                            p=p+1
                            Language=f'{LanguageId}-{LanguageCt}'
                            self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicI[idi]}:</b><i> {Language}</i>')
                        else:
                            pass
                    except:
                        pass
                elif v==LanguageCt:
                    pass
                elif v==Categorieslist:
                    try:
                        p=p+1
                        Categories = Categorieslist. split (",")
                        self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicI[idi]}:</b><i> {Categories}</i>')
                    except:
                        pass
                elif v==Keywordslist:
                    try:
                        p=p+1
                        Keywordslist1 = Keywordslist. split (";")
                        dic={}
                        for k in Keywordslist1:
                            k1 = k. split (":")
                            #clave
                            kk=k1[0]
                            kk=kk.replace("'","")
                            #Valor
                            v=k1[1]
                            v=v.replace('[','')
                            v=v.replace(']','')
                            v=v.replace("'","")
                            v1 = v. split (",")
                            dic[kk]=v1
                        #se agrega la cateoria al dic de keywords
                        if len(Categorieslist)>0:
                            dic['gmd:topicCategory']=Categories
                        else:
                            dic['gmd:topicCategory']=[]
                        self.dockwidget.textBrowserRESUMEN.append(f'<b>Palabras Clave:</b><i>{dic}</i>')
                    except:
                        pass
                else:
                    try:
                        p=p+1
                        self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicI[idi]}:</b> <i> {v}</i>')
                    except:
                        pass
            else:
                if v==LanguageCt:
                    pass
                else:
                    if accion=='Agregar Metadatos':
                        self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicI[idi]}:</b>')
                    else:
                        pass
            idi=idi+1
        return p
    
    def datosExtent (self, CRS, Xmin, Ymin, Xmax, Ymax, Zmax, Zmin, accion):
        p=0
        list=[CRS, Xmin, Ymin, Xmax, Ymax, Zmax, Zmin]
        dicE={0:'CRS', 1:'X Minímo', 2:'Y Minímo', 3:'X Máxima', 4:'Y Máxima', 5:'Z Máxima', 6:'Z Minímo'}
        ide=0
        for e in list:
            if len(f'{e}')>0:
                if e==CRS:
                    if CRS!='EPSG:':
                        p=p+1
                        self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicE[ide]}:</b><i> {e}</i>')
                    else:
                        if accion=='Agregar Metadatos':
                            self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicE[ide]}:</b>')
                        else:
                            pass
                elif e==Zmax or e==Zmin:
                    if e!=99999.99:
                        p=p+1
                        self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicE[ide]}:</b><i> {e}</i>')
                    else:
                        if accion=='Agregar Metadatos':
                            self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicE[ide]}:</b>')
                        else:
                            pass
                else:
                    p=p+1
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicE[ide]}:</b><i> {e}</i>')
            else:
                if accion=='Agregar Metadatos':
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicE[ide]}:</b>')
                else:
                    pass
            ide=ide+1
        return p
    
    def datosExtentTemporal(self, Inicio, Fin, accion):
        p=0
        list=[Inicio, Fin]
        dicE={0:'Inicio', 1:'Final'}
        ide=0
        for e in list:
            if len(f'{e}')>0:
                if e!='dom ene 1 12:00:00 2023':
                    p=p+1
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicE[ide]}:</b><i> {e}</i>')
                else:
                    if accion=='Agregar Metadatos':
                        self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicE[ide]}:</b>')
                    else:
                        pass
            else:
                if accion=='Agregar Metadatos':
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicE[ide]}:</b>')
                else:
                    pass
            ide=ide+1
        return p
    
    def datosAccess(self, Cuota, Licencias, Derechos, accion):
        p=0
        list=[Cuota, Licencias, Derechos]
        dicA={0:'Cuotas', 1:'Licencias', 2:'Derechos'}
        ida=0
        for a in list:
            if len(f'{a}')>0:
                if a==Licencias or a==Derechos:
                    al=a. split (",")
                    p=p+1
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicA[ida]}:</b><i> {al}</i>')
                else:
                    p=p+1
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicA[ida]}:</b><i> {a}</i>')
            else:
                if accion=='Agregar Metadatos':
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicA[ida]}:</b>')
                else:
                    pass
            ida=ida+1
        return p
    
    def datosConstraint(self, ResAces, ResUso, ResOtro, accion):
        p=0
        list=[ResAces, ResUso, ResOtro]
        dicC={ 0:'Restricción Acceso', 1:'Restricción Uso', 2:'Restricción Otro'}
        idr=0
        for r in list:
            if len(f'{r}')>0:
                p=p+1
                self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicC[idr]}:</b><i> {r}</i>')
            else:
                if accion=='Modificar Metadatos':
                    pass
                else:
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicC[idr]}:</b>')
            if accion=='Agregar Metadatos' or accion=='Modificar Metadatos':
                pass
            else:
                if len(ResAces)>0 or len(ResUso)>0 or len(ResOtro)>0:
                    p=1
                else:
                    p=0
            idr=idr+1
        return p
        
    def datosContact(self, NombreC, RolC, OrganizacionC, PosicionC, EmailC, Telefono1C, Telefono2C, accion):
        p=0
        list=[NombreC, RolC, OrganizacionC, PosicionC, EmailC, Telefono1C, Telefono2C]
        dicCC={0:'Nombre', 1:'Rol', 2:'Organización', 3:'Posición', 4:'Correo Electrónico', 5:'Número telefónico', 6:'Otro número'}
        idcc=0
        for cc in list:
            if len(f'{cc}')>0:
                p=p+1
                self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicCC[idcc]}:</b><i> {cc}</i>')
            else:
                if accion=='Modificar Metadatos':
                    pass
                else:
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicCC[idcc]}:</b>')
            idcc=idcc+1
        return p
        
    def datosAddress(self, PostaltipoC, CodigopostalC, DireccionC, PaisC, Areadmin, CiudadC, accion):
        p=0
        list=[PostaltipoC, CodigopostalC, DireccionC, PaisC, Areadmin, CiudadC]
        dicCA={0:'Tipo CP', 1:'Código Postal', 2:'Dirección', 3:'País', 4:'Area administrativa', 5:'Ciudad'}
        idca=0
        for ca in list:
            if len(f'{ca}')>0:
                if ca==PostaltipoC:
                    if ca!='...':
                        p=p+1
                        self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicCA[idca]}</b><i> {ca}</i>')
                    else:
                        if accion=='Modificar Metadatos':
                            pass
                        else:
                            self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicCA[idca]}:</b>')
                else:
                    p=p+1
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicCA[idca]}</b><i> {ca}</i>')
            else:
                if accion=='Modificar Metadatos':
                    pass
                else:
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicCA[idca]}:</b>')
            idca=idca+1
        return p
    
    def datosLink(self, NombreL, LinktipoL, UrlL, DescripcionL, FormatoL, mimeL, TamanoL, accion):
        p=0
        list=[ NombreL, LinktipoL, UrlL, DescripcionL, FormatoL, mimeL, TamanoL]
        dicL={0:'Nombre', 1:'Tipo', 2:'URL', 3:'Descripción', 4:'Formato', 5:'MIME', 6:'Tamaño'}
        idl=0
        for l in list:
            if len(f'{l}')>0:
                if l==LinktipoL:
                    if l!='...':
                        p=p+1
                        self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicL[idl]}:</b><i> {l}</i>')
                    else:
                        if accion=='Modificar Metadatos':
                            pass
                        else:
                            self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicL[idl]}:</b>')
                else:
                    p=p+1
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicL[idl]}:</b><i> {l}</i>')
            else:
                if accion=='Modificar Metadatos':
                    pass
                else:
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>{dicL[idl]}:</b>')
            idl=idl+1
        return p
        
    def datosMessage(self, accion):
        if self.dockwidget.radioButtonANCLARCAPA.isChecked()==False:
            if accion=='Agregar Metadatos' or accion=='Adicionar Palabras Clave' or accion=='Adicionar Restriciones' or accion=='Adicionar un Contacto' or accion=='Adicionar una Dirección' or accion=='Adicionar un Link' or accion=='Adicionar Historias' or accion=='Modificar Metadatos':
                self.dockwidget.textBrowserRESUMEN.append('+++++++++++++++++++++++++++++++++++++++++++')
                self.dockwidget.textBrowserRESUMEN.append('ATENCIÓN. La capa no está fija, por favor revise que los metadatos sean correctos.')
                self.dockwidget.textBrowserRESUMEN.append('+++++++++++++++++++++++++++++++++++++++++++')
            else:
                self.dockwidget.textBrowserRESUMEN.append('+++++++++++++++++++++++++++++++++++++++++++')
                self.dockwidget.textBrowserRESUMEN.append('ATENCIÓN. La capa no está fija, por favor asegúrese que la capa seleccionada sea la correcta.')
                self.dockwidget.textBrowserRESUMEN.append('+++++++++++++++++++++++++++++++++++++++++++')
        else:
            pass
    
    def datosProgress(self, p, capa, accion):
        nameLayer=capa.name()
        if accion=='Agregar Metadatos' or accion=='Adicionar Palabras Clave' or accion=='Adicionar Restriciones' or accion=='Adicionar un Contacto' or accion=='Adicionar una Dirección' or accion=='Adicionar un Link' or accion=='Adicionar Historias':
            self.dockwidget.textBrowserRESUMEN.append('- Porcentaje de Metadatos definidos para esta operación:')
            if accion=='Agregar Metadatos':
                Valor=p/44
            elif accion=='Adicionar Palabras Clave'or accion=='Adicionar Restriciones' or accion=='Adicionar Historias':
                Valor=p/1
                p=p*44
            elif accion=='Adicionar un Contacto':
                Valor=p/13
                p=int(p*3.4)
            elif accion=='Adicionar una Dirección':
                Valor=p/6
                p=p*7
            elif accion=='Adicionar un Link':
                Valor=p/7
                p=p*6
            text='|'* p + "{0:.0%}".format(Valor)
            if p==0:
                self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(True)
            else:
                pass
            self.dockwidget.textBrowserRESUMEN.append(text)
            if accion=='Agregar Metadatos':
                self.dockwidget.textBrowserRESUMEN.append(f'- Se agregarán a la capa: <b>{nameLayer}</b>')
            else:
                self.dockwidget.textBrowserRESUMEN.append(f'- Se adicionarán a la capa: <b>{nameLayer}</b>')
        elif accion=='Modificar Metadatos':
            self.dockwidget.textBrowserRESUMEN.append('- El número de Metadatos a modificar en esta operación son:')
            self.dockwidget.textBrowserRESUMEN.append(f' {p}')
            if p==0:
                self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(True)
            else:
                pass
            self.dockwidget.textBrowserRESUMEN.append(f'- En la capa: <b>{nameLayer}</b>')
        else:
            self.dockwidget.textBrowserRESUMEN.append(f'- Se removerá de la capa: <b>{nameLayer}</b>')
        self.datosMessage(accion)
    
    
    def resumenMetadato(self):
        try:
            accion=self.dockwidget.comboBoxACCION.currentText()
            # Obtener la capa actualmente seleccionada en QGIS
            capa = self.dockwidget.comboBoxCAPASEL.currentData()
            nameLayer=capa.name()
            self.dockwidget.textBrowserRESUMEN.setStyleSheet("color: blue")
            Identifier=self.dockwidget.lineEditIDENTIFICADOR.text()
            ParentIdentifier=self.dockwidget.lineEditIDENTIFICADOR_ORIGEN.text()
            Title=self.dockwidget.lineEditTITULO.text()
            Type=self.dockwidget.lineEditTIPO.text()
            LanguageId=self.dockwidget.comboBoxIDIOMAID.currentText()
            LanguageCt=self.dockwidget.comboBoxIDIOMAPAIS.currentText()
            Abstract=self.dockwidget.lineEditRESUMEN.text()
            Categorieslist=self.dockwidget.lineEditCATEGORIA.text()
            Keywordslist=self.dockwidget.lineEditPALABRASCLAVES.text()
            CRS=self.dockwidget.lineEditCRS.text()
            Xmin=self.dockwidget.lineEditXMIN.text()
            Ymin=self.dockwidget.lineEditYMIN.text()
            Xmax=self.dockwidget.lineEditXMAX.text()
            Ymax=self.dockwidget.lineEditYMAX.text()
            Zmax=self.dockwidget.doubleSpinBoxZMAX.value()
            Zmin=self.dockwidget.doubleSpinBoxZMIN.value()
            Inicio=self.dockwidget.dateTimeEditINICIO.dateTime ().toString()
            Fin=self.dockwidget.dateTimeEditFINAL.dateTime ().toString()
            Cuota=self.dockwidget.lineEditCUOTAS.text()
            Licencias=self.dockwidget.lineEditLICENCIAS.text()
            Derechos=self.dockwidget.lineEditDERECHOS.text()
            ResAces=self.dockwidget.lineEditACCESO.text()
            ResUso=self.dockwidget.lineEditUSO.text()
            ResOtro=self.dockwidget.lineEditOTRO.text()
            NombreC=self.dockwidget.lineEditNOMBRE.text()
            RolC=self.dockwidget.lineEditROL.text()
            OrganizacionC=self.dockwidget.lineEditORGANIZACION.text()
            PosicionC=self.dockwidget.lineEditPOSICION.text()
            EmailC=self.dockwidget.lineEditEMAIL.text()
            Telefono1C=self.dockwidget.lineEditTELEFONO.text()
            Telefono2C=self.dockwidget.lineEditOTRONUMERO.text()
            PostaltipoC=self.dockwidget.comboBoxTIPODIRECCION.currentText()
            CodigopostalC=self.dockwidget.lineEditCODIGOPOSTAL.text()
            DireccionC=self.dockwidget.lineEditDIRECCION.text()
            PaisC=self.dockwidget.lineEditPAIS.text()
            Areadmin=self.dockwidget.lineEditAREAADMIN.text()
            CiudadC=self.dockwidget.lineEditCIUDAD.text()
            NombreL=self.dockwidget.lineEditNOMBREENL.text()
            LinktipoL=self.dockwidget.comboBoxTIPOENL.currentText()
            UrlL=self.dockwidget.lineEditURL.text()
            DescripcionL=self.dockwidget.lineEditDESCRIP.text()
            FormatoL=self.dockwidget.lineEditFORMATO.text()
            mimeL=self.dockwidget.lineEditMIME.text()
            TamanoL=self.dockwidget.lineEditTAMANOENL.text()
            fecha = date.today()
            fecha=f'{fecha}:'
            Historia=self.dockwidget.textEditHISTORIA.toPlainText()
            p=0
            self.dockwidget.textBrowserRESUMEN.clear()
            if accion=='Seleccionar':
                pass
            elif accion=='Agregar Metadatos':
                #Datos Identificacion
                p=self.datosIdentifier(Identifier, ParentIdentifier, Title, Type, LanguageId, LanguageCt, Abstract, Categorieslist, Keywordslist, accion)
                print(p)
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                #Datos Extension
                p1=self.datosExtent(CRS, Xmin, Ymin, Xmax, Ymax, Zmax, Zmin,  accion)
                p=p+p1
                p1t=self.datosExtentTemporal(Inicio, Fin, accion)
                p=p+p1t
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                #Datos Acceso
                p2=self.datosAccess( Cuota, Licencias, Derechos, accion)
                p=p+p2
                p3=self.datosConstraint(ResAces, ResUso, ResOtro, accion)
                p=p+p3
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                #Datos Contacto
                p4=self.datosContact( NombreC, RolC, OrganizacionC, PosicionC, EmailC, Telefono1C, Telefono2C, accion)
                p=p+p4
                p5=self.datosAddress(PostaltipoC, CodigopostalC, DireccionC, PaisC, Areadmin, CiudadC, accion)
                p=p+p5
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                #Datos Link
                p6=self.datosLink(NombreL, LinktipoL, UrlL, DescripcionL, FormatoL, mimeL, TamanoL, accion)
                p=p+p6
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                #Datos Historia
                if len(Historia)>0 and Historia!=fecha:
                    p=p+1
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>Historia(s):</b><i> {Historia}</i>')
                else:
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>Historia(s):</b>')
                #Barra de progreso
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                self.datosProgress( p, capa, accion)
            elif accion=='Adicionar Palabras Clave':
                if len(Keywordslist)>0:
                    p=p+1
                    Keywordslist1 = Keywordslist. split (";")
                    dic={}
                    for k in Keywordslist1:
                        k1 = k. split (":")
                        #clave
                        kk=k1[0]
                        kk=kk.replace("'","")
                        #Valor
                        v=k1[1]
                        v=v.replace('[','')
                        v=v.replace(']','')
                        v=v.replace("'","")
                        v1 = v. split (",")
                        dic[kk]=v1
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>Palabras Clave:</b><i> {dic}</i>')
                #Barra de progreso
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                self.datosProgress( p, capa, accion)
            elif accion=='Adicionar Restriciones':
                p=self.datosConstraint(ResAces, ResUso, ResOtro, accion)
                #Barra de progreso
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                self.datosProgress( p, capa, accion)
            elif accion=='Adicionar un Contacto':
                p=self.datosContact( NombreC, RolC, OrganizacionC, PosicionC, EmailC, Telefono1C, Telefono2C, accion)
                p1=self.datosAddress(PostaltipoC, CodigopostalC, DireccionC, PaisC, Areadmin, CiudadC, accion)
                p=p+p1
                #Barra de progreso
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                self.datosProgress( p, capa, accion)
            elif accion=='Adicionar una Dirección':
                p=self.datosAddress(PostaltipoC, CodigopostalC, DireccionC, PaisC, Areadmin, CiudadC, accion)
                #Nombre de los contactos
                ContactsNum=len(capa.metadata().contacts())
                if ContactsNum>1:
                    self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                    self.dockwidget.textBrowserRESUMEN.append('Al ejecutar la operación se solicitará el <u>contacto</u> a quien adicionar la dirección, entre:')
                    ContactsList=[capa.metadata().contacts()[f].name for f in range(ContactsNum)]
                    n=1
                    for namec in ContactsList:
                        self.dockwidget.textBrowserRESUMEN.append(f'> > > > > > > {n}) <b>{namec}</b>')
                        n=n+1
                else:
                    pass
                #Barra de progreso
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                self.datosProgress( p, capa, accion)
            elif accion=='Adicionar un Link':
                p=self.datosLink(NombreL, LinktipoL, UrlL, DescripcionL, FormatoL, mimeL, TamanoL, accion)
                #Barra de progreso
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                self.datosProgress( p, capa, accion)
            elif accion=='Adicionar Historias':
                if len(Historia)>0 and Historia!=fecha:
                    p=p+1
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>Historia(s):</b><i> {Historia}</i>')
                else:
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>Historia(s):</b>')
                #Barra de progreso
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                self.datosProgress( p, capa, accion)
            elif accion=='Modificar Metadatos':
                p=self.datosIdentifier(Identifier, ParentIdentifier, Title, Type, LanguageId, LanguageCt, Abstract, Categorieslist, Keywordslist, accion)
                print(p)
                #Datos Extension
                if len(Xmin)>0 and len(Ymin)>0 and len(Ymax)>0 and len(Xmax)>0 and Zmax!=99999.99 and Zmin!=99999.99:
                    p1=self.datosExtent(CRS, Xmin, Ymin, Xmax, Ymax, Zmax, Zmin, accion)
                    p=p+p1
                else:
                    if len(Xmin)>0 or len(Ymin)>0 or len(Ymax)>0 or len(Xmax)>0 or Zmax!=99999.99 or Zmin!=99999.99:
                        self.dockwidget.textBrowserRESUMEN.append('Debe definir <b>XYZ Minímo-XYZ Máxima</b>')
                    else:
                        pass
                if Inicio!='dom ene 1 12:00:00 2023' and Fin!='dom ene 1 12:00:00 2023':
                    p1t=self.datosExtentTemporal(Inicio, Fin, accion)
                    p=p+p1t
                else:
                    if Inicio!='dom ene 1 12:00:00 2023' or Fin!='dom ene 1 12:00:00 2023':
                        self.dockwidget.textBrowserRESUMEN.append('Debe definir <b>Desde y Hasta</b>')
                    else:
                        pass
                #Datos Acceso
                p2=self.datosAccess( Cuota, Licencias, Derechos, accion)
                p=p+p2
                p3=self.datosConstraint(ResAces, ResUso, ResOtro, accion)
                p=p+p3
                #Datos Contacto
                p4=self.datosContact( NombreC, RolC, OrganizacionC, PosicionC, EmailC, Telefono1C, Telefono2C, accion)
                p=p+p4
                p5=self.datosAddress(PostaltipoC, CodigopostalC, DireccionC, PaisC, Areadmin, CiudadC, accion)
                p=p+p5
                #Datos Link
                p6=self.datosLink(NombreL, LinktipoL, UrlL, DescripcionL, FormatoL, mimeL, TamanoL, accion)
                p=p+p6
                #Datos Historia
                if len(Historia)>0 and Historia!=fecha:
                    p=p+1
                    self.dockwidget.textBrowserRESUMEN.append(f'<b>Historia(s):</b><i> {Historia}</i>')
                else:
                    pass
                #Barra de progreso
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                self.datosProgress( p, capa, accion)
            elif accion=='Remover Palabra Clave':
                m=capa.metadata()
                d=capa.metadata().keywords()
                keysd=d.keys()
                listKey=[d for d in keysd]
                print(listKey)
                print(len(listKey))
                if len(listKey)>1:
                    self.dockwidget.textBrowserRESUMEN.append('Al ejecutar se solicitará el concepto a remover')
                    self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                    self.datosProgress( p, capa, accion)
                elif len(listKey)==1:
                    self.dockwidget.textBrowserRESUMEN.append('La palabra clave será removida.')
                    self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                    self.datosProgress( p, capa, accion)
                else:
                    self.dockwidget.textBrowserRESUMEN.append('No existen palabras clave que remover.')
                    self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(True)
            elif accion=='Remover Restricción':
                re=len(capa.metadata().constraints())
                if re>1:
                    self.dockwidget.textBrowserRESUMEN.append('Al ejecutar se solicitará la restricción(tipo) a remover.')
                    self.dockwidget.textBrowserRESUMEN.append('<u>RESTRICCIONES:</u>')
                    for r in range(re):
                        text=f'<b>{capa.metadata().constraints()[r].type}</b>={capa.metadata().constraints()[r].constraint}'
                        self.dockwidget.textBrowserRESUMEN.append(text)
                    self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                    self.datosProgress( p, capa, accion)
                elif re==1:
                    self.dockwidget.textBrowserRESUMEN.append('La restricción será removida.')
                    self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                    self.datosProgress( p, capa, accion)
                else:
                    self.dockwidget.textBrowserRESUMEN.append('No existen restriccion(es) que remover.')
                    self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(True)
            elif accion=='Remover un Contacto':
                co=len(capa.metadata().contacts())
                if co>1:
                    self.dockwidget.textBrowserRESUMEN.append('Al ejecutar se solicitará el contacto(nombre) a remover.')
                    self.dockwidget.textBrowserRESUMEN.append('<u>CONTACTO:</u>')
                    for c in range(co):
                        text=f'{capa.metadata().contacts()[c].name}'
                        self.dockwidget.textBrowserRESUMEN.append(text)
                    self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                    self.datosProgress( p, capa, accion)
                elif co==1:
                    self.dockwidget.textBrowserRESUMEN.append('El contacto será removido.')
                    self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                    self.datosProgress( p, capa, accion)
                else:
                    self.dockwidget.textBrowserRESUMEN.append('No existen contacto(s) que remover.')
                    self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(True)
            elif accion=='Remover una Dirección':
                co=len(capa.metadata().contacts())
                if co>1:
                    self.dockwidget.textBrowserRESUMEN.append('- Al ejecutar se solicitará el contacto a quien se removerá una dirección.')
                    self.dockwidget.textBrowserRESUMEN.append('- Si el contacto posee más de una dirección, se solicitará la dirección(número) a remover.')
                    self.dockwidget.textBrowserRESUMEN.append('<u>CONTACTO (Número de direcciones que posee):</u>')
                    for c in range(co):
                        nd=len(capa.metadata().contacts()[c].addresses)
                        text=f'{capa.metadata().contacts()[c].name} <b>({nd})</b>'
                        self.dockwidget.textBrowserRESUMEN.append(text)
                    self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                    self.datosProgress( p, capa, accion)
                elif co==1:
                    nd=len(capa.metadata().contacts()[0].addresses)
                    if nd>1:
                        self.dockwidget.textBrowserRESUMEN.append('Se solicitará la dirección(número) a remover.')
                        for d in range(nd):
                            d1=d+1
                            text=f'Dirección  <b>({d1})</b>'
                            self.dockwidget.textBrowserRESUMEN.append(text)
                        self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                        self.datosProgress( p, capa, accion)
                    elif nd==1:
                        self.dockwidget.textBrowserRESUMEN.append('La dirección del contacto será removida.')
                        self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                        self.datosProgress( p, capa, accion)
                    else:
                        self.dockwidget.textBrowserRESUMEN.append('El contacto no posee una dirección asignada.')
                        self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                        self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(True)
                else:
                    self.dockwidget.textBrowserRESUMEN.append('No hay contacto registrado.')
                    self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                    self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(True)
            elif accion=='Remover un Link':
                li=len(capa.metadata().links())
                if li>1:
                    self.dockwidget.textBrowserRESUMEN.append('Al ejecutar se solicitará el enlace(nombre) a remover.')
                    self.dockwidget.textBrowserRESUMEN.append('<u>LINK:</u>')
                    for l in range(li):
                        text=f'{capa.metadata().links()[l].name}'
                        self.dockwidget.textBrowserRESUMEN.append(text)
                    self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                    self.datosProgress( p, capa, accion)
                elif li==1:
                    self.dockwidget.textBrowserRESUMEN.append('El enlace(link) será removido.')
                    self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                    self.datosProgress( p, capa, accion)
                else:
                    self.dockwidget.textBrowserRESUMEN.append('No existen enlace(s) que remover.')
                    self.dockwidget.pushButtonAGREGARMETADATO.setDisabled(True)
            elif accion=='Remover Metadatos':
                self.dockwidget.textBrowserRESUMEN.append('<b>******PRECAUCIÓN******</b>')
                self.dockwidget.textBrowserRESUMEN.append('Todos los metadatos serán removidos.')
                self.dockwidget.textBrowserRESUMEN.append('-------------------------------')
                self.datosProgress( p, capa, accion)
            else:
                pass
        except:
            pass
    #Metadatos
    def setMetadatos(self):
        accion=self.dockwidget.comboBoxACCION.currentText()
        # Obtener la capa actualmente seleccionada en QGIS
        capa = self.dockwidget.comboBoxCAPASEL.currentData()
        Identifier=self.dockwidget.lineEditIDENTIFICADOR.text()
        ParentIdentifier=self.dockwidget.lineEditIDENTIFICADOR_ORIGEN.text()
        Title=self.dockwidget.lineEditTITULO.text()
        Type=self.dockwidget.lineEditTIPO.text()
        LanguageId=self.dockwidget.comboBoxIDIOMAID.currentText()
        LanguageCt=self.dockwidget.comboBoxIDIOMAPAIS.currentText()
        Abstract=self.dockwidget.lineEditRESUMEN.text()
        Categorieslist=self.dockwidget.lineEditCATEGORIA.text()
        Keywordslist=self.dockwidget.lineEditPALABRASCLAVES.text()
        #Datos Extension
        CRS=self.dockwidget.lineEditCRS.text()
        Xmin=self.dockwidget.lineEditXMIN.text()
        Ymin=self.dockwidget.lineEditYMIN.text()
        Xmax=self.dockwidget.lineEditXMAX.text()
        Ymax=self.dockwidget.lineEditYMAX.text()
        Zmax=self.dockwidget.doubleSpinBoxZMAX.value()
        Zmin=self.dockwidget.doubleSpinBoxZMIN.value()
        Inicio=self.dockwidget.dateTimeEditINICIO.dateTime ()
        Fin=self.dockwidget.dateTimeEditFINAL.dateTime ()
        #Datos Acceso
        Cuota=self.dockwidget.lineEditCUOTAS.text()
        LicenciasList=self.dockwidget.lineEditLICENCIAS.text()
        DerechosList=self.dockwidget.lineEditDERECHOS.text()
        ResAces=self.dockwidget.lineEditACCESO.text()
        ResUso=self.dockwidget.lineEditUSO.text()
        ResOtro=self.dockwidget.lineEditOTRO.text()
        #Datos Contacto
        NombreC=self.dockwidget.lineEditNOMBRE.text()
        RolC=self.dockwidget.lineEditROL.text()
        OrganizacionC=self.dockwidget.lineEditORGANIZACION.text()
        PosicionC=self.dockwidget.lineEditPOSICION.text()
        EmailC=self.dockwidget.lineEditEMAIL.text()
        TELEFONO1C=self.dockwidget.lineEditTELEFONO.text()
        TELEFONO2C=self.dockwidget.lineEditOTRONUMERO.text()
        PostaltipoC=self.dockwidget.comboBoxTIPODIRECCION.currentText()
        if PostaltipoC=='...':
            PostaltipoC=''
        else:
            pass
        CodigopostalC=self.dockwidget.lineEditCODIGOPOSTAL.text()
        DireccionC=self.dockwidget.lineEditDIRECCION.text()
        PaisC=self.dockwidget.lineEditPAIS.text()
        AreadminC=self.dockwidget.lineEditAREAADMIN.text()
        CiudadC=self.dockwidget.lineEditCIUDAD.text()
        #Datos Link
        NombreL=self.dockwidget.lineEditNOMBREENL.text()
        LinktipoL=self.dockwidget.comboBoxTIPOENL.currentText()
        if LinktipoL=='...':
            LinktipoL=''
        else:
            pass
        UrlL=self.dockwidget.lineEditURL.text()
        DescripcionL=self.dockwidget.lineEditDESCRIP.text()
        FormatoL=self.dockwidget.lineEditFORMATO.text()
        mimeL=self.dockwidget.lineEditMIME.text()
        TamanoL=self.dockwidget.lineEditTAMANOENL.text()
        #Datos Historia
        HistoriaList=self.dockwidget.textEditHISTORIA.toPlainText()
        if accion=='Seleccionar':
            pass
        elif accion=='Agregar Metadatos':
            #Datos Identificación
            Language=f'{LanguageId}-{LanguageCt}'
            if Language=='...-...':
                Language=''
            else:
                pass
            Categories = Categorieslist. split (",")
            Keywordslist1 = Keywordslist. split (";")
            dic={}
            try:
                for k in Keywordslist1:
                    k1 = k. split (":")
                    #clave
                    kk=k1[0]
                    kk=kk.replace("'","")
                    #Valor
                    v=k1[1]
                    v=v.replace('[','')
                    v=v.replace(']','')
                    v=v.replace("'","")
                    v1 = v. split (",")
                    dic[kk]=v1
                #se agrega la cateoria al dic de keywords
                if len(Categorieslist)>0:
                    dic['gmd:topicCategory']=Categories
                else:
                    dic['gmd:topicCategory']=[]
            except:
                pass
            Licencias=LicenciasList. split (",")
            Derechos=DerechosList. split (",")
            #Historia
            fecha = date.today()
            fecha=f'{fecha}:'
            if HistoriaList!=fecha:
                Historia=HistoriaList. split (",")
            else:
                Historia=[]
            #setIdentifier
            m = QgsLayerMetadata()
            m.setIdentifier(Identifier)
            m.setParentIdentifier(ParentIdentifier)
            m.setTitle(Title)
            m.setType(Type)
            m.setLanguage(Language)
            m.setCategories(Categories)
            m.setAbstract(Abstract)
            m.setKeywords(dic)
            #setExtendet
            m.setCrs(QgsCoordinateReferenceSystem.fromOgcWmsCrs(CRS))
            e = QgsLayerMetadata.Extent()
            se = QgsLayerMetadata.SpatialExtent()
            se.extentCrs = QgsCoordinateReferenceSystem.fromOgcWmsCrs(CRS)
            if len(Xmin)>0:
                Xmin=float(Xmin)
            else:
                Xmin=0
            if len(Ymin)>0:
                Ymin=float(Ymin)
            else:
                Ymin=0
            if len(Xmax)>0:
                Xmax=float(Xmax)
            else:
                Xmax=0
            if len(Ymax)>0:
                Ymax=float(Ymax)
            else:
                Ymax=0
            if Zmax==99999.99:
                Zmax=0
            else:
                Zmax=float(Zmax)
            if Zmin==99999.99:
                Zmin=0
            else:
                Zmin=float(Zmin)
            se.bounds = QgsBox3d(Xmin, Ymin, Zmin, Xmax, Ymax, Zmax)
            e.setSpatialExtents([se])
            dates = [QgsDateTimeRange(Inicio,Fin)]
            e.setTemporalExtents(dates)
            m.setExtent(e)
            #setAccess
            m.setFees(Cuota)
            if len(ResAces)>0 and len(ResUso)==0 and len(ResOtro)==0:
                m.setConstraints([QgsLayerMetadata.Constraint(ResAces, 'Access')])
            elif len(ResAces)>0 and len(ResUso)>0 and len(ResOtro)==0:
                m.setConstraints([QgsLayerMetadata.Constraint(ResAces, 'Access'),QgsLayerMetadata.Constraint(ResUso, 'Use')])
            elif len(ResAces)>0 and len(ResUso)==0 and len(ResOtro)>0:
                m.setConstraints([QgsLayerMetadata.Constraint(ResAces, 'Access'),QgsLayerMetadata.Constraint(ResOtro, 'Other')])
            elif len(ResAces)>0 and len(ResUso)>0 and len(ResOtro)>0:
                m.setConstraints([QgsLayerMetadata.Constraint(ResAces, 'Access'),QgsLayerMetadata.Constraint(ResUso, 'Use'),QgsLayerMetadata.Constraint(ResOtro, 'Other')])
            elif len(ResAces)==0 and len(ResUso)>0 and len(ResOtro)==0:
                m.setConstraints([QgsLayerMetadata.Constraint(ResUso, 'Use')])
            elif len(ResAces)==0 and len(ResUso)>0 and len(ResOtro)>0:
                m.setConstraints([QgsLayerMetadata.Constraint(ResUso, 'Use'),QgsLayerMetadata.Constraint(ResOtro, 'Other')])
            elif len(ResAces)==0 and len(ResUso)==0 and len(ResOtro)>0:
                m.setConstraints([QgsLayerMetadata.Constraint(ResOtro, 'Other')])
            else:
                pass
            m.setRights(Derechos)
            m.setLicenses(Licencias)
            #setContact
            c = QgsLayerMetadata.Contact()
            c.name = NombreC
            c.organization = OrganizacionC
            c.position = PosicionC
            c.voice = TELEFONO1C
            c.fax = TELEFONO2C
            c.email = EmailC
            c.role = RolC
            address = QgsLayerMetadata.Address()
            address.type = PostaltipoC
            address.address = DireccionC
            address.city = CiudadC
            address.administrativeArea = AreadminC
            address.postalCode = CodigopostalC
            address.country = PaisC
            c.addresses = [address]
            m.setContacts([c])
            #setLink
            l = QgsLayerMetadata.Link()
            l.name = NombreL
            l.type = LinktipoL
            l.description = DescripcionL
            l.url = UrlL
            l.format = FormatoL
            l.mimeType = mimeL
            l.size = TamanoL
            m.setLinks([l])
            m.setHistory(Historia)
            capa.setMetadata(m)
            iface.messageBar().pushMessage('Los metadatos se agregaron a la capa con éxito'+"\U0001F60C", Qgis.Success)
        elif accion=='Adicionar Palabras Clave':
            Keywordslist1 = Keywordslist. split (";")
            m=capa.metadata()
            try:
                for k in Keywordslist1:
                    k1 = k. split (":")
                    #clave
                    kk=k1[0]
                    kk=kk.replace("'","")
                    #Valor
                    v=k1[1]
                    v=v.replace('[','')
                    v=v.replace(']','')
                    v=v.replace("'","")
                    v1 = v. split (",")
                    m.addKeywords(kk,v1)
            except:
                pass
            capa.setMetadata(m)
            iface.messageBar().pushMessage('Las Palabras Clave (metadatos) se adicionaron a la capa con éxito'+"\U0001F60C", Qgis.Success)
        elif accion=='Adicionar Restriciones':
            m=capa.metadata()
            if len(ResAces)>0:
                m.addConstraint(QgsLayerMetadata.Constraint(ResAces, 'Access'))
            else:
                pass
            if len(ResUso)>0:
                m.addConstraint(QgsLayerMetadata.Constraint(ResUso, 'Use'))
            else:
                pass
            if len(ResOtro)>0:
                m.addConstraint(QgsLayerMetadata.Constraint(ResOtro, 'Other'))
            else:
                pass
            capa.setMetadata(m)
            iface.messageBar().pushMessage('La(s) Restricción(es) (metadatos) se adicionaron a la capa con éxito'+"\U0001F60C", Qgis.Success)
        elif accion=='Adicionar un Contacto':
            m=capa.metadata()
            c = QgsLayerMetadata.Contact()
            c.name = NombreC
            c.organization = OrganizacionC
            c.position = PosicionC
            c.voice = TELEFONO1C
            c.fax = TELEFONO2C
            c.email = EmailC
            c.role = RolC
            address = QgsLayerMetadata.Address()
            address.type = PostaltipoC
            address.address = DireccionC
            address.city = CiudadC
            address.administrativeArea = AreadminC
            address.postalCode = CodigopostalC
            address.country = PaisC
            c.addresses = [address]
            m.addContact(c)
            capa.setMetadata(m)
            iface.messageBar().pushMessage('El contacto y su dirección (metadatos) se adicionó a la capa con éxito'+"\U0001F60C", Qgis.Success)
        elif accion=='Adicionar una Dirección':
            try:
                m=capa.metadata()
                ContactsNum=len(capa.metadata().contacts())
                if ContactsNum>1:
                    ContactsList=[capa.metadata().contacts()[f].name for f in range(ContactsNum)]
                    contact, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona un contacto","Contacto:",ContactsList,0,False)
                    idc=ContactsList.index(contact)
                else:
                    idc=0
                c=capa.metadata().contacts()
                cx=capa.metadata().contacts()[idc]
                d=cx.addresses
                addressA = QgsLayerMetadata.Address()
                addressA.type = PostaltipoC
                addressA.address = DireccionC
                addressA.city = CiudadC
                addressA.administrativeArea = AreadminC
                addressA.postalCode = CodigopostalC
                addressA.country = PaisC
                d.append(addressA)
                cx.addresses = d
                c[idc]=cx
                m.setContacts(c)
                capa.setMetadata(m)
                iface.messageBar().pushMessage('La dirección (metadatos) se adicionó al contacto con éxito'+"\U0001F60C", Qgis.Success)
            except:
                ContactsNum=len(capa.metadata().contacts())
                if ContactsNum==0:
                    iface.messageBar().pushMessage('No hay contactos', Qgis.Warning)
                else:
                    iface.messageBar().pushMessage('No se ejecutó', Qgis.Warning)
        elif accion=='Adicionar un Link':
            m=capa.metadata()
            lA=QgsLayerMetadata.Link()
            lA.name = NombreL
            lA.type = LinktipoL
            lA.description = DescripcionL
            lA.url = UrlL
            lA.format = FormatoL
            lA.mimeType = mimeL
            lA.size = TamanoL
            m.addLink(lA)
            capa.setMetadata(m)
            iface.messageBar().pushMessage('El enlace se adicionó a la capa con éxito'+"\U0001F60C", Qgis.Success)
        elif accion=='Adicionar Historias':
            fecha = date.today()
            fecha=f'{fecha}:'
            if HistoriaList!=fecha:
                m=capa.metadata()
                Historia=HistoriaList. split (",")
                for h in Historia:
                    m.addHistoryItem(h)
                capa.setMetadata(m)
                iface.messageBar().pushMessage('La(s) Historia(s) fueron adicionadas a la capa con éxito'+"\U0001F60C", Qgis.Success)
            else:
                pass
        elif accion=='Modificar Metadatos':
            m=capa.metadata()
            if len(Identifier)>0:
                m.setIdentifier(Identifier)
            else:
                pass
            if len(ParentIdentifier)>0:
                m.setParentIdentifier(ParentIdentifier)
            else:
                pass
            if len(Title)>0:
                m.setTitle(Title)
            else:
                pass
            if len(Type)>0:
                m.setType(Type)
            else:
                pass
            if len(LanguageId)>0 and len(LanguageCt)>0:
                Language=f'{LanguageId}-{LanguageCt}'
                if Language=='...-...':
                    pass
                else:
                    m.setLanguage(Language)
            else:
                pass
            if len(Abstract)>0:
                m.setAbstract(Abstract)
            else:
                pass
            if len(Categorieslist)>0:
                Categories = Categorieslist. split (",")
                m.setCategories(Categories)
            else:
                pass
            if len(Keywordslist)>0:
                try:
                    Keywordslist1 = Keywordslist. split (";")
                    dic={}
                    for k in Keywordslist1:
                        k1 = k. split (":")
                        #clave
                        kk=k1[0]
                        kk=kk.replace("'","")
                        #Valor
                        v=k1[1]
                        v=v.replace('[','')
                        v=v.replace(']','')
                        v=v.replace("'","")
                        v1 = v. split (",")
                        dic[kk]=v1
                    #se agrega la cateoria al dic de keywords
                    if len(Categorieslist)>0:
                        dic['gmd:topicCategory']=Categories
                    else:
                        pass
                    m.setKeywords(dic)
                except:
                    pass
            else:
                pass
            if len(CRS)>0 and CRS!='EPSG:':
                m.setCrs(QgsCoordinateReferenceSystem.fromOgcWmsCrs(CRS))
            else:
                pass
            e = m.extent()
            if len(Xmin)>0 and len(Ymin)>0 and len(Ymax)>0 and len(Xmax)>0 and Zmax!=99999.99 and Zmin!=99999.99:
                se = m.SpatialExtent()
                se.extentCrs = QgsCoordinateReferenceSystem.fromOgcWmsCrs(CRS)
                Xmin=float(Xmin)
                Ymin=float(Ymin)
                Xmax=float(Xmax)
                Ymax=float(Ymax)
                if Zmax==99999.99:
                    Zmax=0
                else:
                    Zmax=float(Zmax)
                if Zmin==99999.99:
                    Zmin=0
                else:
                    Zmin=float(Zmin)
                se.bounds = QgsBox3d(Xmin, Ymin, Zmin, Xmax,Ymax, Zmax)
                e.setSpatialExtents([se])
                m.setExtent(e)
            else:
                pass
            if Inicio.toString()!='dom ene 1 12:00:00 2023' and Fin.toString()!='dom ene 1 12:00:00 2023':
                dates = [QgsDateTimeRange(Inicio,Fin)]
                e.setTemporalExtents(dates)
                m.setExtent(e)
            else:
                pass
            if len(Cuota)>0:
                m.setFees(Cuota)
            else:
                pass
            if len(ResAces)>0 or len(ResUso)>0 or len(ResOtro)>0:
                if len(ResAces)>0 and len(ResUso)==0 and len(ResOtro)==0:
                    m.setConstraints([QgsLayerMetadata.Constraint(ResAces, 'Access')])
                elif len(ResAces)>0 and len(ResUso)>0 and len(ResOtro)==0:
                    m.setConstraints([QgsLayerMetadata.Constraint(ResAces, 'Access'),QgsLayerMetadata.Constraint(ResUso, 'Use')])
                elif len(ResAces)>0 and len(ResUso)==0 and len(ResOtro)>0:
                    m.setConstraints([QgsLayerMetadata.Constraint(ResAces, 'Access'),QgsLayerMetadata.Constraint(ResOtro, 'Other')])
                elif len(ResAces)>0 and len(ResUso)>0 and len(ResOtro)>0:
                    m.setConstraints([QgsLayerMetadata.Constraint(ResAces, 'Access'),QgsLayerMetadata.Constraint(ResUso, 'Use'),QgsLayerMetadata.Constraint(ResOtro, 'Other')])
                elif len(ResAces)==0 and len(ResUso)>0 and len(ResOtro)==0:
                    m.setConstraints([QgsLayerMetadata.Constraint(ResUso, 'Use')])
                elif len(ResAces)==0 and len(ResUso)>0 and len(ResOtro)>0:
                    m.setConstraints([QgsLayerMetadata.Constraint(ResUso, 'Use'),QgsLayerMetadata.Constraint(ResOtro, 'Other')])
                elif len(ResAces)==0 and len(ResUso)==0 and len(ResOtro)>0:
                    m.setConstraints([QgsLayerMetadata.Constraint(ResOtro, 'Other')])
                else:
                    pass
            else:
                pass
            if len(DerechosList)>0:
                Derechos=DerechosList. split (",")
                m.setRights(Derechos)
            else:
                pass
            if len(LicenciasList)>0:
                Licencias=LicenciasList. split (",")
                m.setLicenses(Licencias)
            if len(NombreC)>0 or len(OrganizacionC)>0 or len(PosicionC)>0 or len(OrganizacionC)>0 or len(TELEFONO1C)>0 or len(TELEFONO2C)>0 or len(EmailC)>0 or len(RolC)>0 or len(PostaltipoC)>0 or len(DireccionC)>0 or len(CiudadC)>0 or len(AreadminC)>0 or len(CodigopostalC)>0 or len(PaisC)>0:
                try:
                    NumC=len(m.contacts())
                    if NumC>1:
                        ContactsList=[m.contacts()[f].name for f in range(NumC)]
                        contact, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona un Contacto","Contacto:",ContactsList,0,False)
                        idc=ContactsList.index(contact)
                    else:
                        idc=0
                    c=m.contacts()
                    c1 = m.contacts()[idc]
                    if len(NombreC)>0:
                        c1.name = NombreC
                    else:
                        pass
                    if len(OrganizacionC)>0:
                        c1.organization = OrganizacionC
                    else:
                        pass
                    if len(PosicionC)>0:
                        c1.position = PosicionC
                    else:
                        pass
                    if len(TELEFONO1C)>0:
                        c1.voice = TELEFONO1C
                    else:
                        pass
                    if len(TELEFONO2C)>0:
                        c1.fax = TELEFONO2C
                    else:
                        pass
                    if len(EmailC)>0:
                        c1.email = EmailC
                    else:
                        pass
                    if len(RolC)>0:
                        c1.role = RolC
                    if len(PostaltipoC)>0 or len(DireccionC)>0 or len(CiudadC)>0 or len(AreadminC)>0 or len(CodigopostalC)>0 or len(PaisC)>0:
                        NumA=len(c1.addresses)
                        if NumA>1:
                            AddressesList=[f'Dirección {f+1}' for f in range(NumA)]
                            addresses, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona una dirección","Dirección:",AddressesList,0,False)
                            idd=AddressesList.index(addresses)
                        else:
                            idd=0
                        address = c1.addresses
                        address1 = c1.addresses[idd]
                        if PostaltipoC!='...':
                            address1.type = PostaltipoC
                        else:
                            pass
                        if len(DireccionC)>0:
                            address1.address = DireccionC
                        else:
                            pass
                        if len(CiudadC)>0:
                            address1.city = CiudadC
                        else:
                            pass
                        if len(AreadminC)>0:
                            address1.administrativeArea = AreadminC
                        else:
                            pass
                        if len(CodigopostalC)>0:
                            address1.postalCode = CodigopostalC
                        else:
                            pass
                        if len(PaisC)>0:
                            address1.country = PaisC
                        else:
                            pass
                        address[idd]=address1
                        c1.addresses = (address)
                    else:
                        pass
                    c[idc]=c1
                    m.setContacts(c)
                except:
                    pass
            else:
                pass
            if len(NombreL)>0 or len(LinktipoL)>0 or len(DescripcionL)>0 or len(UrlL)>0 or len(FormatoL)>0 or len(mimeL)>0 or len(TamanoL)>0:
                try:
                    #setLink
                    l = m.links()
                    numLink=len(m.links())
                    if numLink>1:
                        LinkList=[f'{m.links()[f].name}' for f in range(numLink)]
                        link, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona un link","Link:",LinkList,0,False)
                        idl=LinkList.index(link)
                    else:
                        idl=0
                    l1=m.links()[idl]
                    if len(NombreL)>0:
                        l1.name = NombreL
                    else:
                        pass
                    if LinktipoL!='...':
                        l1.type = LinktipoL
                    else:
                        pass
                    if len(DescripcionL)>0:
                        l1.description = DescripcionL
                    else:
                        pass
                    if len(UrlL)>0:
                        l1.url = UrlL
                    else:
                        pass
                    if len(FormatoL)>0:
                        l1.format = FormatoL
                    else:
                        pass
                    if len(mimeL)>0:
                        l1.mimeType = mimeL
                    else:
                        pass
                    if len(TamanoL)>0:
                        l1.size = TamanoL
                    else:
                        pass
                    l[idl]=l1
                    m.setLinks(l)
                except:
                    pass
            else:
                pass
            fecha = date.today()
            fecha=f'{fecha}:'
            if len(HistoriaList)>0 and HistoriaList!=fecha:
                Historia=HistoriaList. split (",")
                m.setHistory(Historia)
            else:
                pass
            capa.setMetadata(m)
            iface.messageBar().pushMessage('El/Los Metadato(s) fueron modificados con éxito'+"\U0001F60C", Qgis.Success)
        elif accion=='Remover Palabra Clave':
            try:
                m=capa.metadata()
                d=capa.metadata().keywords()
                keysd=d.keys()
                listKey=[d for d in keysd]
                if len(listKey)>1:
                    listKey.insert(0,'Seleccionar')
                    concepto, okPressed =QInputDialog.getItem(QComboBox(),"Seleccione un Concepto","Concepto:",listKey,0,False)
                else:
                    concepto=listKey[0]
                m.removeKeywords(concepto)
                capa.setMetadata(m)
                if concepto in keysd:
                    iface.messageBar().pushMessage('La Palabra Clave (metadatos) seleccionada fue removida con éxito'+"\U0001F60C", Qgis.Success)
                else:
                    iface.messageBar().pushMessage('No se ejecutó', Qgis.Warning)
            except:
                iface.messageBar().pushMessage('No se ejecutó', Qgis.Warning)
        elif accion=='Remover Restricción':
            try:
                m=capa.metadata()
                NumCont=len(m.constraints())
                if NumCont>1:
                    ContraintsList=[m.constraints()[f].type for f in range(NumCont)]
                    ContraintsList.insert(0,'Seleccionar')
                    contraint, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona una Restricción","Restricción:",ContraintsList,0,False)
                    idc=ContraintsList.index(contraint)
                    if contraint!='Seleccionar':
                        idc=idc-1
                    else:
                        idc= None 
                else:
                    idc=0
                #Se genera la lista de restricciónes
                ListCont=m.constraints()
                del ListCont[idc]
                m.setConstraints(ListCont)
                capa.setMetadata(m)
                iface.messageBar().pushMessage('La Restricción (metadatos) seleccionada fue removida con éxito'+"\U0001F60C", Qgis.Success)
            except:
                iface.messageBar().pushMessage('No se ejecutó', Qgis.Warning)
        elif accion=='Remover un Contacto':
            try:
                m=capa.metadata()
                NumC=len(m.contacts())
                if NumC>1:
                    ContactsList=[m.contacts()[f].name for f in range(NumC)]
                    ContactsList.insert(0,'Seleccionar')
                    contact, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona un Contacto","Contacto:",ContactsList,0,False)
                    idc=ContactsList.index(contact)
                    if contact!='Seleccionar':
                        idc=idc-1
                    else:
                        idc= None 
                else:
                    idc=0
                #Se genera la lista de contactos
                ListContact=m.contacts()
                del ListContact[idc]
                m.setContacts(ListContact)
                capa.setMetadata(m)
                iface.messageBar().pushMessage('El Contacto (metadatos) seleccionado fue removido con éxito'+"\U0001F60C", Qgis.Success)
            except:
                iface.messageBar().pushMessage('No se ejecutó', Qgis.Warning)
        elif accion=='Remover una Dirección':
            try:
                m=capa.metadata()
                c=m.contacts()
                NumC=len(m.contacts())
                if NumC>1:
                    ContactsList=[m.contacts()[f].name for f in range(NumC)]
                    ContactsList.insert(0,'Seleccionar')
                    contact, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona un Contacto","Contacto:",ContactsList,0,False)
                    idc=ContactsList.index(contact)
                    if contact!='Seleccionar':
                        idc=idc-1
                    else:
                        idc= None 
                else:
                    idc=0

                NumA=len(m.contacts()[idc].addresses)
                if NumA>1:
                    AddressesList=[f'Dirección {f+1}' for f in range(NumA)]
                    AddressesList.insert(0,'Seleccionar')
                    addresses, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona una dirección","Dirección:",AddressesList,0,False)
                    idd=AddressesList.index(addresses)
                    if addresses!='Seleccionar':
                        idd=idd-1
                    else:
                        idd= None 
                else:
                    idd=0
                #Se genera la lista de contactos
                c1=m.contacts()[idc]
                ListAddresses=c1.addresses
                del ListAddresses[idd]
                c1.addresses = (ListAddresses)
                c[idc]=c1
                m.setContacts(c)
                capa.setMetadata(m)
                iface.messageBar().pushMessage('La Dirección (metadatos) seleccionada fue removida con éxito'+"\U0001F60C", Qgis.Success)
            except:
                iface.messageBar().pushMessage('No se ejecutó', Qgis.Warning)
        elif accion=='Remover un Link':
            try:
                m=capa.metadata()
                numLink=len(capa.metadata().links())
                if numLink>1:
                    LinkList=[f'{m.links()[f].name}' for f in range(numLink)]
                    LinkList.insert(0,'Seleccionar')
                    link, okPressed =QInputDialog.getItem(QComboBox(),"Selecciona un link","Link:",LinkList,0,False)
                    idl=LinkList.index(link)
                    if link!='Seleccionar':
                        idl=idl-1
                    else:
                        idl= None 
                else:
                    idl=0
                #Se genera la lista de links
                ListLink=m.links()
                del ListLink[idl]
                m.setLinks(ListLink)
                capa.setMetadata(m)
                iface.messageBar().pushMessage('El Link (metadatos) seleccionado fue removido con éxito'+"\U0001F60C", Qgis.Success)
            except:
                iface.messageBar().pushMessage('No se ejecutó', Qgis.Warning)
        elif accion=='Remover Metadatos':
            try:
                m = QgsLayerMetadata()
                capa.setMetadata(m)
                iface.messageBar().pushMessage('Todos los metadatos fueron removido con éxito'+"\U0001F60C", Qgis.Success)
            except:
                iface.messageBar().pushMessage('No se ejecutó', Qgis.Warning)
        self.dockwidget.radioButtonANCLARCAPA.setChecked(False)
        self.clearI()
        self.clearE()
        self.clearA()
        self.clearC()
        self.clearL()
        self.clearH()
        self.clearR()
        self.items2()
        self.dockwidget.comboBoxTIPOMETADATO.setCurrentText('Seleccionar')
        self.ActiveIcon()
        
    #-------------------------------------------------------------------Pestaña 3
    
    def activeLayer(self):
        try:
            layer=iface.activeLayer()
            layername=layer.name()
            self.dockwidget.labelARCHIVO.setText(f'Capa activa: {layername}')
        except:
            self.dockwidget.labelARCHIVO.setText('Capa activa: ')
    def loadMetadata(self):
        try:
            archivo, _filter= QFileDialog.getOpenFileName(None, "Abrir Archivo",'','*.qmd')
            layer=iface.activeLayer()
            fileOpen= open (archivo , "r")
            contenido = fileOpen . read ( )
            fileOpen.close()
            doc=QDomDocument("METADATA")
            doc.setContent(contenido)
            layer.importNamedMetadata(doc,'')
            iface.messageBar().pushMessage('Los metadatos fueron cargados a la capa con éxito'+"\U0001F60C", Qgis.Success)
            self.dockwidget.comboBoxTIPOMETADATO.setCurrentText('Seleccionar')
        except:
            iface.messageBar().pushMessage('No se ejecutó', Qgis.Warning)
        
    def saveMetadata(self):
        try:
            layer=iface.activeLayer()
            layername=layer.name()
            layername=layername.replace(' ','_')
            archivo, _filter = QFileDialog.getSaveFileName(None,"Guardar como:",f"Metadatos_{layername}", '*.qmd')
            doc = QDomDocument("METADATA")
            iface.activeLayer().exportNamedMetadata(doc,'')
            s = doc.toString()
            with open(archivo, 'w') as output_file:
                output_file.write(s)
                output_file.close()
            iface.messageBar().pushMessage('Los metadatos de la capa fueron guardados en un archivo con éxito'+"\U0001F60C", Qgis.Success)
        except:
            iface.messageBar().pushMessage('No se ejecutó', Qgis.Warning)
    def openFile(self):
        try:
            self.dockwidget.plainTextEditFILE3.clear()
            archivo, _filter= QFileDialog.getOpenFileName(None, "Abrir Archivo",'','*.qmd')
            layer=iface.activeLayer()
            fileOpen= open (archivo , "r")
            contenido = fileOpen . read ( )
            fileOpen.close()
            doc=QDomDocument("METADATA")
            doc.setContent(contenido)
            s = doc.toString()
            self.dockwidget.plainTextEditFILE3.setPlainText(s)
        except:
            iface.messageBar().pushMessage('No se ejecutó', Qgis.Warning)
    def saveFile(self):
        contenido=self.dockwidget.plainTextEditFILE3.toPlainText()
        if len(contenido)>0:
            try:
                contenido=self.dockwidget.plainTextEditFILE3.toPlainText()
                doc=QDomDocument("METADATA")
                doc.setContent(contenido)
                s = doc.toString()
                archivo, _filter = QFileDialog.getSaveFileName(None,"Guardar como:","", '*.qmd')
                with open(archivo, 'w') as output_file:
                    output_file.write(s)
                    output_file.close()
                self.dockwidget.plainTextEditFILE3.clear()
                iface.messageBar().pushMessage('La edición de los metadatos se guardó con éxito'+"\U0001F60C", Qgis.Success)
            except:
                iface.messageBar().pushMessage('No se ejecutó', Qgis.Warning)
        else:
            pass
        
    #--------------------------------------------------------------------------
    def newProject(self):
        self.dockwidget.radioButtonANCLARCAPA.setChecked(False)
        self.items1()
        self.readLayer2()
        self.ActiveIcon()
        self.clearI()
        self.clearE()
        self.clearA()
        self.clearC()
        self.clearL()
        self.clearH()
        self.clearR()
        self.activeLayer()
    
    
    def unload(self):
        #remover del pluggin menu
        self.iface.removePluginMenu("QMetadataLayer", self.action)
        #remover el toolbar:
        del self.Qoilbar
        #remover los botones
        self.iface.removeToolBarIcon(self.action)
        del self.action

    #--------------------------------------------------------------------------


    def runQMS(self):
        """Run method that loads and starts the plugin"""
        # show the dockwidget
        # TODO: fix to allow choice of dock location
        try:
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
        except:
            pass
            
    #--------------------------------------------------------------------------
    
    def autocomplet(self):
        #se abre el archivo
        archivoC = open (os.path.dirname(__file__) + "/default/countrys_es.txt" , "r")
        #se lee
        contenido = archivoC . read ( )
        archivoC.close()
        #se repara
        contenido = contenido . replace ('"','')
        contenido = contenido . replace ("'","")
        countryListEs=contenido. split (",")
        self.completer = QCompleter(countryListEs)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.dockwidget.lineEditPAIS.setCompleter(self.completer)
        
        wordList = ['attribute','attributeType','collectionHardware','collectionSession',\
        'dataset','dataserie','dimensionGroup','feature','featureType','series','sevice','software','tile']
        self.completer = QCompleter(wordList)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.dockwidget.lineEditTIPO.setCompleter(self.completer)
        wordList=['GEMET','formation','fluid','fieldOfStudy','oilfieldType','rockType','sismicType', 'rockProperties']
        self.completer = QCompleter(wordList)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.dockwidget.lineEditCONCEPTOPC.setCompleter(self.completer)
        now=datetime.now()
        wordList=[f'Copyright {now.year}',f'Copyleft {now.year}']
        self.completer = QCompleter(wordList)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.dockwidget.lineEditDERECHOS.setCompleter(self.completer)
        #se abre el archivo
        archivoA = open (os.path.dirname(__file__)+ f"/default/areaAdmin_es.txt" , "r", encoding='utf-8-sig')
        #se lee
        contenido = archivoA . read ( )
        archivoA.close()
        #se repara
        contenido = contenido . replace ('"','')
        contenido = contenido . replace ("'","")
        areaAdminListEs=contenido. split (",")
        self.completer = QCompleter(areaAdminListEs)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.dockwidget.lineEditAREAADMIN.setCompleter(self.completer)
        #se abre el archivo
        archivo = open (os.path.dirname(__file__) + f"/default/ciudades_es.txt" , "r",encoding='utf-8-sig')
        #se lee
        contenido = archivo . read ( )
        archivo.close()
        #se repara
        contenido = contenido . replace ('"','')
        contenido = contenido . replace ("'","")
        city_cpListVe=contenido. split (",")
        cityListVe=[]
        n=0
        for c in city_cpListVe:
            n1=n%2
            if n1==0:
                if c in cityListVe:
                    pass
                else:
                    cityListVe.append(c)
            n=n+1
        self.completer = QCompleter(cityListVe)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.dockwidget.lineEditCIUDAD.setCompleter(self.completer)
        wordList = ['None','Sin Costo']
        self.completer = QCompleter(wordList)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.dockwidget.lineEditCUOTAS.setCompleter(self.completer)
            
        wordList=['application/1d-interleaved-parityfec','application/3gpdash-qoe-report+xml','application/3gppHal+json','application/3gppHalForms+json','application/3gpp-ims+xml','application/A2L','application/ace+cbor','application/ace+json',\
        'application/activemessage','application/activity+json','application/aif+cbor','application/aif+json','application/alto-cdni+json','application/alto-cdnifilter+json','application/alto-costmap+json','application/alto-costmapfilter+json',\
        'application/alto-directory+json','application/alto-endpointprop+json','application/alto-endpointpropparams+json','application/alto-endpointcost+json','application/alto-endpointcostparams+json','application/alto-error+json',\
        'application/alto-networkmapfilter+json','application/alto-networkmap+json','application/alto-propmap+json','application/alto-propmapparams+json','application/alto-updatestreamcontrol+json','application/alto-updatestreamparams+json',\
        'application/AML','application/andrew-inset','application/applefile','application/at+jwt','application/ATF','application/ATFX','application/atom+xml','application/atomcat+xml','application/atomdeleted+xml','application/atomicmail',\
        'application/atomsvc+xml','application/atsc-dwd+xml','application/atsc-dynamic-event-message','application/atsc-held+xml','application/atsc-rdt+json','application/atsc-rsat+xml','application/ATXML','application/auth-policy+xml',\
        'application/automationml-aml+xml','application/automationml-amlx+zip','application/bacnet-xdd+zip','application/batch-SMTP','application/beep+xml','application/c2pa','application/calendar+json','application/calendar+xml',\
        'application/call-completion','application/CALS-1840','application/captive+json','application/cbor','application/cbor-seq','application/cccex','application/ccmp+xml','application/ccxml+xml','application/cda+xml','application/CDFX+XML',\
        'application/cdmi-capability','application/cdmi-container','application/cdmi-domain','application/cdmi-object','application/cdmi-queue','application/cdni','application/CEA','application/cea-2018+xml','application/cellml+xml','application/cfw',\
        'application/cid-edhoc+cbor-seq','application/city+json','application/clr','application/clue_info+xml','application/clue+xml','application/cms','application/cnrp+xml','application/coap-group+json','application/coap-payload',\
        'application/commonground','application/concise-problem-details+cbor','application/conference-info+xml','application/cpl+xml','application/cose','application/cose-key','application/cose-key-set','application/cose-x509','application/csrattrs',\
        'application/csta+xml','application/CSTAdata+xml','application/csvm+json','application/cwl','application/cwl+json','application/cwt','application/cybercash','application/dash+xml','application/dash-patch+xml','application/dashdelta',\
        'application/davmount+xml','application/dca-rft','application/DCD','application/dec-dx','application/dialog-info+xml','application/dicom','application/dicom+json','application/dicom+xml','application/DII','application/DIT','application/dns',\
        'application/dns+json','application/dns-message','application/dots+cbor','application/dpop+jwt','application/dskpp+xml','application/dssc+der','application/dssc+xml','application/dvcs','application/ecmascript','application/edhoc+cbor-seq',\
        'application/EDI-consent','application/EDIFACT','application/EDI-X12','application/efi','application/elm+json','application/elm+xml','application/EmergencyCallData.cap+xml','application/EmergencyCallData.Comment+xml',\
        'application/EmergencyCallData.Control+xml','application/EmergencyCallData.DeviceInfo+xml','application/EmergencyCallData.eCall.MSD','application/EmergencyCallData.LegacyESN+json','application/EmergencyCallData.ProviderInfo+xml',\
        'application/EmergencyCallData.ServiceInfo+xml','application/EmergencyCallData.SubscriberInfo+xml','application/EmergencyCallData.VEDS+xml','application/emma+xml','application/emotionml+xml','application/encaprtp','application/epp+xml',\
        'application/epub+zip','application/eshop','application/example','application/exi','application/expect-ct-report+json','application/express','application/fastinfoset','application/fastsoap','application/fdf','application/fdt+xml',\
        'application/fhir+json','application/fhir+xml','application/fits','application/flexfec','application/font-sfnt','application/font-tdpfr','application/font-woff','application/framework-attributes+xml','application/geo+json','application/geo+json-seq',\
        'application/geopackage+sqlite3','application/geoxacml+xml','application/gltf-buffer','application/gml+xml','application/gzip','application/H224','application/held+xml','application/hl7v2+xml','application/http','application/hyperstudio',\
        'application/ibe-key-request+xml','application/ibe-pkg-reply+xml','application/ibe-pp-data','application/iges','application/im-iscomposing+xml','application/index','application/index.cmd','application/index.obj','application/index.response',\
        'application/index.vnd','application/inkml+xml','application/IOTP','application/ipfix','application/ipp','application/ISUP','application/its+xml','application/java-archive','application/javascript','application/jf2feed+json','application/jose',\
        'application/jose+json','application/jrd+json','application/jscalendar+json','application/jscontact+json','application/json','application/json-patch+json','application/json-seq','application/jsonpath','application/jwk+json','application/jwk-set+json',\
        'application/jwt','application/kpml-request+xml','application/kpml-response+xml','application/ld+json','application/lgr+xml','application/link-format','application/linkset','application/linkset+json','application/load-control+xml','application/logout+jwt',\
        'application/lost+xml','application/lostsync+xml','application/lpf+zip','application/LXF','application/mac-binhex40','application/macwriteii','application/mads+xml','application/manifest+json','application/marc','application/marcxml+xml',\
        'application/mathematica','application/mathml+xml','application/mathml-content+xml','application/mathml-presentation+xml','application/mbms-associated-procedure-description+xml','application/mbms-deregister+xml','application/mbms-envelope+xml',\
        'application/mbms-msk-response+xml','application/mbms-msk+xml','application/mbms-protection-description+xml','application/mbms-reception-report+xml','application/mbms-register-response+xml','application/mbms-register+xml','application/mbms-schedule+xml',\
        'application/mbms-user-service-description+xml','application/mbox','application/media_control+xml','application/media-policy-dataset+xml','application/mediaservercontrol+xml','application/merge-patch+json','application/metalink4+xml','application/mets+xml',\
        'application/MF4','application/mikey','application/mipc','application/missing-blocks+cbor-seq','application/mmt-aei+xml','application/mmt-usd+xml','application/mods+xml','application/moss-keys','application/moss-signature','application/mosskey-data',\
        'application/mosskey-request','application/mp21','application/mp4','application/mpeg4-generic','application/mpeg4-iod','application/mpeg4-iod-xmt','application/mrb-consumer+xml','application/mrb-publish+xml','application/msc-ivr+xml','application/msc-mixer+xml',\
        'application/msword','application/mud+json','application/multipart-core','application/mxf','application/n-quads','application/n-triples','application/nasdata','application/news-checkgroups','application/news-groupinfo','application/news-transmission',\
        'application/nlsml+xml','application/node','application/nss','application/oauth-authz-req+jwt','application/oblivious-dns-message','application/ocsp-request','application/ocsp-response','application/octet-stream','application/ODA','application/odm+xml',\
        'application/ODX','application/oebps-package+xml','application/ogg','application/ohttp-keys','application/opc-nodeset+xml','application/oscore','application/oxps','application/p21','application/p21+zip','application/p2p-overlay+xml','application/parityfec',\
        'application/passport','application/patch-ops-error+xml','application/pdf','application/PDX','application/pem-certificate-chain','application/pgp-encrypted','application/pgp-keys','application/pgp-signature','application/pidf-diff+xml','application/pidf+xml',\
        'application/pkcs10','application/pkcs7-mime','application/pkcs7-signature','application/pkcs8','application/pkcs8-encrypted','application/pkcs12','application/pkix-attr-cert','application/pkix-cert','application/pkix-crl','application/pkix-pkipath',\
        'application/pkixcmp','application/pls+xml','application/poc-settings+xml','application/postscript','application/ppsp-tracker+json','application/private-token-issuer-directory','application/private-token-request','application/private-token-response',\
        'application/problem+json','application/problem+xml','application/provenance+xml','application/prs.alvestrand.titrax-sheet','application/prs.cww','application/prs.cyn','application/prs.hpub+zip','application/prs.implied-document+xml','application/prs.implied-executable',\
        'application/prs.implied-structure','application/prs.nprend','application/prs.plucker','application/prs.rdf-xml-crypt','application/prs.vcfbzip2','application/prs.xsf+xml','application/pskc+xml','application/pvd+json','application/rdf+xml','application/route-apd+xml',\
        'application/route-s-tsid+xml','application/route-usd+xml','application/QSIG','application/raptorfec','application/rdap+json','application/reginfo+xml','application/relax-ng-compact-syntax','application/remote-printing','application/reputon+json','application/resource-lists-diff+xml',\
        'application/resource-lists+xml','application/rfc+xml','application/riscos','application/rlmi+xml','application/rls-services+xml','application/rpki-checklist','application/rpki-ghostbusters','application/rpki-manifest','application/rpki-publication','application/rpki-roa',\
        'application/rpki-updown','application/rtf','application/rtploopback','application/rtx','application/samlassertion+xml','application/samlmetadata+xml','application/sarif-external-properties+json','application/sarif+json','application/sbe','application/sbml+xml','application/scaip+xml',\
        'application/scim+json','application/scvp-cv-request','application/scvp-cv-response','application/scvp-vp-request','application/scvp-vp-response','application/sdp','application/secevent+jwt','application/senml-etch+cbor','application/senml-etch+json','application/senml-exi',\
        'application/senml+cbor','application/senml+json','application/senml+xml','application/sensml-exi','application/sensml+cbor','application/sensml+json','application/sensml+xml','application/sep-exi','application/sep+xml','application/session-info','application/set-payment',\
        'application/set-payment-initiation','application/set-registration','application/set-registration-initiation','application/SGML','application/sgml-open-catalog','application/shf+xml','application/sieve','application/simple-filter+xml','application/simple-message-summary',\
        'application/simpleSymbolContainer','application/sipc','application/slate','application/smil','application/smil+xml','application/smpte336m','application/soap+fastinfoset','application/soap+xml','application/sparql-query','application/spdx+json','application/sparql-results+xml',\
        'application/spirits-event+xml','application/sql','application/srgs','application/srgs+xml','application/sru+xml','application/ssml+xml','application/stix+json','application/swid+cbor','application/swid+xml','application/tamp-apex-update','application/tamp-apex-update-confirm',\
        'application/tamp-community-update','application/tamp-community-update-confirm','application/tamp-error','application/tamp-sequence-adjust','application/tamp-sequence-adjust-confirm','application/tamp-status-query','application/tamp-status-response','application/tamp-update',\
        'application/tamp-update-confirm','application/taxii+json','application/td+json','application/tei+xml','application/TETRA_ISI','application/thraud+xml','application/timestamp-query','application/timestamp-reply','application/timestamped-data','application/tlsrpt+gzip',\
        'application/tlsrpt+json','application/tm+json','application/tnauthlist','application/token-introspection+jwt','application/trickle-ice-sdpfrag','application/trig','application/ttml+xml','application/tve-trigger','application/tzif','application/tzif-leap','application/ulpfec',\
        'application/urc-grpsheet+xml','application/urc-ressheet+xml','application/urc-targetdesc+xml','application/urc-uisocketdesc+xml','application/vcard+json','application/vcard+xml','application/vemmi','application/vnd.1000minds.decision-model+xml','application/vnd.1ob',\
        'application/vnd.3gpp.5gnas','application/vnd.3gpp.access-transfer-events+xml','application/vnd.3gpp.bsf+xml','application/vnd.3gpp.crs+xml','application/vnd.3gpp.current-location-discovery+xml','application/vnd.3gpp.GMOP+xml','application/vnd.3gpp.gtpc','application/vnd.3gpp.interworking-data',\
        'application/vnd.3gpp.lpp','application/vnd.3gpp.mc-signalling-ear','application/vnd.3gpp.mcdata-affiliation-command+xml','application/vnd.3gpp.mcdata-info+xml','application/vnd.3gpp.mcdata-msgstore-ctrl-request+xml','application/vnd.3gpp.mcdata-payload','application/vnd.3gpp.mcdata-regroup+xml',\
        'application/vnd.3gpp.mcdata-service-config+xml','application/vnd.3gpp.mcdata-signalling','application/vnd.3gpp.mcdata-ue-config+xml','application/vnd.3gpp.mcdata-user-profile+xml','application/vnd.3gpp.mcptt-affiliation-command+xml','application/vnd.3gpp.mcptt-floor-request+xml','application/vnd.3gpp.mcptt-info+xml',\
        'application/vnd.3gpp.mcptt-location-info+xml','application/vnd.3gpp.mcptt-mbms-usage-info+xml','application/vnd.3gpp.mcptt-regroup+xml','application/vnd.3gpp.mcptt-service-config+xml','application/vnd.3gpp.mcptt-signed+xml','application/vnd.3gpp.mcptt-ue-config+xml','application/vnd.3gpp.mcptt-ue-init-config+xml',\
        'application/vnd.3gpp.mcptt-user-profile+xml','application/vnd.3gpp.mcvideo-affiliation-command+xml','application/vnd.3gpp.mcvideo-affiliation-info+xml','application/vnd.3gpp.mcvideo-info+xml','application/vnd.3gpp.mcvideo-location-info+xml','application/vnd.3gpp.mcvideo-mbms-usage-info+xml',\
        'application/vnd.3gpp.mcvideo-regroup+xml','application/vnd.3gpp.mcvideo-service-config+xml','application/vnd.3gpp.mcvideo-transmission-request+xml','application/vnd.3gpp.mcvideo-ue-config+xml','application/vnd.3gpp.mcvideo-user-profile+xml','application/vnd.3gpp.mid-call+xml','application/vnd.3gpp.ngap',\
        'application/vnd.3gpp.pfcp','application/vnd.3gpp.pic-bw-large','application/vnd.3gpp.pic-bw-small','application/vnd.3gpp.pic-bw-var','application/vnd.3gpp-prose-pc3a+xml','application/vnd.3gpp-prose-pc3ach+xml','application/vnd.3gpp-prose-pc3ch+xml','application/vnd.3gpp-prose-pc8+xml','application/vnd.3gpp-prose+xml',\
        'application/vnd.3gpp.s1ap','application/vnd.3gpp.seal-group-doc+xml','application/vnd.3gpp.seal-info+xml','application/vnd.3gpp.seal-location-info+xml','application/vnd.3gpp.seal-mbms-usage-info+xml','application/vnd.3gpp.seal-network-QoS-management-info+xml','application/vnd.3gpp.seal-ue-config-info+xml',\
        'application/vnd.3gpp.seal-unicast-info+xml','application/vnd.3gpp.seal-user-profile-info+xml','application/vnd.3gpp.sms','application/vnd.3gpp.sms+xml','application/vnd.3gpp.srvcc-ext+xml','application/vnd.3gpp.SRVCC-info+xml','application/vnd.3gpp.state-and-event-info+xml','application/vnd.3gpp.ussd+xml',\
        'application/vnd.3gpp.vae-info+xml','application/vnd.3gpp-v2x-local-service-information','application/vnd.3gpp2.bcmcsinfo+xml','application/vnd.3gpp2.sms','application/vnd.3gpp2.tcap','application/vnd.3gpp.v2x','application/vnd.3lightssoftware.imagescal','application/vnd.3M.Post-it-Notes','application/vnd.accpac.simply.aso',\
        'application/vnd.accpac.simply.imp','application/vnd.acm.addressxfer+json','application/vnd.acm.chatbot+json','application/vnd.acucobol','application/vnd.acucorp','application/vnd.adobe.flash.movie','application/vnd.adobe.formscentral.fcdt','application/vnd.adobe.fxp','application/vnd.adobe.partial-upload',\
        'application/vnd.adobe.xdp+xml','application/vnd.aether.imp','application/vnd.afpc.afplinedata','application/vnd.afpc.afplinedata-pagedef','application/vnd.afpc.cmoca-cmresource','application/vnd.afpc.foca-charset','application/vnd.afpc.foca-codedfont','application/vnd.afpc.foca-codepage','application/vnd.afpc.modca',\
        'application/vnd.afpc.modca-cmtable','application/vnd.afpc.modca-formdef','application/vnd.afpc.modca-mediummap','application/vnd.afpc.modca-objectcontainer','application/vnd.afpc.modca-overlay','application/vnd.afpc.modca-pagesegment','application/vnd.age','application/vnd.ah-barcode','application/vnd.ahead.space',\
        'application/vnd.airzip.filesecure.azf','application/vnd.airzip.filesecure.azs','application/vnd.amadeus+json','application/vnd.amazon.mobi8-ebook','application/vnd.americandynamics.acc','application/vnd.amiga.ami','application/vnd.amundsen.maze+xml','application/vnd.android.ota','application/vnd.anki',\
        'application/vnd.anser-web-certificate-issue-initiation','application/vnd.antix.game-component','application/vnd.apache.arrow.file','application/vnd.apache.arrow.stream','application/vnd.apache.thrift.binary','application/vnd.apache.thrift.compact','application/vnd.apache.thrift.json','application/vnd.apexlang',\
        'application/vnd.api+json','application/vnd.aplextor.warrp+json','application/vnd.apothekende.reservation+json','application/vnd.apple.installer+xml','application/vnd.apple.keynote','application/vnd.apple.mpegurl','application/vnd.apple.numbers','application/vnd.apple.pages','application/vnd.arastra.swi',\
        'application/vnd.aristanetworks.swi','application/vnd.artisan+json','application/vnd.artsquare','application/vnd.astraea-software.iota','application/vnd.audiograph','application/vnd.autopackage','application/vnd.avalon+json','application/vnd.avistar+xml','application/vnd.balsamiq.bmml+xml','application/vnd.banana-accounting',\
        'application/vnd.bbf.usp.error','application/vnd.bbf.usp.msg','application/vnd.bbf.usp.msg+json','application/vnd.balsamiq.bmpr','application/vnd.bekitzur-stech+json','application/vnd.belightsoft.lhzd+zip','application/vnd.belightsoft.lhzl+zip','application/vnd.bint.med-content','application/vnd.biopax.rdf+xml',\
        'application/vnd.blink-idb-value-wrapper','application/vnd.blueice.multipass','application/vnd.bluetooth.ep.oob','application/vnd.bluetooth.le.oob','application/vnd.bmi','application/vnd.bpf','application/vnd.bpf3','application/vnd.businessobjects','application/vnd.byu.uapi+json','application/vnd.bzip3','application/vnd.cab-jscript',\
        'application/vnd.canon-cpdl','application/vnd.canon-lips','application/vnd.capasystems-pg+json','application/vnd.cendio.thinlinc.clientconf','application/vnd.century-systems.tcp_stream','application/vnd.chemdraw+xml','application/vnd.chess-pgn','application/vnd.chipnuts.karaoke-mmd','application/vnd.ciedi','application/vnd.cinderella',\
        'application/vnd.cirpack.isdn-ext','application/vnd.citationstyles.style+xml','application/vnd.claymore','application/vnd.cloanto.rp9','application/vnd.clonk.c4group','application/vnd.cluetrust.cartomobile-config','application/vnd.cluetrust.cartomobile-config-pkg','application/vnd.cncf.helm.chart.content.v1.tar+gzip',\
        'application/vnd.cncf.helm.chart.provenance.v1.prov','application/vnd.cncf.helm.config.v1+json','application/vnd.coffeescript','application/vnd.collabio.xodocuments.document','application/vnd.collabio.xodocuments.document-template','application/vnd.collabio.xodocuments.presentation','application/vnd.collabio.xodocuments.presentation-template',\
        'application/vnd.collabio.xodocuments.spreadsheet','application/vnd.collabio.xodocuments.spreadsheet-template','application/vnd.collection.doc+json','application/vnd.collection+json','application/vnd.collection.next+json','application/vnd.comicbook-rar','application/vnd.comicbook+zip','application/vnd.commerce-battelle','application/vnd.commonspace',\
        'application/vnd.coreos.ignition+json','application/vnd.cosmocaller','application/vnd.contact.cmsg','application/vnd.crick.clicker','application/vnd.crick.clicker.keyboard','application/vnd.crick.clicker.palette','application/vnd.crick.clicker.template','application/vnd.crick.clicker.wordbank','application/vnd.criticaltools.wbs+xml',\
        'application/vnd.cryptii.pipe+json','application/vnd.crypto-shade-file','application/vnd.cryptomator.encrypted','application/vnd.cryptomator.vault','application/vnd.ctc-posml','application/vnd.ctct.ws+xml','application/vnd.cups-pdf','application/vnd.cups-postscript','application/vnd.cups-ppd','application/vnd.cups-raster','application/vnd.cups-raw',\
        'application/vnd.curl','application/vnd.cyan.dean.root+xml','application/vnd.cybank','application/vnd.cyclonedx+json','application/vnd.cyclonedx+xml','application/vnd.d2l.coursepackage1p0+zip','application/vnd.d3m-dataset','application/vnd.d3m-problem','application/vnd.dart','application/vnd.data-vision.rdz','application/vnd.datalog',\
        'application/vnd.datapackage+json','application/vnd.dataresource+json','application/vnd.dbf','application/vnd.debian.binary-package','application/vnd.dece.data','application/vnd.dece.ttml+xml','application/vnd.dece.unspecified','application/vnd.dece.zip','application/vnd.denovo.fcselayout-link','application/vnd.desmume.movie',\
        'application/vnd.dir-bi.plate-dl-nosuffix','application/vnd.dm.delegation+xml','application/vnd.dna','application/vnd.document+json','application/vnd.dolby.mobile.1','application/vnd.dolby.mobile.2','application/vnd.doremir.scorecloud-binary-document','application/vnd.dpgraph','application/vnd.dreamfactory','application/vnd.drive+json',\
        'application/vnd.dtg.local','application/vnd.dtg.local.flash','application/vnd.dtg.local.html','application/vnd.dvb.ait','application/vnd.dvb.dvbisl+xml','application/vnd.dvb.dvbj','application/vnd.dvb.esgcontainer','application/vnd.dvb.ipdcdftnotifaccess','application/vnd.dvb.ipdcesgaccess','application/vnd.dvb.ipdcesgaccess2',\
        'application/vnd.dvb.ipdcesgpdd','application/vnd.dvb.ipdcroaming','application/vnd.dvb.iptv.alfec-base','application/vnd.dvb.iptv.alfec-enhancement','application/vnd.dvb.notif-aggregate-root+xml','application/vnd.dvb.notif-container+xml','application/vnd.dvb.notif-generic+xml','application/vnd.dvb.notif-ia-msglist+xml',\
        'application/vnd.dvb.notif-ia-registration-request+xml','application/vnd.dvb.notif-ia-registration-response+xml','application/vnd.dvb.notif-init+xml','application/vnd.dvb.pfr','application/vnd.dvb.service','application/vnd.dxr','application/vnd.dynageo','application/vnd.dzr','application/vnd.easykaraoke.cdgdownload','application/vnd.ecip.rlp',\
        'application/vnd.ecdis-update','application/vnd.eclipse.ditto+json','application/vnd.ecowin.chart','application/vnd.ecowin.filerequest','application/vnd.ecowin.fileupdate','application/vnd.ecowin.series','application/vnd.ecowin.seriesrequest','application/vnd.ecowin.seriesupdate','application/vnd.efi.img','application/vnd.efi.iso','application/vnd.eln+zip',\
        'application/vnd.emclient.accessrequest+xml','application/vnd.enliven','application/vnd.enphase.envoy','application/vnd.eprints.data+xml','application/vnd.epson.esf','application/vnd.epson.msf','application/vnd.epson.quickanime','application/vnd.epson.salt','application/vnd.epson.ssf','application/vnd.ericsson.quickcall','application/vnd.espass-espass+zip',\
        'application/vnd.eszigno3+xml','application/vnd.etsi.aoc+xml','application/vnd.etsi.asic-s+zip','application/vnd.etsi.asic-e+zip','application/vnd.etsi.cug+xml','application/vnd.etsi.iptvcommand+xml','application/vnd.etsi.iptvdiscovery+xml','application/vnd.etsi.iptvprofile+xml','application/vnd.etsi.iptvsad-bc+xml','application/vnd.etsi.iptvsad-cod+xml',\
        'application/vnd.etsi.iptvsad-npvr+xml','application/vnd.etsi.iptvservice+xml','application/vnd.etsi.iptvsync+xml','application/vnd.etsi.iptvueprofile+xml','application/vnd.etsi.mcid+xml','application/vnd.etsi.mheg5','application/vnd.etsi.overload-control-policy-dataset+xml','application/vnd.etsi.pstn+xml','application/vnd.etsi.sci+xml',\
        'application/vnd.etsi.simservs+xml','application/vnd.etsi.timestamp-token','application/vnd.etsi.tsl+xml','application/vnd.etsi.tsl.der','application/vnd.eu.kasparian.car+json','application/vnd.eudora.data','application/vnd.evolv.ecig.profile','application/vnd.evolv.ecig.settings','application/vnd.evolv.ecig.theme','application/vnd.exstream-empower+zip',\
        'application/vnd.exstream-package','application/vnd.ezpix-album','application/vnd.ezpix-package','application/vnd.f-secure.mobile','application/vnd.fastcopy-disk-image','application/vnd.familysearch.gedcom+zip','application/vnd.fdsn.mseed','application/vnd.fdsn.seed','application/vnd.ffsns','application/vnd.ficlab.flb+zip','application/vnd.filmit.zfc',\
        'application/vnd.fints','application/vnd.firemonkeys.cloudcell','application/vnd.FloGraphIt','application/vnd.fluxtime.clip','application/vnd.font-fontforge-sfd','application/vnd.framemaker','application/vnd.freelog.comic','application/vnd.frogans.fnc','application/vnd.frogans.ltf','application/vnd.fsc.weblaunch','application/vnd.fujifilm.fb.docuworks',\
        'application/vnd.fujifilm.fb.docuworks.binder','application/vnd.fujifilm.fb.docuworks.container','application/vnd.fujifilm.fb.jfi+xml','application/vnd.fujitsu.oasys','application/vnd.fujitsu.oasys2','application/vnd.fujitsu.oasys3','application/vnd.fujitsu.oasysgp','application/vnd.fujitsu.oasysprs','application/vnd.fujixerox.ART4',\
        'application/vnd.fujixerox.ART-EX','application/vnd.fujixerox.ddd','application/vnd.fujixerox.docuworks','application/vnd.fujixerox.docuworks.binder','application/vnd.fujixerox.docuworks.container','application/vnd.fujixerox.HBPL','application/vnd.fut-misnet','application/vnd.futoin+cbor','application/vnd.futoin+json','application/vnd.fuzzysheet',\
        'application/vnd.genomatix.tuxedo','application/vnd.genozip','application/vnd.gentics.grd+json','application/vnd.gentoo.catmetadata+xml','application/vnd.gentoo.ebuild','application/vnd.gentoo.eclass','application/vnd.gentoo.gpkg','application/vnd.gentoo.manifest','application/vnd.gentoo.xpak','application/vnd.gentoo.pkgmetadata+xml',\
        'application/vnd.geo+json','application/vnd.geocube+xml','application/vnd.geogebra.file','application/vnd.geogebra.slides','application/vnd.geogebra.tool','application/vnd.geometry-explorer','application/vnd.geonext','application/vnd.geoplan','application/vnd.geospace','application/vnd.gerber','application/vnd.globalplatform.card-content-mgt',\
        'application/vnd.globalplatform.card-content-mgt-response','application/vnd.gmx','application/vnd.gnu.taler.exchange+json','application/vnd.gnu.taler.merchant+json','application/vnd.google-earth.kml+xml','application/vnd.google-earth.kmz','application/vnd.gov.sk.e-form+xml','application/vnd.gov.sk.e-form+zip','application/vnd.gov.sk.xmldatacontainer+xml',\
        'application/vnd.gpxsee.map+xml','application/vnd.grafeq','application/vnd.gridmp','application/vnd.groove-account','application/vnd.groove-help','application/vnd.groove-identity-message','application/vnd.groove-injector','application/vnd.groove-tool-message','application/vnd.groove-tool-template','application/vnd.groove-vcard','application/vnd.hal+json',\
        'application/vnd.hal+xml','application/vnd.HandHeld-Entertainment+xml','application/vnd.hbci','application/vnd.hc+json','application/vnd.hcl-bireports','application/vnd.hdt','application/vnd.heroku+json','application/vnd.hhe.lesson-player','application/vnd.hp-HPGL','application/vnd.hp-hpid','application/vnd.hp-hps','application/vnd.hp-jlyt','application/vnd.hp-PCL',\
        'application/vnd.hp-PCLXL','application/vnd.hsl','application/vnd.httphone','application/vnd.hydrostatix.sof-data','application/vnd.hyper-item+json','application/vnd.hyper+json','application/vnd.hyperdrive+json','application/vnd.hzn-3d-crossword','application/vnd.ibm.afplinedata','application/vnd.ibm.electronic-media','application/vnd.ibm.MiniPay',\
        'application/vnd.ibm.modcap','application/vnd.ibm.rights-management','application/vnd.ibm.secure-container','application/vnd.iccprofile','application/vnd.ieee.1905','application/vnd.igloader','application/vnd.imagemeter.folder+zip','application/vnd.imagemeter.image+zip','application/vnd.immervision-ivp','application/vnd.immervision-ivu',\
        'application/vnd.ims.imsccv1p1','application/vnd.ims.imsccv1p2','application/vnd.ims.imsccv1p3','application/vnd.ims.lis.v2.result+json','application/vnd.ims.lti.v2.toolconsumerprofile+json','application/vnd.ims.lti.v2.toolproxy.id+json','application/vnd.ims.lti.v2.toolproxy+json','application/vnd.ims.lti.v2.toolsettings+json',\
        'application/vnd.ims.lti.v2.toolsettings.simple+json','application/vnd.informedcontrol.rms+xml','application/vnd.infotech.project','application/vnd.infotech.project+xml','application/vnd.informix-visionary','application/vnd.innopath.wamp.notification','application/vnd.insors.igm','application/vnd.intercon.formnet','application/vnd.intergeo',\
        'application/vnd.intertrust.digibox','application/vnd.intertrust.nncp','application/vnd.intu.qbo','application/vnd.intu.qfx','application/vnd.ipfs.ipns-record','application/vnd.ipld.car','application/vnd.ipld.dag-cbor','application/vnd.ipld.dag-json','application/vnd.ipld.raw','application/vnd.iptc.g2.catalogitem+xml','application/vnd.iptc.g2.conceptitem+xml',\
        'application/vnd.iptc.g2.knowledgeitem+xml','application/vnd.iptc.g2.newsitem+xml','application/vnd.iptc.g2.newsmessage+xml','application/vnd.iptc.g2.packageitem+xml','application/vnd.iptc.g2.planningitem+xml','application/vnd.ipunplugged.rcprofile','application/vnd.irepository.package+xml','application/vnd.is-xpr','application/vnd.isac.fcs','application/vnd.jam',\
        'application/vnd.iso11783-10+zip','application/vnd.japannet-directory-service','application/vnd.japannet-jpnstore-wakeup','application/vnd.japannet-payment-wakeup','application/vnd.japannet-registration','application/vnd.japannet-registration-wakeup','application/vnd.japannet-setstore-wakeup','application/vnd.japannet-verification','application/vnd.japannet-verification-wakeup',\
        'application/vnd.jcp.javame.midlet-rms','application/vnd.jisp','application/vnd.joost.joda-archive','application/vnd.jsk.isdn-ngn','application/vnd.kahootz','application/vnd.kde.karbon','application/vnd.kde.kchart','application/vnd.kde.kformula','application/vnd.kde.kivio','application/vnd.kde.kontour','application/vnd.kde.kpresenter','application/vnd.kde.kspread',\
        'application/vnd.kde.kword','application/vnd.kenameaapp','application/vnd.kidspiration','application/vnd.Kinar','application/vnd.koan','application/vnd.kodak-descriptor','application/vnd.las','application/vnd.las.las+json','application/vnd.las.las+xml','application/vnd.laszip','application/vnd.leap+json','application/vnd.liberty-request+xml',\
        'application/vnd.llamagraphics.life-balance.desktop','application/vnd.llamagraphics.life-balance.exchange+xml','application/vnd.logipipe.circuit+zip','application/vnd.loom','application/vnd.lotus-1-2-3','application/vnd.lotus-approach','application/vnd.lotus-freelance','application/vnd.lotus-notes','application/vnd.lotus-organizer','application/vnd.lotus-screencam',\
        'application/vnd.lotus-wordpro','application/vnd.macports.portpkg','application/vnd.mapbox-vector-tile','application/vnd.marlin.drm.actiontoken+xml','application/vnd.marlin.drm.conftoken+xml','application/vnd.marlin.drm.license+xml','application/vnd.marlin.drm.mdcf','application/vnd.mason+json','application/vnd.maxar.archive.3tz+zip','application/vnd.maxmind.maxmind-db',\
        'application/vnd.mcd','application/vnd.mdl','application/vnd.mdl-mbsdf','application/vnd.medcalcdata','application/vnd.mediastation.cdkey','application/vnd.medicalholodeck.recordxr','application/vnd.meridian-slingshot','application/vnd.mermaid','application/vnd.MFER','application/vnd.mfmp','application/vnd.micro+json','application/vnd.micrografx.flo','application/vnd.micrografx.igx',\
        'application/vnd.microsoft.portable-executable','application/vnd.microsoft.windows.thumbnail-cache','application/vnd.miele+json','application/vnd.mif','application/vnd.minisoft-hp3000-save','application/vnd.mitsubishi.misty-guard.trustweb','application/vnd.Mobius.DAF','application/vnd.Mobius.DIS','application/vnd.Mobius.MBK','application/vnd.Mobius.MQY','application/vnd.Mobius.MSL',\
        'application/vnd.Mobius.PLC','application/vnd.Mobius.TXF','application/vnd.modl','application/vnd.mophun.application','application/vnd.mophun.certificate','application/vnd.motorola.flexsuite','application/vnd.motorola.flexsuite.adsi','application/vnd.motorola.flexsuite.fis','application/vnd.motorola.flexsuite.gotap','application/vnd.motorola.flexsuite.kmr',\
        'application/vnd.motorola.flexsuite.ttc','application/vnd.motorola.flexsuite.wem','application/vnd.motorola.iprm','application/vnd.mozilla.xul+xml','application/vnd.ms-artgalry','application/vnd.ms-asf','application/vnd.ms-cab-compressed','application/vnd.ms-3mfdocument','application/vnd.ms-excel','application/vnd.ms-excel.addin.macroEnabled.12',\
        'application/vnd.ms-excel.sheet.binary.macroEnabled.12','application/vnd.ms-excel.sheet.macroEnabled.12','application/vnd.ms-excel.template.macroEnabled.12','application/vnd.ms-fontobject','application/vnd.ms-htmlhelp','application/vnd.ms-ims','application/vnd.ms-lrm','application/vnd.ms-office.activeX+xml','application/vnd.ms-officetheme','application/vnd.ms-playready.initiator+xml',\
        'application/vnd.ms-powerpoint','application/vnd.ms-powerpoint.addin.macroEnabled.12','application/vnd.ms-powerpoint.presentation.macroEnabled.12','application/vnd.ms-powerpoint.slide.macroEnabled.12','application/vnd.ms-powerpoint.slideshow.macroEnabled.12','application/vnd.ms-powerpoint.template.macroEnabled.12','application/vnd.ms-PrintDeviceCapabilities+xml',\
        'application/vnd.ms-PrintSchemaTicket+xml','application/vnd.ms-project','application/vnd.ms-tnef','application/vnd.ms-windows.devicepairing','application/vnd.ms-windows.nwprinting.oob','application/vnd.ms-windows.printerpairing','application/vnd.ms-windows.wsd.oob','application/vnd.ms-wmdrm.lic-chlg-req','application/vnd.ms-wmdrm.lic-resp','application/vnd.ms-wmdrm.meter-chlg-req',\
        'application/vnd.ms-wmdrm.meter-resp','application/vnd.ms-word.document.macroEnabled.12','application/vnd.ms-word.template.macroEnabled.12','application/vnd.ms-works','application/vnd.ms-wpl','application/vnd.ms-xpsdocument','application/vnd.msa-disk-image','application/vnd.mseq','application/vnd.msign','application/vnd.multiad.creator','application/vnd.multiad.creator.cif',\
        'application/vnd.musician','application/vnd.music-niff','application/vnd.muvee.style','application/vnd.mynfc','application/vnd.nacamar.ybrid+json','application/vnd.ncd.control','application/vnd.ncd.reference','application/vnd.nearst.inv+json','application/vnd.nebumind.line','application/vnd.nervana','application/vnd.netfpx','application/vnd.neurolanguage.nlu','application/vnd.nimn',\
        'application/vnd.nintendo.snes.rom','application/vnd.nintendo.nitro.rom','application/vnd.nitf','application/vnd.noblenet-directory','application/vnd.noblenet-sealer','application/vnd.noblenet-web','application/vnd.nokia.catalogs','application/vnd.nokia.conml+wbxml','application/vnd.nokia.conml+xml','application/vnd.nokia.iptv.config+xml','application/vnd.nokia.iSDS-radio-presets',\
        'application/vnd.nokia.landmark+wbxml','application/vnd.nokia.landmark+xml','application/vnd.nokia.landmarkcollection+xml','application/vnd.nokia.ncd','application/vnd.nokia.n-gage.ac+xml','application/vnd.nokia.n-gage.data','application/vnd.nokia.n-gage.symbian.install','application/vnd.nokia.pcd+wbxml','application/vnd.nokia.pcd+xml','application/vnd.nokia.radio-preset',\
        'application/vnd.nokia.radio-presets','application/vnd.novadigm.EDM','application/vnd.novadigm.EDX','application/vnd.novadigm.EXT','application/vnd.ntt-local.content-share','application/vnd.ntt-local.file-transfer','application/vnd.ntt-local.ogw_remote-access','application/vnd.ntt-local.sip-ta_remote','application/vnd.ntt-local.sip-ta_tcp_stream',\
        'application/vnd.oasis.opendocument.base','application/vnd.oasis.opendocument.chart','application/vnd.oasis.opendocument.chart-template','application/vnd.oasis.opendocument.database','application/vnd.oasis.opendocument.formula','application/vnd.oasis.opendocument.formula-template','application/vnd.oasis.opendocument.graphics','application/vnd.oasis.opendocument.graphics-template',\
        'application/vnd.oasis.opendocument.image','application/vnd.oasis.opendocument.image-template','application/vnd.oasis.opendocument.presentation','application/vnd.oasis.opendocument.presentation-template','application/vnd.oasis.opendocument.spreadsheet','application/vnd.oasis.opendocument.spreadsheet-template','application/vnd.oasis.opendocument.text',\
        'application/vnd.oasis.opendocument.text-master','application/vnd.oasis.opendocument.text-master-template','application/vnd.oasis.opendocument.text-template','application/vnd.oasis.opendocument.text-web','application/vnd.obn','application/vnd.ocf+cbor','application/vnd.oci.image.manifest.v1+json','application/vnd.oftn.l10n+json','application/vnd.oipf.contentaccessdownload+xml',\
        'application/vnd.oipf.contentaccessstreaming+xml','application/vnd.oipf.cspg-hexbinary','application/vnd.oipf.dae.svg+xml','application/vnd.oipf.dae.xhtml+xml','application/vnd.oipf.mippvcontrolmessage+xml','application/vnd.oipf.pae.gem','application/vnd.oipf.spdiscovery+xml','application/vnd.oipf.spdlist+xml','application/vnd.oipf.ueprofile+xml','application/vnd.oipf.userprofile+xml',\
        'application/vnd.olpc-sugar','application/vnd.oma.bcast.associated-procedure-parameter+xml','application/vnd.oma.bcast.drm-trigger+xml','application/vnd.oma.bcast.imd+xml','application/vnd.oma.bcast.ltkm','application/vnd.oma.bcast.notification+xml','application/vnd.oma.bcast.provisioningtrigger','application/vnd.oma.bcast.sgboot','application/vnd.oma.bcast.sgdd+xml',\
        'application/vnd.oma.bcast.sgdu','application/vnd.oma.bcast.simple-symbol-container','application/vnd.oma.bcast.smartcard-trigger+xml','application/vnd.oma.bcast.sprov+xml','application/vnd.oma.bcast.stkm','application/vnd.oma.cab-address-book+xml','application/vnd.oma.cab-feature-handler+xml','application/vnd.oma.cab-pcc+xml','application/vnd.oma.cab-subs-invite+xml',\
        'application/vnd.oma.cab-user-prefs+xml','application/vnd.oma.dcd','application/vnd.oma.dcdc','application/vnd.oma.dd2+xml','application/vnd.oma.drm.risd+xml','application/vnd.oma.group-usage-list+xml','application/vnd.oma.lwm2m+cbor','application/vnd.oma.lwm2m+json','application/vnd.oma.lwm2m+tlv','application/vnd.oma.pal+xml','application/vnd.oma.poc.detailed-progress-report+xml',\
        'application/vnd.oma.poc.final-report+xml','application/vnd.oma.poc.groups+xml','application/vnd.oma.poc.invocation-descriptor+xml','application/vnd.oma.poc.optimized-progress-report+xml','application/vnd.oma.push','application/vnd.oma.scidm.messages+xml','application/vnd.oma.xcap-directory+xml','application/vnd.omads-email+xml','application/vnd.omads-file+xml',\
        'application/vnd.omads-folder+xml','application/vnd.omaloc-supl-init','application/vnd.oma-scws-config','application/vnd.oma-scws-http-request','application/vnd.oma-scws-http-response','application/vnd.onepager','application/vnd.onepagertamp','application/vnd.onepagertamx','application/vnd.onepagertat','application/vnd.onepagertatp','application/vnd.onepagertatx',\
        'application/vnd.onvif.metadata','application/vnd.openblox.game-binary','application/vnd.openblox.game+xml','application/vnd.openeye.oeb','application/vnd.openstreetmap.data+xml','application/vnd.opentimestamps.ots','application/vnd.openxmlformats-officedocument.custom-properties+xml','application/vnd.openxmlformats-officedocument.customXmlProperties+xml',\
        'application/vnd.openxmlformats-officedocument.drawing+xml','application/vnd.openxmlformats-officedocument.drawingml.chart+xml','application/vnd.openxmlformats-officedocument.drawingml.chartshapes+xml','application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml','application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml',\
        'application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml','application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml','application/vnd.openxmlformats-officedocument.extended-properties+xml','application/vnd.openxmlformats-officedocument.presentationml.commentAuthors+xml','application/vnd.openxmlformats-officedocument.presentationml.comments+xml',\
        'application/vnd.openxmlformats-officedocument.presentationml.handoutMaster+xml','application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml','application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml','application/vnd.openxmlformats-officedocument.presentationml.presentation','application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml',\
        'application/vnd.openxmlformats-officedocument.presentationml.presProps+xml','application/vnd.openxmlformats-officedocument.presentationml.slide','application/vnd.openxmlformats-officedocument.presentationml.slide+xml','application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml','application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml',\
        'application/vnd.openxmlformats-officedocument.presentationml.slideshow','application/vnd.openxmlformats-officedocument.presentationml.slideshow.main+xml','application/vnd.openxmlformats-officedocument.presentationml.slideUpdateInfo+xml','application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml','application/vnd.openxmlformats-officedocument.presentationml.tags+xml',\
        'application/vnd.openxmlformats-officedocument.presentationml.template','application/vnd.openxmlformats-officedocument.presentationml.template.main+xml','application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.calcChain+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.chartsheet+xml',\
        'application/vnd.openxmlformats-officedocument.spreadsheetml.comments+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.connections+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.dialogsheet+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.externalLink+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.pivotCacheDefinition+xml',\
        'application/vnd.openxmlformats-officedocument.spreadsheetml.pivotCacheRecords+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.pivotTable+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.queryTable+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.revisionHeaders+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.revisionLog+xml',\
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.sheetMetadata+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml',\
        'application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.tableSingleCells+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.template','application/vnd.openxmlformats-officedocument.spreadsheetml.template.main+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.userNames+xml',\
        'application/vnd.openxmlformats-officedocument.spreadsheetml.volatileDependencies+xml','application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml','application/vnd.openxmlformats-officedocument.theme+xml','application/vnd.openxmlformats-officedocument.themeOverride+xml','application/vnd.openxmlformats-officedocument.vmlDrawing',\
        'application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml','application/vnd.openxmlformats-officedocument.wordprocessingml.document','application/vnd.openxmlformats-officedocument.wordprocessingml.document.glossary+xml','application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml','application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml',\
        'application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml','application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml','application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml','application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml','application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml',\
        'application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml','application/vnd.openxmlformats-officedocument.wordprocessingml.template','application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml','application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml','application/vnd.openxmlformats-package.core-properties+xml',\
        'application/vnd.openxmlformats-package.digital-signature-xmlsignature+xml','application/vnd.openxmlformats-package.relationships+xml','application/vnd.oracle.resource+json','application/vnd.orange.indata','application/vnd.osa.netdeploy','application/vnd.osgeo.mapguide.package','application/vnd.osgi.bundle','application/vnd.osgi.dp','application/vnd.osgi.subsystem','application/vnd.otps.ct-kip+xml',\
        'application/vnd.oxli.countgraph','application/vnd.pagerduty+json','application/vnd.palm','application/vnd.panoply','application/vnd.paos.xml','application/vnd.patentdive','application/vnd.patientecommsdoc','application/vnd.pawaafile','application/vnd.pcos','application/vnd.pg.format','application/vnd.pg.osasli','application/vnd.piaccess.application-licence','application/vnd.picsel','application/vnd.pmi.widget',\
        'application/vnd.poc.group-advertisement+xml','application/vnd.pocketlearn','application/vnd.powerbuilder6','application/vnd.powerbuilder6-s','application/vnd.powerbuilder7','application/vnd.powerbuilder75','application/vnd.powerbuilder75-s','application/vnd.powerbuilder7-s','application/vnd.preminet','application/vnd.previewsystems.box','application/vnd.proteus.magazine','application/vnd.psfs',\
        'application/vnd.pt.mundusmundi','application/vnd.publishare-delta-tree','application/vnd.pvi.ptid1','application/vnd.pwg-multiplexed','application/vnd.pwg-xhtml-print+xml','application/vnd.qualcomm.brew-app-res','application/vnd.quarantainenet','application/vnd.Quark.QuarkXPress','application/vnd.quobject-quoxdocument','application/vnd.radisys.moml+xml','application/vnd.radisys.msml-audit-conf+xml',\
        'application/vnd.radisys.msml-audit-conn+xml','application/vnd.radisys.msml-audit-dialog+xml','application/vnd.radisys.msml-audit-stream+xml','application/vnd.radisys.msml-audit+xml','application/vnd.radisys.msml-conf+xml','application/vnd.radisys.msml-dialog-base+xml','application/vnd.radisys.msml-dialog-fax-detect+xml','application/vnd.radisys.msml-dialog-fax-sendrecv+xml',\
        'application/vnd.radisys.msml-dialog-group+xml','application/vnd.radisys.msml-dialog-speech+xml','application/vnd.radisys.msml-dialog-transform+xml','application/vnd.radisys.msml-dialog+xml','application/vnd.radisys.msml+xml','application/vnd.rainstor.data','application/vnd.rapid','application/vnd.rar','application/vnd.realvnc.bed','application/vnd.recordare.musicxml','application/vnd.recordare.musicxml+xml',\
        'application/vnd.relpipe','application/vnd.RenLearn.rlprint','application/vnd.resilient.logic','application/vnd.restful+json','application/vnd.rig.cryptonote','application/vnd.route66.link66+xml','application/vnd.rs-274x','application/vnd.ruckus.download','application/vnd.s3sms','application/vnd.sailingtracker.track','application/vnd.sar','application/vnd.sbm.cid','application/vnd.sbm.mid2','application/vnd.scribus',\
        'application/vnd.sealed.3df','application/vnd.sealed.csf','application/vnd.sealed.doc','application/vnd.sealed.eml','application/vnd.sealed.mht','application/vnd.sealed.net','application/vnd.sealed.ppt','application/vnd.sealed.tiff','application/vnd.sealed.xls','application/vnd.sealedmedia.softseal.html','application/vnd.sealedmedia.softseal.pdf','application/vnd.seemail','application/vnd.seis+json','application/vnd.sema',\
        'application/vnd.semd','application/vnd.semf','application/vnd.shade-save-file','application/vnd.shana.informed.formdata','application/vnd.shana.informed.formtemplate','application/vnd.shana.informed.interchange','application/vnd.shana.informed.package','application/vnd.shootproof+json','application/vnd.shopkick+json','application/vnd.shp','application/vnd.shx','application/vnd.sigrok.session',\
        'application/vnd.SimTech-MindMapper','application/vnd.siren+json','application/vnd.smaf','application/vnd.smart.notebook','application/vnd.smart.teacher','application/vnd.smintio.portals.archive','application/vnd.snesdev-page-table','application/vnd.software602.filler.form+xml','application/vnd.software602.filler.form-xml-zip','application/vnd.solent.sdkm+xml','application/vnd.spotfire.dxp','application/vnd.spotfire.sfs',\
        'application/vnd.sqlite3','application/vnd.sss-cod','application/vnd.sss-dtf','application/vnd.sss-ntf','application/vnd.stepmania.package','application/vnd.stepmania.stepchart','application/vnd.street-stream','application/vnd.sun.wadl+xml','application/vnd.sus-calendar','application/vnd.svd','application/vnd.swiftview-ics','application/vnd.sybyl.mol2','application/vnd.sycle+xml','application/vnd.syft+json',\
        'application/vnd.syncml.dm.notification','application/vnd.syncml.dmddf+xml','application/vnd.syncml.dmtnds+wbxml','application/vnd.syncml.dmtnds+xml','application/vnd.syncml.dmddf+wbxml','application/vnd.syncml.dm+wbxml','application/vnd.syncml.dm+xml','application/vnd.syncml.ds.notification','application/vnd.syncml+xml','application/vnd.tableschema+json','application/vnd.tao.intent-module-archive',\
        'application/vnd.tcpdump.pcap','application/vnd.think-cell.ppttc+json','application/vnd.tml','application/vnd.tmd.mediaflex.api+xml','application/vnd.tmobile-livetv','application/vnd.tri.onesource','application/vnd.trid.tpt','application/vnd.triscape.mxs','application/vnd.trueapp','application/vnd.truedoc','application/vnd.ubisoft.webplayer','application/vnd.ufdl','application/vnd.uiq.theme','application/vnd.umajin',\
        'application/vnd.unity','application/vnd.uoml+xml','application/vnd.uplanet.alert','application/vnd.uplanet.alert-wbxml','application/vnd.uplanet.bearer-choice','application/vnd.uplanet.bearer-choice-wbxml','application/vnd.uplanet.cacheop','application/vnd.uplanet.cacheop-wbxml','application/vnd.uplanet.channel','application/vnd.uplanet.channel-wbxml','application/vnd.uplanet.list','application/vnd.uplanet.listcmd',\
        'application/vnd.uplanet.listcmd-wbxml','application/vnd.uplanet.list-wbxml','application/vnd.uri-map','application/vnd.uplanet.signal','application/vnd.valve.source.material','application/vnd.vcx','application/vnd.vd-study','application/vnd.vectorworks','application/vnd.vel+json','application/vnd.verimatrix.vcas','application/vnd.veritone.aion+json','application/vnd.veryant.thin','application/vnd.ves.encrypted',\
        'application/vnd.vidsoft.vidconference','application/vnd.visio','application/vnd.visionary','application/vnd.vividence.scriptfile','application/vnd.vsf','application/vnd.wap.sic','application/vnd.wap.slc','application/vnd.wap.wbxml','application/vnd.wap.wmlc','application/vnd.wap.wmlscriptc','application/vnd.wasmflow.wafl','application/vnd.webturbo','application/vnd.wfa.dpp','application/vnd.wfa.p2p','application/vnd.wfa.wsc',\
        'application/vnd.windows.devicepairing','application/vnd.wmc','application/vnd.wmf.bootstrap','application/vnd.wolfram.mathematica','application/vnd.wolfram.mathematica.package','application/vnd.wolfram.player','application/vnd.wordlift','application/vnd.wordperfect','application/vnd.wqd','application/vnd.wrq-hp3000-labelled','application/vnd.wt.stf','application/vnd.wv.csp+xml','application/vnd.wv.csp+wbxml',\
        'application/vnd.wv.ssp+xml','application/vnd.xacml+json','application/vnd.xara','application/vnd.xfdl','application/vnd.xfdl.webform','application/vnd.xmi+xml','application/vnd.xmpie.cpkg','application/vnd.xmpie.dpkg','application/vnd.xmpie.plan','application/vnd.xmpie.ppkg','application/vnd.xmpie.xlim','application/vnd.zul','application/vnd.zzazz.deck+xml','application/voicexml+xml','application/voucher-cms+json',\
        'application/vq-rtcpxr','application/wasm','application/watcherinfo+xml','application/webpush-options+json','application/whoispp-query','application/whoispp-response','application/widget','application/wita','application/wordperfect5.1','application/wsdl+xml','application/wspolicy+xml','application/x-pki-message','application/x-www-form-urlencoded','application/x-x509-ca-cert','application/x-x509-ca-ra-cert',\
        'application/x-x509-next-ca-cert','application/x400-bp','application/xacml+xml','application/xcap-att+xml','application/xcap-caps+xml','application/xcap-diff+xml','application/xcap-el+xml','application/xcap-error+xml','application/xcap-ns+xml','application/xcon-conference-info-diff+xml','application/xcon-conference-info+xml','application/xenc+xml','application/xfdf','application/xhtml+xml','application/xliff+xml',\
        'application/xml','application/xml-dtd','application/xml-external-parsed-entity','application/xml-patch+xml','application/xmpp+xml','application/xop+xml','application/xslt+xml','application/xv+xml','application/yaml','application/yang','application/yang-data+cbor','application/yang-data+json','application/yang-data+xml','application/yang-patch+json','application/yang-patch+xml','application/yin+xml','application/zip','application/zlib','application/zstd',\
        'audio/1d-interleaved-parityfec','audio/32kadpcm','audio/3gpp','audio/3gpp2','audio/aac','audio/ac3','audio/AMR','audio/AMR-WB','audio/amr-wb+','audio/aptx','audio/asc','audio/ATRAC-ADVANCED-LOSSLESS','audio/ATRAC-X','audio/ATRAC3','audio/basic','audio/BV16','audio/BV32','audio/clearmode','audio/CN','audio/DAT12','audio/dls','audio/dsr-es201108','audio/dsr-es202050','audio/dsr-es202211','audio/dsr-es202212','audio/DV','audio/DVI4','audio/eac3','audio/encaprtp',\
        'audio/EVRC','audio/EVRC-QCP','audio/EVRC0','audio/EVRC1','audio/EVRCB','audio/EVRCB0','audio/EVRCB1','audio/EVRCNW','audio/EVRCNW0','audio/EVRCNW1','audio/EVRCWB','audio/EVRCWB0','audio/EVRCWB1','audio/EVS','audio/example','audio/flexfec','audio/fwdred','audio/G711-0','audio/G719','audio/G7221','audio/G722','audio/G723','audio/G726-16','audio/G726-24','audio/G726-32','audio/G726-40','audio/G728','audio/G729','audio/G7291','audio/G729D','audio/G729E','audio/GSM',\
        'audio/GSM-EFR','audio/GSM-HR-08','audio/iLBC','audio/ip-mr_v2.5','audio/L8','audio/L16','audio/L20','audio/L24','audio/LPC','audio/matroska','audio/MELP','audio/MELP600','audio/MELP1200','audio/MELP2400','audio/mhas','audio/mobile-xmf','audio/MPA','audio/mp4','audio/MP4A-LATM','audio/mpa-robust','audio/mpeg','audio/mpeg4-generic','audio/ogg','audio/opus','audio/parityfec','audio/PCMA','audio/PCMA-WB','audio/PCMU','audio/PCMU-WB','audio/prs.sid','audio/QCELP',\
        'audio/raptorfec','audio/RED','audio/rtp-enc-aescm128','audio/rtploopback','audio/rtp-midi','audio/rtx','audio/scip','audio/SMV','audio/SMV0','audio/SMV-QCP','audio/sofa','audio/sp-midi','audio/speex','audio/t140c','audio/t38','audio/telephone-event','audio/TETRA_ACELP','audio/TETRA_ACELP_BB','audio/tone','audio/TSVCIS','audio/UEMCLIP','audio/ulpfec','audio/usac','audio/VDVI','audio/VMR-WB','audio/vnd.3gpp.iufp','audio/vnd.4SB','audio/vnd.audiokoz','audio/vnd.CELP',\
        'audio/vnd.cisco.nse','audio/vnd.cmles.radio-events','audio/vnd.cns.anp1','audio/vnd.cns.inf1','audio/vnd.dece.audio','audio/vnd.digital-winds','audio/vnd.dlna.adts','audio/vnd.dolby.heaac.1','audio/vnd.dolby.heaac.2','audio/vnd.dolby.mlp','audio/vnd.dolby.mps','audio/vnd.dolby.pl2','audio/vnd.dolby.pl2x','audio/vnd.dolby.pl2z','audio/vnd.dolby.pulse.1','audio/vnd.dra','audio/vnd.dts','audio/vnd.dts.hd','audio/vnd.dts.uhd','audio/vnd.dvb.file','audio/vnd.everad.plj',\
        'audio/vnd.hns.audio','audio/vnd.lucent.voice','audio/vnd.ms-playready.media.pya','audio/vnd.nokia.mobile-xmf','audio/vnd.nortel.vbk','audio/vnd.nuera.ecelp4800','audio/vnd.nuera.ecelp7470','audio/vnd.nuera.ecelp9600','audio/vnd.octel.sbc','audio/vnd.presonus.multitrack','audio/vnd.qcelp','audio/vnd.rhetorex.32kadpcm','audio/vnd.rip','audio/vnd.sealedmedia.softseal.mpeg','audio/vnd.vmx.cvsd','audio/vorbis','audio/vorbis-config',\
        'font/collection','font/otf','font/sfnt','font/ttf','font/woff','font/woff2',\
        'image/aces','image/apng','image/avci','image/avcs','image/avif','image/bmp','image/cgm','image/dicom-rle','image/dpx','image/emf','image/example','image/fits','image/g3fax','image/heic','image/heic-sequence','image/heif','image/heif-sequence','image/hej2k','image/hsj2','image/j2c','image/jls','image/jp2','image/jph','image/jphc','image/jpm','image/jpx','image/jxr','image/jxrA','image/jxrS','image/jxs','image/jxsc','image/jxsi','image/jxss','image/ktx','image/ktx2',\
        'image/naplps','image/png','image/prs.btif','image/prs.pti','image/pwg-raster','image/svg+xml','image/t38','image/tiff','image/tiff-fx','image/vnd.adobe.photoshop','image/vnd.airzip.accelerator.azv','image/vnd.cns.inf2','image/vnd.dece.graphic','image/vnd.djvu','image/vnd.dwg','image/vnd.dxf','image/vnd.dvb.subtitle','image/vnd.fastbidsheet','image/vnd.fpx','image/vnd.fst','image/vnd.fujixerox.edmics-mmr','image/vnd.fujixerox.edmics-rlc','image/vnd.globalgraphics.pgb',\
        'image/vnd.microsoft.icon','image/vnd.mix','image/vnd.ms-modi','image/vnd.mozilla.apng','image/vnd.net-fpx','image/vnd.pco.b16','image/vnd.radiance','image/vnd.sealed.png','image/vnd.sealedmedia.softseal.gif','image/vnd.sealedmedia.softseal.jpg','image/vnd.svf','image/vnd.tencent.tap','image/vnd.valve.source.texture','image/vnd.wap.wbmp','image/vnd.xiff','image/vnd.zbrush.pcx','image/webp','image/wmf','image/emf','image/wmf',\
        'message/bhttp','message/CPIM','message/delivery-status','message/disposition-notification','message/example','message/feedback-report','message/global','message/global-delivery-status','message/global-disposition-notification','message/global-headers','message/http','message/imdn+xml','message/mls','message/news','message/ohttp-req','message/ohttp-res','message/s-http','message/sip','message/sipfrag','message/tracking-status','message/vnd.si.simp','message/vnd.wfa.wsc',\
        'model/3mf','model/e57','model/example','model/gltf-binary','model/gltf+json','model/JT','model/iges','model/mtl','model/obj','model/prc','model/step','model/step+xml','model/step+zip','model/step-xml+zip','model/stl','model/u3d','model/vnd.bary','model/vnd.cld','model/vnd.collada+xml','model/vnd.dwf','model/vnd.flatland.3dml','model/vnd.gdl','model/vnd.gs-gdl','model/vnd.gtw','model/vnd.moml+xml','model/vnd.mts','model/vnd.opengex','model/vnd.parasolid.transmit.binary',\
        'model/vnd.parasolid.transmit.text','model/vnd.pytha.pyox','model/vnd.rosette.annotated-data-model','model/vnd.sap.vds','model/vnd.usda','model/vnd.usdz+zip','model/vnd.valve.source.compiled-map','model/vnd.vtu','model/x3d-vrml','model/x3d+fastinfoset','model/x3d+xml','multipart/appledouble','multipart/byteranges','multipart/encrypted','multipart/example','multipart/form-data','multipart/header-set','multipart/multilingual','multipart/related','multipart/report',\
        'multipart/signed','multipart/vnd.bint.med-plus','multipart/voice-message','multipart/x-mixed-replace',\
        'text/1d-interleaved-parityfec','text/cache-manifest','text/calendar','text/cql','text/cql-expression','text/cql-identifier','text/css','text/csv','text/csv-schema','text/directory','text/dns','text/ecmascript','text/encaprtp','text/example','text/fhirpath','text/flexfec','text/fwdred','text/gff3','text/grammar-ref-list','text/hl7v2','text/html','text/javascript','text/jcr-cnd','text/markdown','text/mizar','text/n3','text/parameters','text/parityfec',\
        'text/provenance-notation','text/prs.fallenstein.rst','text/prs.lines.tag','text/prs.prop.logic','text/prs.texi','text/raptorfec','text/RED','text/rfc822-headers','text/rtf','text/rtp-enc-aescm128','text/rtploopback','text/rtx','text/SGML','text/shaclc','text/shex','text/spdx','text/strings','text/t140','text/tab-separated-values','text/troff','text/turtle','text/ulpfec','text/uri-list','text/vcard','text/vnd.a','text/vnd.abc','text/vnd.ascii-art','text/vnd.curl',\
        'text/vnd.debian.copyright','text/vnd.DMClientScript','text/vnd.dvb.subtitle','text/vnd.esmertec.theme-descriptor','text/vnd.exchangeable','text/vnd.familysearch.gedcom','text/vnd.ficlab.flt','text/vnd.fly','text/vnd.fmi.flexstor','text/vnd.gml','text/vnd.graphviz','text/vnd.hans','text/vnd.hgl','text/vnd.in3d.3dml','text/vnd.in3d.spot','text/vnd.IPTC.NewsML','text/vnd.IPTC.NITF','text/vnd.latex-z','text/vnd.motorola.reflex','text/vnd.ms-mediapackage',\
        'text/vnd.net2phone.commcenter.command','text/vnd.radisys.msml-basic-layout','text/vnd.senx.warpscript','text/vnd.si.uricatalogue','text/vnd.sun.j2me.app-descriptor','text/vnd.sosi','text/vnd.trolltech.linguist','text/vnd.wap.si','text/vnd.wap.sl','text/vnd.wap.wml','text/vnd.wap.wmlscript','text/vtt','text/wgsl','text/xml','text/xml-external-parsed-entity',\
        'video/1d-interleaved-parityfec','video/3gpp','video/3gpp2','video/3gpp-tt','video/AV1','video/BMPEG','video/BT656','video/CelB','video/DV','video/encaprtp','video/example','video/FFV1','video/flexfec','video/H261','video/H263','video/H263-1998','video/H263-2000','video/H264','video/H264-RCDO','video/H264-SVC','video/H265','video/H266','video/iso.segment','video/JPEG','video/jpeg2000','video/jxsv','video/matroska','video/matroska-3d','video/mj2','video/MP1S','video/MP2P',\
        'video/MP2T','video/mp4','video/MP4V-ES','video/MPV','video/mpeg4-generic','video/nv','video/ogg','video/parityfec','video/pointer','video/quicktime','video/raptorfec','video/raw','video/rtp-enc-aescm128','video/rtploopback','video/rtx','video/scip','video/smpte291','video/SMPTE292M','video/ulpfec','video/vc1','video/vc2','video/vnd.CCTV','video/vnd.dece.hd','video/vnd.dece.mobile','video/vnd.dece.mp4','video/vnd.dece.pd','video/vnd.dece.sd','video/vnd.dece.video',\
        'video/vnd.directv.mpeg','video/vnd.directv.mpeg-tts','video/vnd.dlna.mpeg-tts','video/vnd.dvb.file','video/vnd.fvt','video/vnd.hns.video','video/vnd.iptvforum.1dparityfec-1010','video/vnd.iptvforum.1dparityfec-2005','video/vnd.iptvforum.2dparityfec-1010','video/vnd.iptvforum.2dparityfec-2005','video/vnd.iptvforum.ttsavc','video/vnd.iptvforum.ttsmpeg2','video/vnd.motorola.video','video/vnd.motorola.videop','video/vnd.mpegurl','video/vnd.ms-playready.media.pyv',\
        'video/vnd.nokia.interleaved-multimedia','video/vnd.nokia.mp4vr','video/vnd.nokia.videovoip','video/vnd.objectvideo','video/vnd.radgamettools.bink','video/vnd.radgamettools.smacker','video/vnd.sealed.mpeg1','video/vnd.sealed.mpeg4','video/vnd.sealed.swf','video/vnd.sealedmedia.softseal.mov','video/vnd.uvvu.mp4','video/vnd.youtube.yt','video/vnd.vivo','video/VP8','video/VP9',\
        'mailto:[dirección]']
        self.completer = QCompleter(wordList)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.dockwidget.lineEditMIME.setCompleter(self.completer)
        wordList=['Personal autorizado','Sin restricción','Limitado',\
        'Solicitar autorización','None','Libre','Regido por la licencia',\
        'Información Confidencial','Sin autorización', 'Acceso limitado',\
        'Uso limitado','comunicarse con el contacto','Acceso abierto','Datos abiertos']
        self.completer = QCompleter(wordList)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.dockwidget.lineEditACCESO.setCompleter(self.completer)
        self.dockwidget.lineEditUSO.setCompleter(self.completer)
        
