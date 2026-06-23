# PyQt6 for web popup
from PyQt6.QtMultimediaWidgets import *
from PyQt6.QtMultimedia import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import os

# PLAN
# SETTINGS

# PyQt6
THMBNLW = 240
THMBNLH = 135
IMGE = {".png", ".jpg", ".jpeg",".webp"}
VIDE = {".mp4", ".mkv", ".webm", ".mov", ".avi"}
THS = QSize(THMBNLW, THMBNLH)
CrdW = 250

#Thumbnail Cards
class TC(QFrame):
    def __init__(self, imgp):
        super().__init__()
        self.imgp = imgp
        self.setFixedWidth(CrdW)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setStyleSheet("""
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
            """)
        
        lyt = QVBoxLayout(self)
        lyt.setContentsMargins(10, 10, 10, 15)
        lyt.setSpacing(5)

        self.thmbnl = QLabel()
        self.thmbnl.setObjectName("thmbnail")
        self.thmbnl.setFixedSize(THS)
        self.thmbnl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #NM = NAME, removes extra part from " - [" onwards MAKE TOGGLEABLE
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


# self.tggle = QToggle
#self.tggle.toggled.connect(def)
class QToggle(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(46, 24)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setChecked(not self.isChecked())
            event.accept()
        else:
            super().mousePressEvent(event)

    def paintEvent(self, event):
        pntr = QPainter(self)
        pntr.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg = QColor("#33739d") if self.isChecked() else QColor("#444")
        pntr.setBrush(bg)
        pntr.setPen(Qt.PenStyle.NoPen)
        pntr.drawRoundedRect(0, 0, 46, 24, 12, 12)

        kx = 24 if self.isChecked() else 2
        pntr.setBrush(QColor("#f3f3f3"))
        pntr.drawEllipse(kx, 2, 20, 20)

class VidWindow(QWidget):
    def __init__(self,player,aud):
        super().__init__()
        self.player = player
        self.aud = aud
        self.vol = 0.5
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.vid = QVideoWidget()

        self.cvw = QWidget()
        self.cvw.setFixedHeight(58)

        # Main Vertical Layout
        self.mvl = QVBoxLayout(self.cvw)
        # Timing Row
        self.thvl = QHBoxLayout()
        # Button row
        self.hvl = QHBoxLayout()
        #Volume 
        self.vll = QHBoxLayout()
        
        
        self.mvl.setContentsMargins(8,2,8,2)
        self.mvl.setSpacing(2)

        self.thvl.setContentsMargins(0,0,0,0)
        self.thvl.setSpacing(6)
        self.hvl.setContentsMargins(0,0,0,0)
        self.hvl.setSpacing(6)

        self.plt()
        self.btn()

        self.hvl.addStretch()
        self.hvl.addWidget(self.sbd)
        self.hvl.addWidget(self.pbt)
        self.hvl.addWidget(self.sfd)
        self.hvl.addLayout(self.vll)

        self.vll.setSpacing(5)
        self.vll.addStretch()
        self.vll.addWidget(self.vlb)
        self.vll.addWidget(self.vls)
        self.vll.addWidget(self.vl)
    

        self.mvl.addLayout(self.thvl)
        self.mvl.addLayout(self.hvl)        

        lyt = QVBoxLayout(self)
        lyt.setContentsMargins(0,0,0,0)
        lyt.setSpacing(0)
        lyt.addWidget(self.vid)
        lyt.addWidget(self.cvw)

        #Stop other widgets form taking the focus -- Should change to stop glitches with sliders and stuff.
        self.vl.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.vlb.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.vls.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.sbd.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.sfd.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.timslid.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pbt.setFocusPolicy(Qt.FocusPolicy.NoFocus)


    def plt(self):
        self.curtim = QLabel("0:00")
        self.curtim.setMinimumSize(80,0)
        self.curtim.setFixedWidth(55)
        self.curtim.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thvl.addWidget(self.curtim)

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
            QSizePolicy.Policy.Fixed)
        self.thvl.addWidget(self.timslid)

        self.ttltim = QLabel("0:00")
        self.ttltim.setMinimumSize(80,0)
        self.ttltim.setFixedWidth(55)
        self.ttltim.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thvl.addWidget(self.ttltim)
        
        self.player.positionChanged.connect(self.vpos)
        self.player.durationChanged.connect(self.vdur)
        self.timslid.sliderMoved.connect(self.player.setPosition)

    def btn(self):
        # Play / Pause Button
        self.pbt = QPushButton()
        self.pbt.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        self.pbt.clicked.connect(self.tp)
        self.pbt.setFixedHeight(22)
        self.pbt.setIconSize(QSize(16,16))

        # Seek Forwards
        self.sfd = QPushButton()
        self.sfd.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekForward))
        self.sfd.clicked.connect(self.sf)
        self.sfd.setFixedHeight(22)
        self.sfd.setIconSize(QSize(16,16))

        # Seek Backwards
        self.sbd = QPushButton()
        self.sbd.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekBackward))
        self.sbd.clicked.connect(self.sb)
        self.sbd.setFixedHeight(22)
        self.sbd.setIconSize(QSize(16,16))

        #Volume
        self.vl = QLabel("50%")
        self.vl.setFixedHeight(22)

        #Volume button
        self.vlb = QPushButton()
        self.vlb.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))
        self.vlb.setFixedSize(22,22)
        self.vlb.clicked.connect(self.vlcd)
        
        #Volume slider
        self.vls = QSlider(Qt.Orientation.Horizontal)
        self.vls.setFixedHeight(14)
        self.vls.setFixedWidth(100)
        
        self.vls.setSliderPosition(50)
        self.vls.hide()
        self.vls.setRange(0,100)
        self.vls.sliderMoved.connect(self.volc)
        self.vls.setStyleSheet("""
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

    # Volume slider changed
    def volc(self):
        self.vol = self.vls.sliderPosition()
        print(self.vol)
        self.vol = self.vol / float(100)
        print(self.vol)
        self.aud.setVolume(self.vol)
        self.moum()
        self.vl.setText(f"{int(self.vol * 100)}%")

    # Volume Icon to show/hide volume slider
    def vlcd(self):
        if self.vls.isHidden():
            self.vls.show()
        else:
            self.vls.hide()

    # Find Time in Hours, Minutes and Seconds
    def fmt(self,ms):
        sectim = ms // 1000
        mintim = sectim // 60
        hrs = mintim // 60
        mins = mintim % 60
        secs = sectim % 60
        if hrs >= 1:
            return f"{hrs:02d}:{mins:02d}:{secs:02d}"
        else:
            return f"{mins:02d}:{secs:02d}"
    
    #Video Position
    def vpos(self, pos):
        # Setting to be changed (Changes from duration to time till done)
        ttltim_ttorttltm = 0
        self.timslid.blockSignals(True)
        self.timslid.setValue(pos)
        self.timslid.blockSignals(False)
        self.curtim.setText(self.fmt(pos))
        if ttltim_ttorttltm == 1:
            self.ttltim.setText("-" + self.fmt(self.player.duration() - pos))
        else:
            self.ttltim.setText(self.fmt(self.player.duration()))

    #Sets the slider to go from vid start to finish
    def vdur(self, dur):
        self.timslid.setRange(0,dur)

    # Hide the control panel and goes into full screen    
    def efs(self):
        self.cvw.hide()
        self.showFullScreen()

    def keyPressEvent(self, event):
        # If escape pressed, exit fullscreen or close it
        if event.key() == Qt.Key.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
                self.cvw.show()
            else:
                self.player.stop()
                self.close()

        # Toggle pause when space
        elif event.key() == Qt.Key.Key_Space:
            self.tp()

        # Change volume ( rounded to prevent X.00000000001)
        elif event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down:
            if event.key() == Qt.Key.Key_Up:
                self.vol = round(min(self.vol + 0.05, 1.0), 2)
                print(self.vol)
            else:
                self.vol = round(max(self.vol - 0.05,0.0),2)
                print(self.vol)
            self.moum()
            self.vl.setText(f"{int(self.vol * 100)}%")

        # Skippa Skippa forwards or backwards
        elif event.key() == Qt.Key.Key_Right or event.key() == Qt.Key.Key_Left:
            if event.key() == Qt.Key.Key_Right:
                npos = self.player.position() + 10000
            else:
                npos = self.player.position() - 10000
            self.player.setPosition(max(npos, 0))

        # Mute
        elif event.key() == Qt.Key.Key_M:
            if self.aud.isMuted() == True:
                self.aud.setMuted(False)
            else:
                self.aud.setMuted(True)
            if self.aud.isMuted() == True :
                self.vlb.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolumeMuted))
            else:
                self.vlb.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))

        # Toggle Fullscreen
        elif event.key() == Qt.Key.Key_F:
            if self.isFullScreen():
                self.showNormal()
                self.cvw.show()
            else:
                self.cvw.hide()
                self.showFullScreen()

        else:
            super().keyPressEvent(event)

    # Toggle playback
    def tp(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            icn = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        else:
            self.player.play()
            icn = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
        self.pbt.setIcon(icn)

    #Skippa Skippa
    def sf(self):
        npos = self.player.position() + 10000
        self.player.setPosition(max(npos, 0))
    
    # Rewind backwards
    def sb(self):
        npos = self.player.position() - 10000
        self.player.setPosition(max(npos, 0))

    # To diplay muted or not
    def moum(self):
        if self.vol == 0:
            self.vlb.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolumeMuted))
        else:
            self.vlb.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))
    
    #Change Light mode or darkmode
    def sl(self, checked):
        if checked:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background: #f3f3f3;
                    color: #111111;
                }

                QLineEdit, QComboBox {
                    background: #ffffff;
                    border: 1px solid #c7c7c7;
                    border-radius: 5px;
                    color: #111111;
                    padding: 3px 6px;
            }

            QPushButton {
                background: #e5e5e5;
                border: 1px solid #b8b8b8;
                border-radius: 5px;
                color: #111111;
                padding: 3px 6px;
            }
        """)
        else:
            self.setStyleSheet("""
            QMainWindow, QWidget {
                background: #0f0f0f;
                color: #f3f3f3;
            }

            QLineEdit, QComboBox {
                background: #202020;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                color: #f3f3f3;
                padding: 3px 6px;
            }

            QPushButton {
                background: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                color: #f3f3f3;
                padding: 3px 6px;
            }
        """)

# HLP SETTINGS WINDOW
class STTNG(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setGeometry(500,250,900,600)
        self.mw = main_window
        cw = QWidget(self)
        VL = QVBoxLayout(cw)
        STNGLBL = QLabel("SETTINGS")

        # General eg.colour
        GL = QVBoxLayout()
        T1= QHBoxLayout()
        LM = QToggle()
        
        LM.toggled.connect(self.slm)
        LML = QLabel("Toggle Light Mode")
        T1.addWidget(LM)
        T1.addWidget(LML)
        GL.addLayout(T1)

        VL.addWidget(STNGLBL)
        VL.addLayout(GL)
    
    def slm(self, checked):
        print("Light Mode set" if checked else "Dark Mode")
        self.mw.sl(checked)
        


class MW(QMainWindow):
    def __init__(self):
        super().__init__()

        self.folderloc = ""
        self.lfolder = []
        self.settings = QSettings("OfflineYTPlayer", "MediaPlayer")
        self.imgps = []

        self.setWindowTitle("Media Library")
        self.setGeometry(100, 100, 900, 600)
        self.setStatusBar(QStatusBar(self))

        QApplication.instance().setStyleSheet(
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
""")
        

        #Layout / UI     
        self.ui()
        #Media player
        self.medp()
        self.aud.setVolume(0.5)
        #Select folder
        self.lodfold()
        # Propagate previews
        self.ppg()
        
    def sl(self, checked):
        if checked:
            print("checked")
            QApplication.instance().setStyleSheet("""
                QMainWindow, QWidget {
                    background: #f3f3f3;
                    color: #111111;
                }

                QLineEdit, QComboBox {
                    background: #ffffff;
                    border: 1px solid #c7c7c7;
                    border-radius: 5px;
                    color: #111111;
                    padding: 3px 6px;
            }

            QPushButton {
                background: #e5e5e5;
                border: 1px solid #b8b8b8;
                border-radius: 5px;
                color: #111111;
                padding: 3px 6px;
            }
        """)
        else:
            print("else")
            QApplication.instance().setStyleSheet("""
            QMainWindow, QWidget {
                background: #0f0f0f;
                color: #f3f3f3;
            }

            QLineEdit, QComboBox {
                background: #202020;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                color: #f3f3f3;
                padding: 3px 6px;
            }

            QPushButton {
                background: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                color: #f3f3f3;
                padding: 3px 6px;
            }
        """)

    def ui(self):

        # Central Widget & Vertical & Horizontal Layouts
        cw = QWidget()
        pl = QHBoxLayout(cw)
        #Vertical Popout Layout
        plv = QVBoxLayout()
        # Vertical Popout widget
        self.vpw = QWidget()
        # Vertical popout layout for content
        vpl = QVBoxLayout(self.vpw)
        # Folders
        fld = QHBoxLayout()
        # Main Layout
        ml = QVBoxLayout()
        hl = QHBoxLayout()


        pl.setContentsMargins(10,10,10,10)
        pl.setSpacing(10)
        
        # Main Layout Margins and spacing
        ml.setContentsMargins(10,10,10,10)
        ml.setSpacing(10)

        #Popout popout
        self.pout = QPushButton()
        self.pout.setText("SHOW")
        self.pout.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowRight))
        self.pout.clicked.connect(self.togpop)
        plv.addSpacing(15)
        plv.addWidget(self.pout)
        plv.addWidget(self.vpw, 1)
        plv.setAlignment(self.pout, Qt.AlignmentFlag.AlignTop)
        self.vpw.hide()
        self.vpw.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )     


        pl.addLayout(plv)
        pl.addLayout(ml)
        
        #Search input
        self.sinput = QLineEdit()
        self.sinput.setPlaceholderText("Search here:")
        self.sinput.setMaximumHeight(30)
        self.sinput.textChanged.connect(self.ppg)

        # Switch Folder
        self.fsl = QComboBox()
        self.fsl.setMinimumWidth(150)
        self.fsl.currentIndexChanged.connect(self.switfold)
        vpl.addWidget(self.fsl)
        vpl.addLayout(fld)
        vpl.addStretch()

        #Add folder
        af = QPushButton("Add Folder ")
        af.setFixedSize(125,35)
        af.clicked.connect(self.slf)

        #Remove Folder
        rf= QPushButton("Remove Folder")
        rf.setFixedSize(125,35)
        rf.clicked.connect(self.remfold)

        # Settings Button
        seb = QPushButton("SETTINGS")
        seb.setFixedHeight(35)
        seb.clicked.connect(self.opnsttng)
        vpl.addWidget(seb)

        #Exit button
        eb = QPushButton("EXIT")
        eb.setFixedHeight(35)
        eb.clicked.connect(self.close)
        vpl.addWidget(eb)

        # Horizontal layout add exit button and search
        fld.addWidget(af)
        fld.addWidget(rf)
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

    def togpop(self):
        if self.pout.text() == "SHOW":
            self.vpw.show()
            self.pout.setText("HIDE")
            ard = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown)
        else:
            self.vpw.hide()
            self.pout.setText("SHOW")
            ard = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowRight)
        self.pout.setIcon(ard)

    def medp(self):
        self.plyr = QMediaPlayer()
        self.aud = QAudioOutput()
        self.vid = VidWindow(self.plyr,self.aud)
        self.plyr.setAudioOutput(self.aud)
        self.plyr.setVideoOutput(self.vid.vid)

    def opnsttng(self):
        if not hasattr(self, "sttng"):
            self.sttng = STTNG(self)
        self.sttng.show()
        self.sttng.raise_()
        self.sttng.activateWindow()


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
