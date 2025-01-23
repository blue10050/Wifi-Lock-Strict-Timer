import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import os
import threading
import time
import pyttsx3
import subprocess


class ComputerTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Strict timer")
        self.remaining_time = 0
        self.is_paused = False
        self.password = "log4qwer!!@"  # 기본 비밀번호
        self.reset_password = "reset1234"  # 리셋 비밀번호
        self.failed_attempts = 0
        self.lockout_end_time = 0

        self.engine = pyttsx3.init()  # 음성 알림 초기화
        self.engine.setProperty('rate', 150)

        self.root.geometry("400x450")
        self.disable_task_manager_thread()

        self.timer_label = tk.Label(root, text="00:00:00", font=("Arial", 32))
        self.timer_label.pack(pady=20)

        self.start_frame = tk.Frame(root)
        self.start_frame.pack()

        tk.Label(self.start_frame, text="시간 (시): ").grid(row=0, column=0)
        self.hours_entry = tk.Entry(self.start_frame, width=5)
        self.hours_entry.grid(row=0, column=1)

        tk.Label(self.start_frame, text="시간 (분): ").grid(row=0, column=2)
        self.minutes_entry = tk.Entry(self.start_frame, width=5)
        self.minutes_entry.grid(row=0, column=3)

        self.start_button = tk.Button(root, text="타이머 시작", command=self.start_timer)
        self.start_button.pack(pady=10)

        self.pause_button = tk.Button(root, text="타이머 일시정지", command=self.toggle_pause)
        self.pause_button.pack(pady=10)

        self.extend_frame = tk.Frame(root)
        self.extend_frame.pack()

        tk.Label(self.extend_frame, text="연장 시간 (분): ").grid(row=0, column=0)
        self.extend_entry = tk.Entry(self.extend_frame, width=5)
        self.extend_entry.grid(row=0, column=1)

        self.extend_button = tk.Button(self.extend_frame, text="연장하기", command=self.extend_timer)
        self.extend_button.grid(row=0, column=2)

        self.reset_button = tk.Button(root, text="타이머 리셋", command=self.reset_timer_ui)
        self.reset_button.pack(pady=10)

        self.change_password_button = tk.Button(root, text="일반 비밀번호 변경", command=self.change_general_password_ui)
        self.change_password_button.pack(pady=10)

        self.change_reset_password_button = tk.Button(root, text="리셋 비밀번호 변경", command=self.change_reset_password_ui)
        self.change_reset_password_button.pack(pady=10)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.update_timer_label()

        self.wifi_enabled = True  # 와이파이 상태 변수

    def start_timer(self):
        try:
            hours = int(self.hours_entry.get() or 0)
            minutes = int(self.minutes_entry.get() or 0)

            if hours * 60 + minutes > 180:
                messagebox.showinfo("경고", "어이 그만. 밑장빼기냐?")
                return

            if hours == 0 and minutes == 0:
                messagebox.showinfo("경고", "올바른 시간을 입력해주세요.")
                return

            self.remaining_time = hours * 3600 + minutes * 60
            self.is_paused = False
            self.progress['maximum'] = self.remaining_time
            self.start_button.config(state=tk.DISABLED)
            messagebox.showinfo("타이머 시작", "타이머가 시작되었습니다.")
            threading.Thread(target=self.run_timer, daemon=True).start()
        except ValueError:
            messagebox.showerror("에러", "시간과 분을 올바르게 입력해주세요.")

    def run_timer(self):
        while self.remaining_time > 0:
            if not self.is_paused:
                time.sleep(1)
                self.remaining_time -= 1
                self.progress['value'] = self.progress['maximum'] - self.remaining_time
                self.update_timer_label()

                if self.remaining_time in [600, 300, 60]:
                    self.speak_time_remaining()

        if self.remaining_time == 0:
            self.disable_network()
            self.shutdown_computer()

    def toggle_pause(self):
        if self.check_lockout() and self.prompt_for_password():
            self.is_paused = not self.is_paused

    def extend_timer(self):
        if self.check_lockout() and self.prompt_for_password():
            try:
                extra_minutes = int(self.extend_entry.get() or 0)
                if extra_minutes <= 0:
                    raise ValueError
                self.remaining_time += extra_minutes * 60
                self.progress['maximum'] += extra_minutes * 60
                messagebox.showinfo("확인", f"타이머가 {extra_minutes} 분 연장되었습니다.")
            except ValueError:
                messagebox.showerror("에러", "올바른 시간을 입력해주세요.")

    def reset_timer_ui(self):
        if self.check_lockout() and self.prompt_for_password(self.reset_password):
            self.remaining_time = 0
            self.update_timer_label()
            self.start_button.config(state=tk.NORMAL)
            messagebox.showinfo("타이머 리셋", "타이머가 초기화되었습니다.")

    def change_general_password_ui(self):
        if self.check_lockout() and self.prompt_for_password(self.password):
            new_password = simpledialog.askstring("일반 비밀번호 변경", "새 비밀번호를 입력해주세요:", show='*')
            if new_password:
                self.password = new_password
                messagebox.showinfo("확인", "일반 비밀번호가 변경되었습니다.")

    def change_reset_password_ui(self):
        if self.check_lockout() and self.prompt_for_password(self.reset_password):
            new_password = simpledialog.askstring("리셋 비밀번호 변경", "새 비밀번호를 입력해주세요:", show='*')
            if new_password:
                self.reset_password = new_password
                messagebox.showinfo("확인", "리셋 비밀번호가 변경되었습니다.")

    def shutdown_computer(self):
        os.system("shutdown /s /t 0")

    def disable_network(self):
        self.wifi_enabled = False  # 와이파이 비활성화 상태
        self.disable_task_manager()
        subprocess.call("netsh interface set interface Ethernet admin=disabled", shell=True)  # 이더넷 비활성화
        subprocess.call("netsh interface set interface Wi-Fi admin=disabled", shell=True)  # 와이파이 비활성화

    def enable_network(self):
        if self.prompt_for_password():  # 비밀번호 확인 후 네트워크 재활성화
            subprocess.call("netsh interface set interface Ethernet admin=enabled", shell=True)  # 이더넷 활성화
            subprocess.call("netsh interface set interface Wi-Fi admin=enabled", shell=True)  # 와이파이 활성화
            messagebox.showinfo("확인", "이더넷과 와이파이가 활성화되었습니다.")

    def prompt_for_password(self, expected_password=None):
        expected_password = expected_password or self.password
        input_password = simpledialog.askstring("비밀번호 입력", "비밀번호를 입력해주세요:", show='*')

        if input_password != expected_password:
            self.failed_attempts += 1
            if self.failed_attempts >= 5:
                self.lockout_end_time = time.time() + 300
                messagebox.showwarning("잠금", "비밀번호 시도가 너무 많습니다. 5분 후 다시 시도하세요.")
            return False
        self.failed_attempts = 0
        return True

    def check_lockout(self):
        if time.time() < self.lockout_end_time:
            messagebox.showwarning("잠금", "잠시 후 다시 시도해 주세요.")
            return False
        return True

    def update_timer_label(self):
        hours = self.remaining_time // 3600
        minutes = (self.remaining_time % 3600) // 60
        seconds = self.remaining_time % 60
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.timer_label.config(text=time_str)
        self.root.title(time_str)

    def speak_time_remaining(self):
        minutes = self.remaining_time // 60
        if minutes == 10:
            self.engine.say("10분 남았습니다.")
        elif minutes == 5:
            self.engine.say("5분 남았습니다.")
        elif minutes == 1:
            self.engine.say("1분 남았습니다.")
        self.engine.runAndWait()

    def disable_task_manager(self):
        subprocess.call("REG add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 1 /f", shell=True)

    def disable_task_manager_thread(self):
        def enforce_disable_task_manager():
            while True:
                self.disable_task_manager()
                time.sleep(1)

        threading.Thread(target=enforce_disable_task_manager, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = ComputerTimerApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: messagebox.showinfo("안내", "닫을 수 없습니다."))
    root.mainloop()
