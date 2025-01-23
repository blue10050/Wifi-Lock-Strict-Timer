import tkinter as tk
from tkinter import messagebox
import subprocess

# 하드코딩된 관리자 비밀번호 (변수로 설정)
correct_password = "wifion123asd!!@@"  # 실제 비밀번호로 변경하세요

# 비밀번호를 입력받고 명령어 실행
def run_command():
    # 사용자로부터 입력받은 비밀번호
    password = password_entry.get()

    # 비밀번호 확인
    if password != correct_password:
        messagebox.showerror("오류", "비밀번호가 올바르지 않습니다.")
        return

    # Wi-Fi 인터페이스 상태 확인
    wifi_command = 'netsh interface show interface "Wi-Fi"'
    
    try:
        # 인터페이스 상태 확인
        wifi_status = subprocess.run(wifi_command, shell=True, capture_output=True, text=True)

        # "Admin State"가 포함되어 있고, "enabled" 상태가 아니면 활성화
        if "Admin State" in wifi_status.stdout and "enabled" not in wifi_status.stdout:
            subprocess.run('netsh interface set interface "Wi-Fi" admin=enabled', shell=True, check=True)
            messagebox.showinfo("성공", "Wi-Fi 인터페이스가 활성화되었습니다.")
        else:
            messagebox.showinfo("이미 활성화됨", "Wi-Fi 인터페이스는 이미 활성화되어 있습니다.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("오류", f"명령어 실행 실패: {e}")

# tkinter 윈도우 설정
root = tk.Tk()
root.title("Wi-Fi 활성화")
root.geometry("300x150")

# 비밀번호 입력 필드
password_label = tk.Label(root, text="비밀번호:")
password_label.pack(pady=10)

password_entry = tk.Entry(root, show="*", width=25)
password_entry.pack()

# 실행 버튼
run_button = tk.Button(root, text="Wi-Fi 활성화", command=run_command)
run_button.pack(pady=20)

# tkinter 윈도우 실행
root.mainloop()
