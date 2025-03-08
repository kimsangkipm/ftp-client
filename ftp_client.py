import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from ftplib import FTP
import os
from datetime import datetime

class FTPClient:
    def __init__(self, root):
        self.root = root
        self.root.title("FTP 클라이언트")
        self.root.geometry("600x650")  # 높이를 더 늘림
        
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
        
        # GUI 구성
        self.create_widgets()
        
    def create_widgets(self):
        # 서버 연결 프레임
        connection_frame = ttk.LabelFrame(self.root, text="서버 연결", padding="5")
        connection_frame.pack(fill="x", padx=5, pady=5)
        
        # 호스트 입력
        ttk.Label(connection_frame, text="호스트:").grid(row=0, column=0, padx=5, pady=5)
        self.host_entry = ttk.Entry(connection_frame)
        self.host_entry.insert(0, self.default_values['host'])
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # 포트 입력
        ttk.Label(connection_frame, text="포트:").grid(row=0, column=2, padx=5, pady=5)
        self.port_entry = ttk.Entry(connection_frame, width=10)
        self.port_entry.insert(0, self.default_values['port'])
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # 사용자 입력
        ttk.Label(connection_frame, text="사용자:").grid(row=1, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(connection_frame)
        self.username_entry.insert(0, self.default_values['username'])
        self.username_entry.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        
        # 비밀번호 입력
        ttk.Label(connection_frame, text="비밀번호:").grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(connection_frame, show="*")
        self.password_entry.insert(0, self.default_values['password'])
        self.password_entry.grid(row=2, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        
        # 연결 버튼
        self.connect_btn = ttk.Button(connection_frame, text="연결", command=self.connect_ftp)
        self.connect_btn.grid(row=3, column=0, columnspan=4, pady=5)
        
        # 연결 상태 표시 (연결 버튼 아래)
        self.status_frame = ttk.Frame(connection_frame)
        self.status_frame.grid(row=4, column=0, columnspan=4, pady=5)
        
        self.status_label = ttk.Label(self.status_frame, text="연결 상태: 연결되지 않음", foreground="red")
        self.status_label.pack()
        
        # 파일 업로드 프레임
        upload_frame = ttk.LabelFrame(self.root, text="파일 업로드", padding="5")
        upload_frame.pack(fill="x", padx=5, pady=5)
        
        # 제목 입력
        ttk.Label(upload_frame, text="제목:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(upload_frame)
        self.title_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # 내용 입력
        ttk.Label(upload_frame, text="내용:").grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.content_text = scrolledtext.ScrolledText(upload_frame, width=40, height=10, wrap=tk.WORD)
        self.content_text.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # 파일 선택
        self.file_btn = ttk.Button(upload_frame, text="파일 선택", command=self.select_file)
        self.file_btn.grid(row=2, column=0, padx=5, pady=5)
        
        self.file_label = ttk.Label(upload_frame, text="선택된 파일 없음")
        self.file_label.grid(row=2, column=1, columnspan=2, sticky="w", padx=5, pady=5)
        
        # 업로드 버튼
        self.upload_btn = ttk.Button(upload_frame, text="업로드", command=self.upload_file)
        self.upload_btn.grid(row=3, column=0, columnspan=3, pady=10)
        
        # 하단 버튼 프레임
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill="x", padx=5, pady=10)
        
        # 종료 버튼
        self.quit_btn = ttk.Button(
            bottom_frame, 
            text="프로그램 종료", 
            command=self.on_closing,
            style="Accent.TButton"
        )
        self.quit_btn.pack(side="right", padx=5)
        
        # 스타일 설정
        self.setup_styles()
        
    def setup_styles(self):
        # 종료 버튼용 스타일
        style = ttk.Style()
        style.configure("Accent.TButton", 
                       foreground="red",
                       padding=5)
        
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
                foreground="green"
            )
            
        except Exception as e:
            messagebox.showerror("오류", f"연결 실패: {str(e)}")
            self.status_label.config(
                text="연결 상태: 연결 실패",
                foreground="red"
            )
            self.connected = False
            
    def select_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.selected_file = filename
            self.file_label.config(text=os.path.basename(filename))
            
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
            self.file_label.config(text="선택된 파일 없음")
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