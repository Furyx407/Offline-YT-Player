# PyQt6 for web popup
from PyQt6.QtMultimediaWidgets import *
from PyQt6.QtMultimedia import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from pyqtgraph.dockarea import * 
import os

# ToDO: Implement into UI or as an option in menu

# PyQt6
IMGE = {".png", ".jpg", ".jpeg",".webp"}
THS = QSize(240, 135)
CrdW = 250

class TC(QFrame):
    def __init__(self, imgp):
        super().__init__()
        self.imgp = imgp
        self.setFixedWidth(CrdW)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setStyleSheet(
            """
            QFrame {
                background:transparent;
            }
            Qlabel#ttl {
                color:#33739d;
                font-size: 14px;
                font-weight: bold;
                }
            Qlabel#thmbnl {
                background:#f3f3f3;
                border-radius: 5px;
                }
            """
        )
        lyt = QVBoxLayout(self)
        lyt.setContentsMargins(10, 10, 10, 15)
        lyt.setSpacing(5)

        self.thmbnl = QLabel()
        self.thmbnl.setObjectName("thmbnail")
        self.thmbnl.setFixedSize(THS)
        self.thmbnl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        nm = os.path.splitext(os.path.basename(imgp))[0]
        nm = nm.split(" - [")[0]
        self.ttl = QLabel(nm)
        self.ttl.setObjectName("title")
        self.ttl.setFixedWidth(THS.width())
        self.ttl.setWordWrap(True)

        lyt.addWidget(self.thmbnl)
        lyt.addWidget(self.ttl)
        self.set_thmbnl(imgp)

    def set_thmbnl(self, imgp):
        pxmp = QPixmap(imgp)

        if pxmp.isNull():
            self.thmbnl.setText("No Thumbnail :(")
            return
        
        scld = pxmp.scaled(
            self.thmbnl.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.thmbnl.setPixmap(scld)


class MW(QMainWindow):
    def __init__(self):
        super().__init__()

        self.folderloc = ""
        self.lfolder = []
        self.settings = QSettings("OfflineYTPlayer", "MediaPlayer")
        self.imgps = []

        self.setWindowTitle("Media Player")
        self.setGeometry(100, 100, 900, 600)
        self.setStatusBar(QStatusBar(self))

        self.setStyleSheet(
            """
            QmainWindow, QWidget{
                background: #0f0f0f;
                color: #f3f3f3;
            }           
            QLineEdit, QComboBox{
                background: #202020;
                border:1px solid #3a3a3a;
                border-radius:5px;
                color: #f3f3f3;
                padding:3px,6px;
            }
            QPushButton{
                background:2a2a2a;
                border:1px solid #3a3a3a;
                border-radius:5px;
                color: #f3f3f3;
                padding:3px,6px;
            }
"""
        )



        # Toolbar
        #self.tlb()
        
        #Layout / UI     
        self.ui()
        #Select folder
        self.lodfold()
        self.ppg()

    def tlb(self):
        tb = QToolBar()
        self.addToolBar(tb)
        sf = QAction("&Select Folder", self)
        sf.triggered.connect(self.slf)
        sf.setCheckable(True)
        tb.addAction(sf)

        filemenu = self.menuBar().addMenu("Files")
        filemenu.addAction(sf)
        
    def ui(self):

        # Central Widget & Vertical & Horizontal Layouts
        cw = QWidget()
        ml = QVBoxLayout(cw)
        hl = QHBoxLayout()

        # Main Layout Margins and spacing
        ml.setContentsMargins(10,10,10,10)
        ml.setSpacing(10)

        #Search input
        self.sinput = QLineEdit()
        self.sinput.setPlaceholderText("Search here:")
        self.sinput.setMaximumHeight(30)
        self.sinput.textChanged.connect(self.ppg)

        # Switch Folder
        self.fsl = QComboBox()
        self.fsl.setMinimumWidth(250)
        self.fsl.currentIndexChanged.connect(self.switfold)

        #Add folder
        af = QPushButton("Add Folder ")
        af.setFixedSize(125,35)
        af.clicked.connect(self.slf)

        #Remove Folder
        rf= QPushButton("Remove Folder")
        rf.setFixedSize(125,35)
        rf.clicked.connect(self.remfold)

        #Exit button
        eb = QPushButton("EXIT")
        eb.setFixedSize(100,35)
        eb.clicked.connect(self.close)

        # Horizontal layout add exit button and search
        hl.addWidget(eb)
        hl.addWidget(af)
        hl.addWidget(rf)
        hl.addWidget(self.fsl)
        #hl.addStretch()
        hl.addWidget(self.sinput)
                
        # Scroll bar
        self.sa = QScrollArea()
        self.sa.setWidgetResizable(True)
        self.sa.setFrameShape(QFrame.Shape.NoFrame)
        
        #Grid layout for images
        self.gc = QWidget()
        self.gl = QGridLayout(self.gc)
        self.gl.setContentsMargins(0,0,0,0)
        self.gl.setHorizontalSpacing(14)
        self.gl.setVerticalSpacing(18)
        self.sa.setWidget(self.gc)

        # Add horizontal layout to main layout and add scroll bar and set central widget to central widget
        ml.addLayout(hl)
        ml.addWidget(self.sa)
        
        self.setCentralWidget(cw)


    def slf(self):
        fld = QFileDialog.getExistingDirectory(self,"select image directory", self.folderloc)
        if not fld:
            return
        
        if fld not in self.lfolder:
            self.lfolder.append(fld)
            self.savfold()
            self.reffolders()

        self.fsl.setCurrentIndex(self.lfolder.index(fld))
        self.sfolder(fld)

    def lodfold(self):
        self.lfolder = [
            fld
            for fld in self.settings.value("folders",[], type=list)
            if os.path.isdir(fld)
        ]
        self.reffolders()
        lstfolder = self.settings.value("last_folder","", type=str)
        if lstfolder in self.lfolder:
            self.fsl.setCurrentIndex(self.lfolder.index(lstfolder))
            self.sfolder(lstfolder)
        elif self.lfolder:
            self.fsl.setCurrentIndex(0)
            self.sfolder(self.lfolder[0])

    def savfold(self):
        self.settings.setValue("folders", self.lfolder)
        self.settings.setValue("last_folder", self.folderloc)
    
    def reffolders(self):
        self.fsl.blockSignals(True)
        self.fsl.clear()
        for fld in self.lfolder:
            self.fsl.addItem(os.path.basename(fld) or fld, fld)
        self.fsl.blockSignals(False)

    def switfold(self,index):
        if 0 <= index < len(self.lfolder):
            self.sfolder(self.lfolder[index])
    
    def sfolder(self,fld):
        self.folderloc = fld
        self.settings.setValue("last_folder", self.folderloc)
        self.loadimg()
        self.ppg()

    def remfold(self):
        indx = self.fsl.currentIndex()
        if not 0 <= indx < len(self.lfolder):
            return
        
        remmd = self.lfolder.pop(indx)
        if remmd == self.folderloc:
            self.folderloc = ""
            self.imgps = []

        self.savfold()
        self.reffolders()

        if self.lfolder:
            nindx = min(indx, len(self.lfolder)- 1)
            self.fsl.setCurrentIndex(nindx)
            self.sfolder(self.lfolder[nindx])
        else:
            self.ppg()
            self.statusBar().showMessage("No folder selected :(")

    def loadimg(self):
        self.imgps = []
        if not self.folderloc:
            return
        for filename in sorted(os.listdir(self.folderloc)):
            fp = os.path.join(self.folderloc, filename)
            _, ext = os.path.splitext(filename)
            if os.path.isfile(fp) and ext.lower() in IMGE:
                self.imgps.append(fp)
                self.statusBar().showMessage(f"Loaded {len(self.imgps)} thumbnails")
            

    def ppg(self):
        while self.gl.count():
            it = self.gl.takeAt(0)
            wid = it.widget()
            if wid:
                wid.deleteLater()
        st = self.sinput.text().strip().lower()
        vi = [
            p
            for p in self.imgps
            if st in os.path.basename(p).lower()
        ]
        cols = self.cc()

        for index, imgp in enumerate(vi):
            r = index // cols
            col = index % cols
            self.gl.addWidget(TC(imgp), r, col)

        self.gl.setRowStretch((len(vi)//cols) +1, 1)
        self.gl.setColumnStretch(cols,1)

    def cc(self):
        spc = self.gl.horizontalSpacing()
        aw = max(self.sa.viewport().width(),CrdW)
        return max(1, (aw + spc) // (CrdW + spc) )
    
    def resizeEvent(self,event):
        super().resizeEvent(event)
        if hasattr(self,"gl"):
            self.ppg()



app = QApplication([])

mdpl = MW()
mdpl.show()
app.exec()
