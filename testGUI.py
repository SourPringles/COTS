import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QLabel, QFrame, QComboBox
from PyQt5.QtCore import Qt
from modules import urlFactory
import vlc
import re

class CCTVPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CCTV 스트림 플레이어")
        self.setGeometry(100, 100, 1240, 760)  # 전체 창 크기 조정
        main_layout = QHBoxLayout()

        # 좌측: 리스트
        left_layout = QVBoxLayout()
        self.label = QLabel("CCTV 목록에서 선택하세요")
        left_layout.addWidget(self.label)
        self.sortBox = QComboBox()
        self.sortBox.addItems(["기본순", "오름차순", "내림차순"])
        self.sortBox.currentIndexChanged.connect(self.sort_list)
        left_layout.addWidget(self.sortBox)
        self.listWidget = QListWidget()
        self.listWidget.setFixedWidth(200)  # 리스트 너비 제한
        self.cctv_names = urlFactory._getCCTVNameList(mode="tag")
        self.listWidget.addItems(self.cctv_names)
        left_layout.addWidget(self.listWidget)
        self.playButton = QPushButton("재생")
        left_layout.addWidget(self.playButton)
        self.stopButton = QPushButton("멈춤")
        left_layout.addWidget(self.stopButton)
        main_layout.addLayout(left_layout)

        # 우측: 플레이어 영역 (QFrame)
        right_layout = QVBoxLayout()
        self.video_frame = QFrame()
        self.video_frame.setFixedSize(1024, 720)  # 영상 영역 크기 고정
        self.video_frame.setStyleSheet("background-color: black;")
        right_layout.addWidget(self.video_frame)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)
        self.player = None
        self.playButton.clicked.connect(self.play_stream)
        self.stopButton.clicked.connect(self.stop_stream)

    def sort_key(self, name):
        # '세종 3', '세종 31' 등에서 숫자를 기준으로 정렬
        m = re.search(r'(\D+)(\d+)', name)
        if m:
            prefix = m.group(1)
            num = int(m.group(2))
            return (prefix, num)
        return (name, 0)

    def sort_list(self):
        mode = self.sortBox.currentText()
        if mode == "기본순":
            sorted_names = urlFactory._getCCTVNameList(mode="tag")
        elif mode == "오름차순":
            sorted_names = sorted(self.cctv_names, key=self.sort_key)
        elif mode == "내림차순":
            sorted_names = sorted(self.cctv_names, key=self.sort_key, reverse=True)
        else:
            sorted_names = self.cctv_names
        self.listWidget.clear()
        self.listWidget.addItems(sorted_names)

    def play_stream(self):
        selected = self.listWidget.currentItem()
        if selected:
            cctv_name = selected.text()
            url = urlFactory._findCCTVinJson(cctvName=cctv_name)
            if url:
                self.label.setText(f"재생 중: {cctv_name}")
                if self.player:
                    self.player.stop()
                vlc_path = r"C:\\Program Files\\VideoLAN\\VLC\\"
                try:
                    instance = vlc.Instance(f'--plugin-path={vlc_path}')
                except Exception:
                    instance = vlc.Instance()
                self.player = instance.media_player_new()
                media = instance.media_new(url)
                self.player.set_media(media)
                # VLC를 QFrame에 내장 (Windows)
                self.player.set_hwnd(int(self.video_frame.winId()))
                self.player.play()
            else:
                self.label.setText("URL을 찾을 수 없습니다.")

    def stop_stream(self):
        if self.player:
            self.player.stop()
            self.label.setText("재생 멈춤")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CCTVPlayer()
    window.show()
    sys.exit(app.exec_())