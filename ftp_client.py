import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, font
from ftplib import FTP
import os
from datetime import datetime

class MaterialStyle:
    """Material Design 스타일 정의"""
    # 색상
    PRIMARY_COLOR = "#6200EE"  # 안드로이드 기본 보라색
    PRIMARY_DARK = "#3700B3"
    PRIMARY_LIGHT = "#BB86FC"
    SECONDARY_COLOR = "#03DAC6"  # 안드로이드 보조 색상
    BACKGROUND_COLOR = "#FFFFFF"
    SURFACE_COLOR = "#F5F5F5"
    ERROR_COLOR = "#B00020"
    SUCCESS_COLOR = "#4CAF50"
    TEXT_PRIMARY = "#212121"
    TEXT_SECONDARY = "#757575"
    
    # 폰트
    FONT_FAMILY = "Segoe UI"
    FONT_LARGE = (FONT_FAMILY, 14)
    FONT_MEDIUM = (FONT_FAMILY, 12)
    FONT_SMALL = (FONT_FAMILY, 10)
    
    # 패딩
    PADDING_LARGE = 20
    PADDING_MEDIUM = 12
    PADDING_SMALL = 8
    
    @classmethod
    def setup_styles(cls, style):
        """ttk 스타일 설정"""
        # 기본 스타일
        style.configure("TFrame", background=cls.BACKGROUND_COLOR)
        style.configure("TLabel", background=cls.BACKGROUND_COLOR, foreground=cls.TEXT_PRIMARY, font=cls.FONT_MEDIUM)
        style.configure("TEntry", fieldbackground=cls.BACKGROUND_COLOR, foreground=cls.TEXT_PRIMARY, font=cls.FONT_MEDIUM)
        
        # 카드 프레임 스타일
        style.configure("Card.TFrame", 
                        background=cls.SURFACE_COLOR, 
                        relief="flat",
                        borderwidth=0)
        
        # 제목 레이블 스타일
        style.configure("Title.TLabel", 
                        font=(cls.FONT_FAMILY, 16, "bold"),
                        foreground=cls.TEXT_PRIMARY,
                        background=cls.BACKGROUND_COLOR,
                        padding=(0, cls.PADDING_MEDIUM))
        
        # 부제목 레이블 스타일
        style.configure("Subtitle.TLabel", 
                        font=(cls.FONT_FAMILY, 14),
                        foreground=cls.TEXT_PRIMARY,
                        background=cls.BACKGROUND_COLOR,
                        padding=(0, cls.PADDING_SMALL))
        
        # 상태 레이블 스타일
        style.configure("Status.TLabel", 
                        font=cls.FONT_MEDIUM,
                        background=cls.BACKGROUND_COLOR)
        
        # 성공 상태 레이블
        style.configure("Success.TLabel", 
                        foreground=cls.SUCCESS_COLOR,
                        background=cls.BACKGROUND_COLOR,
                        font=cls.FONT_MEDIUM)
        
        # 오류 상태 레이블
        style.configure("Error.TLabel", 
                        foreground=cls.ERROR_COLOR,
                        background=cls.BACKGROUND_COLOR,
                        font=cls.FONT_MEDIUM)
        
        # 파일 레이블 스타일
        style.configure("File.TLabel", 
                        foreground=cls.PRIMARY_COLOR,
                        background=cls.SURFACE_COLOR,
                        font=cls.FONT_MEDIUM)

class MaterialButton(tk.Button):
    """Material Design 스타일의 버튼"""
    def __init__(self, master=None, **kwargs):
        self.style_type = kwargs.pop('style_type', 'primary')
        
        # 스타일 타입에 따른 색상 설정
        if self.style_type == 'primary':
            bg_color = MaterialStyle.PRIMARY_COLOR
            fg_color = "white"
            active_bg = MaterialStyle.PRIMARY_DARK
        elif self.style_type == 'accent':
            bg_color = MaterialStyle.SECONDARY_COLOR
            fg_color = MaterialStyle.TEXT_PRIMARY
            active_bg = "#00B5A3"
        elif self.style_type == 'danger':
            bg_color = MaterialStyle.ERROR_COLOR
            fg_color = "white"
            active_bg = "#9B001C"
        else:
            bg_color = MaterialStyle.PRIMARY_COLOR
            fg_color = "white"
            active_bg = MaterialStyle.PRIMARY_DARK
        
        # 기본 스타일 설정
        kwargs.update({
            'background': bg_color,
            'foreground': fg_color,
            'activebackground': active_bg,
            'activeforeground': fg_color,
            'font': MaterialStyle.FONT_MEDIUM,
            'borderwidth': 0,
            'highlightthickness': 0,
            'padx': MaterialStyle.PADDING_MEDIUM,
            'pady': MaterialStyle.PADDING_SMALL,
            'relief': 'flat',
            'cursor': 'hand2'
        })
        
        super().__init__(master, **kwargs)
        
        # 마우스 오버 효과
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, e):
        if self.style_type == 'primary':
            self['background'] = MaterialStyle.PRIMARY_DARK
        elif self.style_type == 'accent':
            self['background'] = "#00B5A3"
        elif self.style_type == 'danger':
            self['background'] = "#9B001C"
    
    def _on_leave(self, e):
        if self.style_type == 'primary':
            self['background'] = MaterialStyle.PRIMARY_COLOR
        elif self.style_type == 'accent':
            self['background'] = MaterialStyle.SECONDARY_COLOR
        elif self.style_type == 'danger':
            self['background'] = MaterialStyle.ERROR_COLOR

class FileCard(ttk.Frame):
    """파일 정보를 표시하는 카드"""
    def __init__(self, master=None, filename=None, **kwargs):
        super().__init__(master, style="Card.TFrame", **kwargs)
        
        self.filename = filename
        self.file_icon = "📄"  # 기본 파일 아이콘
        
        # 파일 확장자에 따른 아이콘 설정
        if filename:
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                self.file_icon = "🖼️"
            elif ext in ['.doc', '.docx', '.txt', '.pdf']:
                self.file_icon = "📝"
            elif ext in ['.xls', '.xlsx', '.csv']:
                self.file_icon = "📊"
            elif ext in ['.ppt', '.pptx']:
                self.file_icon = "📊"
            elif ext in ['.zip', '.rar', '.7z']:
                self.file_icon = "🗜️"
            elif ext in ['.mp3', '.wav', '.ogg']:
                self.file_icon = "🎵"
            elif ext in ['.mp4', '.avi', '.mov']:
                self.file_icon = "🎬"
        
        # 파일 카드 내용
        self.inner_frame = ttk.Frame(self, style="Card.TFrame")
        self.inner_frame.pack(fill="both", expand=True, padx=MaterialStyle.PADDING_SMALL, pady=MaterialStyle.PADDING_SMALL)
        
        # 파일 아이콘과 이름
        self.icon_label = ttk.Label(self.inner_frame, text=self.file_icon, font=("Segoe UI", 24), style="File.TLabel")
        self.icon_label.pack(side="left", padx=(0, MaterialStyle.PADDING_SMALL))
        
        if filename:
            display_name = os.path.basename(filename)
            self.name_label = ttk.Label(self.inner_frame, text=display_name, style="File.TLabel")
        else:
            self.name_label = ttk.Label(self.inner_frame, text="선택된 파일 없음", style="File.TLabel")
        
        self.name_label.pack(side="left", fill="x", expand=True)
    
    def update_file(self, filename):
        """파일 정보 업데이트"""
        self.filename = filename
        
        # 파일 확장자에 따른 아이콘 업데이트
        if filename:
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                self.file_icon = "🖼️"
            elif ext in ['.doc', '.docx', '.txt', '.pdf']:
                self.file_icon = "📝"
            elif ext in ['.xls', '.xlsx', '.csv']:
                self.file_icon = "📊"
            elif ext in ['.ppt', '.pptx']:
                self.file_icon = "📊"
            elif ext in ['.zip', '.rar', '.7z']:
                self.file_icon = "🗜️"
            elif ext in ['.mp3', '.wav', '.ogg']:
                self.file_icon = "🎵"
            elif ext in ['.mp4', '.avi', '.mov']:
                self.file_icon = "🎬"
            else:
                self.file_icon = "📄"
                
            display_name = os.path.basename(filename)
            self.name_label.config(text=display_name)
        else:
            self.file_icon = "📄"
            self.name_label.config(text="선택된 파일 없음")
            
        self.icon_label.config(text=self.file_icon)

class FTPClient:
    def __init__(self, root):
        self.root = root
        self.root.title("FTP 클라이언트")
        self.root.geometry("800x800")  # 창 크기를 더 크게 조정
        self.root.configure(background=MaterialStyle.BACKGROUND_COLOR)
        
        # 기본값 설정
        self.default_values = {
            'host': 'localhost',
            'port': '2121',
            'username': 'admin',
            'password': '1234'
        }
        
        # 창 종료 이벤트 처리
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # FTP 연결 정보
        self.ftp = None
        self.connected = False
        
        # 스타일 설정
        self.style = ttk.Style()
        MaterialStyle.setup_styles(self.style)
        
        # GUI 구성
        self.create_widgets()
        
    def create_widgets(self):
        # 메인 컨테이너
        main_container = ttk.Frame(self.root, style="TFrame")
        main_container.pack(fill="both", expand=True, padx=MaterialStyle.PADDING_LARGE, pady=MaterialStyle.PADDING_LARGE)
        
        # 앱 타이틀
        app_title = ttk.Label(main_container, text="FTP 클라이언트", style="Title.TLabel")
        app_title.pack(fill="x", pady=(0, MaterialStyle.PADDING_MEDIUM))
        
        # 좌우 레이아웃을 위한 프레임
        content_frame = ttk.Frame(main_container, style="TFrame")
        content_frame.pack(fill="both", expand=True)
        
        # 왼쪽 패널 (서버 연결)
        left_panel = ttk.Frame(content_frame, style="TFrame")
        left_panel.pack(side="left", fill="both", padx=(0, MaterialStyle.PADDING_MEDIUM))
        
        # 서버 연결 카드
        connection_card = ttk.Frame(left_panel, style="Card.TFrame")
        connection_card.pack(fill="x", pady=MaterialStyle.PADDING_MEDIUM)
        
        # 카드 내부 패딩을 위한 프레임
        connection_inner = ttk.Frame(connection_card, style="Card.TFrame")
        connection_inner.pack(fill="x", padx=MaterialStyle.PADDING_MEDIUM, pady=MaterialStyle.PADDING_MEDIUM)
        
        # 카드 제목
        ttk.Label(connection_inner, text="서버 연결", style="Subtitle.TLabel").pack(fill="x", anchor="w")
        
        # 호스트 및 포트 프레임
        host_frame = ttk.Frame(connection_inner, style="Card.TFrame")
        host_frame.pack(fill="x", pady=MaterialStyle.PADDING_SMALL)
        
        ttk.Label(host_frame, text="호스트:", style="TLabel").pack(side="left", padx=(0, MaterialStyle.PADDING_SMALL))
        self.host_entry = ttk.Entry(host_frame)
        self.host_entry.insert(0, self.default_values['host'])
        self.host_entry.pack(side="left", fill="x", expand=True, padx=(0, MaterialStyle.PADDING_MEDIUM))
        
        ttk.Label(host_frame, text="포트:", style="TLabel").pack(side="left", padx=(0, MaterialStyle.PADDING_SMALL))
        self.port_entry = ttk.Entry(host_frame, width=8)
        self.port_entry.insert(0, self.default_values['port'])
        self.port_entry.pack(side="left")
        
        # 사용자 프레임
        user_frame = ttk.Frame(connection_inner, style="Card.TFrame")
        user_frame.pack(fill="x", pady=MaterialStyle.PADDING_SMALL)
        
        ttk.Label(user_frame, text="사용자:", style="TLabel").pack(side="left", padx=(0, MaterialStyle.PADDING_SMALL))
        self.username_entry = ttk.Entry(user_frame)
        self.username_entry.insert(0, self.default_values['username'])
        self.username_entry.pack(side="left", fill="x", expand=True)
        
        # 비밀번호 프레임
        pass_frame = ttk.Frame(connection_inner, style="Card.TFrame")
        pass_frame.pack(fill="x", pady=MaterialStyle.PADDING_SMALL)
        
        ttk.Label(pass_frame, text="비밀번호:", style="TLabel").pack(side="left", padx=(0, MaterialStyle.PADDING_SMALL))
        self.password_entry = ttk.Entry(pass_frame, show="•")
        self.password_entry.insert(0, self.default_values['password'])
        self.password_entry.pack(side="left", fill="x", expand=True)
        
        # 연결 버튼 프레임
        btn_frame = ttk.Frame(connection_inner, style="Card.TFrame")
        btn_frame.pack(fill="x", pady=MaterialStyle.PADDING_MEDIUM)
        
        self.connect_btn = MaterialButton(btn_frame, text="연결", command=self.connect_ftp)
        self.connect_btn.pack(side="right")
        
        # 연결 상태 표시
        status_frame = ttk.Frame(connection_inner, style="Card.TFrame")
        status_frame.pack(fill="x")
        
        self.status_label = ttk.Label(status_frame, text="연결 상태: 연결되지 않음", style="Error.TLabel")
        self.status_label.pack(side="left")
        
        # 첨부파일 카드
        attachment_card = ttk.Frame(left_panel, style="Card.TFrame")
        attachment_card.pack(fill="x", pady=MaterialStyle.PADDING_MEDIUM)
        
        # 카드 내부 패딩을 위한 프레임
        attachment_inner = ttk.Frame(attachment_card, style="Card.TFrame")
        attachment_inner.pack(fill="x", padx=MaterialStyle.PADDING_MEDIUM, pady=MaterialStyle.PADDING_MEDIUM)
        
        # 카드 제목
        ttk.Label(attachment_inner, text="첨부파일", style="Subtitle.TLabel").pack(fill="x", anchor="w")
        
        # 첨부파일 버튼 (크고 눈에 띄게)
        self.file_btn = MaterialButton(
            attachment_inner, 
            text="📎 첨부파일 선택", 
            command=self.select_file, 
            style_type="accent",
            font=("Segoe UI", 12, "bold")
        )
        self.file_btn.pack(fill="x", pady=MaterialStyle.PADDING_MEDIUM)
        
        # 파일 카드 (첨부파일 표시)
        self.file_card = FileCard(attachment_inner)
        self.file_card.pack(fill="x", pady=MaterialStyle.PADDING_SMALL)
        
        # 왼쪽 패널 하단 버튼 프레임 (업로드 및 종료 버튼)
        left_bottom_frame = ttk.Frame(left_panel, style="TFrame")
        left_bottom_frame.pack(fill="x", pady=MaterialStyle.PADDING_MEDIUM, side="bottom")
        
        # 버튼 컨테이너 (버튼들을 그룹화)
        button_container = ttk.Frame(left_bottom_frame, style="TFrame")
        button_container.pack(fill="x")
        
        # 종료 버튼
        self.quit_btn = MaterialButton(
            button_container, 
            text="프로그램 종료", 
            command=self.on_closing,
            style_type="danger"
        )
        self.quit_btn.pack(side="left", padx=(0, MaterialStyle.PADDING_SMALL))
        
        # 업로드 버튼
        self.upload_btn = MaterialButton(
            button_container, 
            text="업로드", 
            command=self.upload_file
        )
        self.upload_btn.pack(side="left")
        
        # 오른쪽 패널 (파일 업로드)
        right_panel = ttk.Frame(content_frame, style="TFrame")
        right_panel.pack(side="right", fill="both", expand=True)
        
        # 파일 업로드 카드
        upload_card = ttk.Frame(right_panel, style="Card.TFrame")
        upload_card.pack(fill="both", expand=True)
        
        # 카드 내부 패딩을 위한 프레임
        upload_inner = ttk.Frame(upload_card, style="Card.TFrame")
        upload_inner.pack(fill="both", expand=True, padx=MaterialStyle.PADDING_MEDIUM, pady=MaterialStyle.PADDING_MEDIUM)
        
        # 카드 제목
        ttk.Label(upload_inner, text="파일 업로드", style="Subtitle.TLabel").pack(fill="x", anchor="w")
        
        # 제목 입력 프레임
        title_frame = ttk.Frame(upload_inner, style="Card.TFrame")
        title_frame.pack(fill="x", pady=MaterialStyle.PADDING_SMALL)
        
        ttk.Label(title_frame, text="제목:", style="TLabel").pack(side="left", padx=(0, MaterialStyle.PADDING_SMALL))
        self.title_entry = ttk.Entry(title_frame)
        self.title_entry.pack(side="left", fill="x", expand=True)
        
        # 내용 입력 프레임
        content_frame = ttk.Frame(upload_inner, style="Card.TFrame")
        content_frame.pack(fill="both", expand=True, pady=MaterialStyle.PADDING_SMALL)
        
        ttk.Label(content_frame, text="내용:", style="TLabel").pack(side="top", anchor="w", pady=(0, MaterialStyle.PADDING_SMALL))
        
        # 내용 텍스트 영역
        self.content_text = scrolledtext.ScrolledText(
            content_frame, 
            wrap=tk.WORD, 
            font=MaterialStyle.FONT_MEDIUM,
            background="white",
            foreground=MaterialStyle.TEXT_PRIMARY
        )
        self.content_text.pack(fill="both", expand=True)
        
    def on_closing(self):
        """프로그램 종료 처리"""
        if self.connected:
            if messagebox.askokcancel("종료 확인", 
                "FTP 서버에 연결된 상태입니다.\n정말 종료하시겠습니까?"):
                self.disconnect_ftp()
                self.root.destroy()
        else:
            self.root.destroy()
            
    def disconnect_ftp(self):
        """FTP 연결 종료"""
        if self.ftp:
            try:
                self.ftp.quit()
            except:
                pass
            finally:
                self.ftp = None
                self.connected = False
        
    def connect_ftp(self):
        try:
            host = self.host_entry.get()
            port = self.port_entry.get()
            username = self.username_entry.get()
            password = self.password_entry.get()
            
            if not all([host, port, username, password]):
                messagebox.showerror("오류", "모든 연결 정보를 입력해주세요.")
                return
            
            try:
                port = int(port)
            except ValueError:
                messagebox.showerror("오류", "포트는 숫자여야 합니다.")
                return
                
            self.ftp = FTP()
            self.ftp.connect(host=host, port=port)
            self.ftp.login(username, password)
            self.connected = True
            self.status_label.config(
                text=f"연결 상태: 연결됨 ({host}:{port})",
                style="Success.TLabel"
            )
            
        except Exception as e:
            messagebox.showerror("오류", f"연결 실패: {str(e)}")
            self.status_label.config(
                text="연결 상태: 연결 실패",
                style="Error.TLabel"
            )
            self.connected = False
            
    def select_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.selected_file = filename
            self.file_card.update_file(filename)
            
    def upload_file(self):
        if not self.connected:
            messagebox.showerror("오류", "먼저 FTP 서버에 연결해주세요.")
            return
            
        if not hasattr(self, 'selected_file'):
            messagebox.showerror("오류", "업로드할 파일을 선택해주세요.")
            return
            
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showerror("오류", "제목을 입력해주세요.")
            return
            
        if not content:
            messagebox.showerror("오류", "내용을 입력해주세요.")
            return
            
        try:
            # 파일 이름에 제목과 날짜 추가
            file_ext = os.path.splitext(self.selected_file)[1]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{title}_{timestamp}{file_ext}"
            
            # 내용을 임시 파일로 저장
            content_filename = f"content_{timestamp}.txt"
            with open(content_filename, 'w', encoding='utf-8') as f:
                f.write(f"제목: {title}\n\n")
                f.write(content)
            
            # 파일 업로드
            with open(self.selected_file, 'rb') as file:
                self.ftp.storbinary(f'STOR {new_filename}', file)
                
            # 내용 파일 업로드
            with open(content_filename, 'rb') as file:
                self.ftp.storbinary(f'STOR {os.path.splitext(new_filename)[0]}_content.txt', file)
            
            # 임시 파일 삭제
            os.remove(content_filename)
                
            messagebox.showinfo("성공", "파일과 내용이 성공적으로 업로드되었습니다.")
            self.file_card.update_file(None)
            self.title_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
            
        except Exception as e:
            messagebox.showerror("오류", f"업로드 실패: {str(e)}")
            if os.path.exists(content_filename):
                os.remove(content_filename)

if __name__ == "__main__":
    root = tk.Tk()
    app = FTPClient(root)
    root.mainloop() 