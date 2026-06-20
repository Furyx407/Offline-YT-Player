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
VIDE = {".mp4", ".mkv", ".webm", ".mov", ".avi"}
THS = QSize(240, 135)
CrdW = 250

#Thumbnail Cards
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
            Qlabel#title {
                color:#33739d;
                font-size: 14px;
                font-weight: bold;
                }
            Qlabel#thumbnail {
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
    
    clcked = pyqtSignal(str)

    def mousePressEvent(self,event):
        self.clcked.emit(self.imgp)


class VidWindow(QWidget):
    def __init__(self,player,aud):
        super().__init__()
        self.player = player
        self.aud = aud
        self.vol = 0.5

        self.vid = QVideoWidget()

        self.cvw = QWidget()
        self.cvw.setFixedHeight(58)
        self.cvw.setStyleSheet("""
        QWidget {
            background: rgba(0, 0, 0, 160);   
            color: #f3f3f3       
        }
        """)


        mvl = QVBoxLayout(self.cvw)
        # Timing Row
        thvl = QHBoxLayout()
        # Button row
        hvl = QHBoxLayout()

        mvl.setContentsMargins(8,2,8,2)
        mvl.setSpacing(2)
        thvl.setContentsMargins(0,0,0,0)
        thvl.setSpacing(6)
        hvl.setContentsMargins(0,0,0,0)
        thvl.setSpacing(6)

        self.curtim = QLabel("0:00")
        self.curtim.setMinimumSize(80,0)
        self.curtim.setFixedWidth(55)
        self.curtim.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thvl.addWidget(self.curtim)

        self.timslid = QSlider(Qt.Orientation.Horizontal)
        self.timslid.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #444;
                border-radius: 2px;
            }

            QSlider::handle:horizontal {
                width: 10px;
                height: 10px;
                margin: -4px 0;
                background: #f3f3f3;
                border-radius: 5px;
            }

            QSlider::sub-page:horizontal {
            background: #33739d;
            border-radius: 2px;
            }
        """)
        self.timslid.setFixedHeight(14)
        self.timslid.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        thvl.addWidget(self.timslid)

        self.ttltim = QLabel("0:00")
        self.ttltim.setMinimumSize(80,0)
        self.ttltim.setFixedWidth(55)
        self.ttltim.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thvl.addWidget(self.ttltim)
        
        self.player.positionChanged.connect(self.vpos)
        self.player.durationChanged.connect(self.vdur)
        self.timslid.sliderMoved.connect(self.player.setPosition)

        self.pbt = QPushButton("Pause")
        self.pbt.clicked.connect(self.tp)
        self.pbt.setFixedHeight(22)

        self.vl = QLabel("50%")
        self.vl.setFixedHeight(22)

        hvl.addStretch()
        hvl.addWidget(self.pbt)
        hvl.addStretch()
        hvl.addWidget(self.vl)

        mvl.addLayout(thvl)
        mvl.addLayout(hvl)        

        lyt = QVBoxLayout(self)
        lyt.setContentsMargins(0,0,0,0)
        lyt.setSpacing(0)
        lyt.addWidget(self.vid)
        lyt.addWidget(self.cvw)

    def fmt(self,ms):
        sectim = ms // 1000
        mins = sectim // 60
        secs = sectim % 60
        return f"{mins}:{secs:02d}"
    
    def vpos(self, pos):
        self.timslid.blockSignals(True)
        self.timslid.setValue(pos)
        self.timslid.blockSignals(False)
        self.curtim.setText(self.fmt(pos))
        self.ttltim.setText(self.fmt(self.player.duration()))

    def vdur(self, dur):
        self.timslid.setRange(0,dur)
        self.ttltim.setText(self.fmt(dur))
        
    
    def efs(self):
        self.cvw.hide()
        self.showFullScreen()

    def mouseMoveEvent(self, event):
        nb = event.position().y() > self.height() -140

        if nb:
            self.cvw.show()
            self.ht.start()
        super().mouseMoveEvent(event)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
                self.cvw.show()
            else:
                self.player.stop()
                self.close()

        elif event.key() == Qt.Key.Key_Space:
            self.tp()

        elif event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down:
            if event.key() == Qt.Key.Key_Up:
                self.vol = round(min(self.vol + 0.05, 1.0), 2)
                print(self.vol)
            else:
                self.vol = round(max(self.vol - 0.05,0.0),2)
                print(self.vol)
            self.aud.setVolume(self.vol)
            self.vl.setText(f"{int(self.vol * 100)}%")

        elif event.key() == Qt.Key.Key_Right or event.key() == Qt.Key.Key_Left:
            if event.key() == Qt.Key.Key_Right:
                npos = self.player.position() + 10000
            else:
                npos = self.player.position() - 10000
            self.player.setPosition(max(npos, 0))
        elif event.key() == Qt.Key.Key_M:
            if self.aud.isMuted() == True:
                self.aud.setMuted(False)
            else:
                self.aud.setMuted(True)

        elif event.key() == Qt.Key.Key_F:
            if self.isFullScreen():
                self.showNormal()
                self.cvw.show()
            else:
                self.cvw.hide()
                self.showFullScreen()
        else:
            super().keyPressEvent(event)

    def tp(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.pbt.setText("PLAY")
        else:
            self.player.play()
            self.pbt.setText("PAUSE")


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
        #Media player
        self.medp()
        self.aud.setVolume(0.5)
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

    def medp(self):
        self.plyr = QMediaPlayer()
        self.aud = QAudioOutput()
        self.vid = VidWindow(self.plyr,self.aud)
        self.plyr.setAudioOutput(self.aud)
        self.plyr.setVideoOutput(self.vid.vid)

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
            crd = TC(imgp)
            crd.clcked.connect(self.pvfi)
            self.gl.addWidget(crd, r, col)

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

    def pvfi(self, imgp):
        bse = os.path.splitext(imgp)[0]

        for ext in VIDE:
            vp = bse + ext
            if os.path.exists(vp):
                self.playvid(vp)
                return
        self.statusBar().showMessage("No Matching Video :(")
    
    def playvid(self,vp):
        self.plyr.setSource(QUrl.fromLocalFile(vp))
        self.vid.efs()
        self.plyr.play()



app = QApplication([])

mdpl = MW()
mdpl.show()
app.exec()
