import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from ftplib import FTP
import os
from datetime import datetime

class FTPClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FTP 클라이언트")
        self.setGeometry(100, 100, 1200, 800)
        
        # FTP 연결 상태
        self.ftp = None
        self.connected = False
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        layout = QHBoxLayout(central_widget)
        
        # 왼쪽 패널 (서버 연결 및 파일 선택)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # 서버 연결 그룹
        connection_group = QGroupBox("서버 연결")
        connection_layout = QFormLayout()
        
        self.host_input = QLineEdit("localhost")
        self.port_input = QLineEdit("2121")
        self.username_input = QLineEdit("admin")
        self.password_input = QLineEdit("1234")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        connection_layout.addRow("호스트:", self.host_input)
        connection_layout.addRow("포트:", self.port_input)
        connection_layout.addRow("사용자:", self.username_input)
        connection_layout.addRow("비밀번호:", self.password_input)
        
        self.connect_btn = QPushButton("연결")
        self.connect_btn.clicked.connect(self.connect_ftp)
        connection_layout.addRow(self.connect_btn)
        
        connection_group.setLayout(connection_layout)
        left_layout.addWidget(connection_group)
        
        # 파일 선택 그룹
        file_group = QGroupBox("파일 선택")
        file_layout = QVBoxLayout()
        
        self.file_btn = QPushButton("파일 선택")
        self.file_btn.clicked.connect(self.select_file)
        self.file_label = QLabel("선택된 파일 없음")
        
        file_layout.addWidget(self.file_btn)
        file_layout.addWidget(self.file_label)
        
        file_group.setLayout(file_layout)
        left_layout.addWidget(file_group)
        
        # 업로드 버튼
        self.upload_btn = QPushButton("업로드")
        self.upload_btn.clicked.connect(self.upload_file)
        left_layout.addWidget(self.upload_btn)
        
        layout.addWidget(left_panel, 1)
        
        # 오른쪽 패널 (제목 및 내용 입력)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # 제목 입력
        title_layout = QHBoxLayout()
        title_label = QLabel("제목:")
        self.title_input = QLineEdit()
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        right_layout.addLayout(title_layout)
        
        # 내용 입력 (QTextEdit)
        content_label = QLabel("내용:")
        right_layout.addWidget(content_label)
        
        self.textEdit = QTextEdit()
        self.textEdit.setAcceptRichText(True)
        self.textEdit.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: #212121;
                border: 1px solid #e0e0e0;
                padding: 8px;
                font-size: 12pt;
            }
            QTextEdit table {
                border: 1px solid black;
                border-collapse: collapse;
            }
            QTextEdit td, QTextEdit th {
                border: 1px solid black;
                padding: 8px;
            }
        """)
        
        # 기본 문서 스타일 설정
        doc = self.textEdit.document()
        doc.setDefaultStyleSheet("""
            table { border-collapse: collapse; margin: 10px 0; }
            table, th, td { border: 1px solid black; padding: 8px; }
            th { background-color: #f0f0f0; }
        """)
        
        right_layout.addWidget(self.textEdit)
        layout.addWidget(right_panel, 2)
        
        self.show()
        
    def connect_ftp(self):
        try:
            host = self.host_input.text()
            port = int(self.port_input.text())
            username = self.username_input.text()
            password = self.password_input.text()
            
            if not all([host, port, username, password]):
                QMessageBox.critical(self, "오류", "모든 연결 정보를 입력해주세요.")
                return
                
            self.ftp = FTP()
            self.ftp.connect(host=host, port=port)
            self.ftp.login(username, password)
            self.connected = True
            
            QMessageBox.information(self, "성공", "FTP 서버에 연결되었습니다.")
            self.connect_btn.setStyleSheet("background-color: #4CAF50; color: white;")
            self.connect_btn.setText("연결됨")
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"연결 실패: {str(e)}")
            self.connected = False
            
    def select_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "파일 선택")
        if filename:
            self.selected_file = filename
            self.file_label.setText(os.path.basename(filename))
            
    def upload_file(self):
        if not self.connected:
            QMessageBox.critical(self, "오류", "먼저 FTP 서버에 연결해주세요.")
            return
            
        if not hasattr(self, 'selected_file'):
            QMessageBox.critical(self, "오류", "업로드할 파일을 선택해주세요.")
            return
            
        title = self.title_input.text()
        content = self.textEdit.toHtml()
        
        if not title:
            QMessageBox.critical(self, "오류", "제목을 입력해주세요.")
            return
            
        if not content:
            QMessageBox.critical(self, "오류", "내용을 입력해주세요.")
            return
            
        try:
            # 파일 이름에 제목과 날짜 추가
            file_ext = os.path.splitext(self.selected_file)[1]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{title}_{timestamp}{file_ext}"
            
            # 내용을 임시 파일로 저장
            content_filename = f"content_{timestamp}.html"
            with open(content_filename, 'w', encoding='utf-8') as f:
                f.write(f"<h1>{title}</h1>\n\n")
                f.write(content)
            
            # 파일 업로드
            with open(self.selected_file, 'rb') as file:
                self.ftp.storbinary(f'STOR {new_filename}', file)
                
            # 내용 파일 업로드
            with open(content_filename, 'rb') as file:
                self.ftp.storbinary(f'STOR {os.path.splitext(new_filename)[0]}_content.html', file)
            
            # 임시 파일 삭제
            os.remove(content_filename)
                
            QMessageBox.information(self, "성공", "파일과 내용이 성공적으로 업로드되었습니다.")
            self.file_label.setText("선택된 파일 없음")
            self.title_input.clear()
            self.textEdit.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"업로드 실패: {str(e)}")
            if os.path.exists(content_filename):
                os.remove(content_filename)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = FTPClient()
    sys.exit(app.exec()) 