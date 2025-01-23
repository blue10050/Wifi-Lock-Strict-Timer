# Wifi-Lock-Strict-Timer
This timer requires a password to operate and cannot be interrupted. Upon expiration, it will automatically disconnect from Wi-Fi and force the computer to power off.
이 타이머는 타이머를 조작하는데에 필요한 모든 동작을 패스워드가 있어야 동작시킬 수 있으며, 타이머가 끝나면 자동으로 와이파이를 비활성화시키고 컴퓨터를 끕니다.

All source code can be modified by you, and please leave a GitHub link when uploading it elsewhere.
모든 소스 코드는 당신이 수정할 수 있으며, 다른곳에 업로드할때는 깃허브 링크를 남겨주세요.

#This timer is a program I created to reduce my brother's computer use.
#이 타이머는 저희 동생의 컴퓨터 사용을 줄이기 위해 만든 프로그램입니다.

Features -
1. Limit computer usage time with a strict timer
2. Visual display of time remaining right after playing
3. Remaining time announced using TTS library
4. Automatically checks and blocks again when the registry changes
5. Automatically shuts down when time is up and disables WiFi
1. 엄격한 타이머로 컴퓨터 사용 시간 제한
2. 재생 바로 남은 시간 시각적 표시
3. 남은 시간을 TTS 라이브러리를 사용하여 안내
4. 레지스트리가 변경되면 자동으로 확인하여 다시 차단
5. 시간이 모두 끝나면 자동으로 종료하고 와이파이 비활성화

How to Run file? - 어떻게 파일을 실행시키나요?

This program was written in Python and consists of a main timer program and a program that activates Wi-Fi upon restart.
이 프로그램은 파이썬으로 짜여졌으며, 메인 타이머 프로그램과 재기동시 와이파이를 활성화시키는 프로그램으로 되어있습니다.

1. First, go to the PyinstallerFinal file, open the dist file, and open the main file. Then run the main.exe file to run the timer.
   파이인스톨러파이널 파일로 간 다음, dist파일을 열고, 메인 파일을 엽니다. 그리고 main.exe파일을 실행시켜 타이머를 실행시킵니다.
   
-caution- 
The timer must be run with administrator privileges, and once it is running, it cannot be turned off by any means until you restart your computer!
이 타이머는 무조건 관리자 권한으로 실행되어야 하며, 프로그램이 한번 동작하면 모든 방법으로도 컴퓨터를 끌 수 없습니다!
Sometimes Virus Defender recognizes this file as Wactac virus. However, it is a safe file, and the error occurs because it disables the task manager and the related registry.
가끔 바이러스 디펜더가 이 파일을 Wactac 파이러스로 인식할 때가 있습니다. 하지만 안전한 파일이며, 작업관리자를 비활성화하고 관련된 레지스트리를 비활성화하기 때문에 생기는 오류입니다.
#

2. All passwords can be modified in the source code, and password changes are made only once when the timer runs. Next time you run the timer again, you must use the existing password.
모든 비밀번호는 소스코드에서 수정 가능하며, 비밀번호 변경은 타이머가 실행될 때 한번만 변경되는 비밀번호입니다. 다음에 다시 타이머를 실행하면 기존의 비밀번호로 조작하여야 합니다.

3. The password consists of two parts. The password to pause and increase time is 'log4qwer!!@', and the password used to reset the timer is 'reset1234'.
패스워드는 두개로 구성되어 있습니다. 일시정지, 시간 증가를 하는 패스워드는 'log4qwer!!@' 이며, 타이머를 리셋할때 사용되는 비밀번호는 'reset1234' 입니다.

4. You can start, stop, reset and extend the timer using each password.
당신은 각각의 패스워드를 사용하여 타이머를 실행시키고, 정지하고, 리셋하고, 연장할 수 있습니다.

5. When all timers stop, Wi-Fi is automatically disabled. To run Wi-Fi after restarting, run the Wifi.exe file in the Wifi file and re-enable Wi-Fi. The Wi-Fi password is "wifion123asd!!@@".
타이머가 모두 정지되면 자동으로 와이파이가 비활성화됩니다. 재기동 후 와이파이를 실행시키려면 Wifi파일의 Wifi.exe파일을 실행시켜 와이파이를 다시 활성화합니다. 와이파이 비밀번호는 "wifion123asd!!@@"  입니다.
