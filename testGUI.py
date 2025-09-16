import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt
from modules import urlFactory
import vlc

class CCTVPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CCTV 스트림 플레이어")
        self.setGeometry(100, 100, 800, 400)
        main_layout = QHBoxLayout()

        # 좌측: 리스트
        left_layout = QVBoxLayout()
        self.label = QLabel("CCTV 목록에서 선택하세요")
        left_layout.addWidget(self.label)
        self.listWidget = QListWidget()
        self.cctv_names = urlFactory._getCCTVNameList(mode="tag")
        self.listWidget.addItems(self.cctv_names)
        left_layout.addWidget(self.listWidget)
        self.playButton = QPushButton("재생")
        self.playButton.clicked.connect(self.play_stream)
        left_layout.addWidget(self.playButton)
        self.stopButton = QPushButton("멈춤")
        self.stopButton.clicked.connect(self.stop_stream)
        left_layout.addWidget(self.stopButton)
        main_layout.addLayout(left_layout)

        # 우측: 플레이어 영역
        right_layout = QVBoxLayout()
        self.player_label = QLabel("플레이어 영역")
        self.player_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.player_label)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)
        self.player = None

    def play_stream(self):
        selected = self.listWidget.currentItem()
        if selected:
            cctv_name = selected.text()
            url = urlFactory._findCCTVinJson(cctvName=cctv_name)
            if url:
                self.label.setText(f"재생 중: {cctv_name}")
                if self.player:
                    self.player.stop()
                # VLC 경로 지정 필요시 아래 경로 수정
                vlc_path = r"C:\\Program Files\\VideoLAN\\VLC\\"
                try:
                    instance = vlc.Instance(f'--plugin-path={vlc_path}')
                except Exception:
                    instance = vlc.Instance()
                self.player = instance.media_player_new()
                media = instance.media_new(url)
                self.player.set_media(media)
                self.player.play()
                self.player_label.setText(f"스트림 재생 중...\n{url}")
            else:
                self.label.setText("URL을 찾을 수 없습니다.")
                self.player_label.setText("")

    def stop_stream(self):
        if self.player:
            self.player.stop()
            self.label.setText("재생 멈춤")
            self.player_label.setText("플레이어 영역")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CCTVPlayer()
    window.show()
    sys.exit(app.exec_())