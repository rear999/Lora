import time
import win32gui
import win32con
import webbrowser
import os
import speech_recognition as sr
from playsound import playsound
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # project
SOUNDS_DIR = (BASE_DIR / "sounds").resolve()

RESPONSES = {
    "time": SOUNDS_DIR/"lora_time.wav",
    "youtube": SOUNDS_DIR/"lora_Tube.wav",
    "translator": SOUNDS_DIR/"lora_Perevod.wav",
    "telegram": SOUNDS_DIR/"lora_TG.wav",
    "calculator": SOUNDS_DIR/"lora_Calkular.wav",
    "window": SOUNDS_DIR/"lora_window.wav"
} 

WAKE_ACTIVATE = "лора"
WAKE_DEACTIVATE = "лора стоп"

COMMANDS = {
    "time": ["сколько время", "который час", "скажи время", "время сейчас", "время"],
    "youtube": ["открой youtube", "запусти youtube", "youtube"],
    "translator": ["открой переводчик", "переведи текст", "переводчик", "запусти переводчик"],
    "telegram": ["открой telegram", "запусти telegram", "открой тг", "telegram", "тг"],
    "calculator": ["открой калькулятор", "запусти калькулятор", "калькулятор"],
    "window":["закрой все окна", "сверни все окна","открой рабочий стол","верни на рабочий стол"]
}

recognizer = sr.Recognizer()
mic = sr.Microphone()

# флаг режима: True — слушаем и выполняем команды; False — игнорируем команды
active_mode = False

def normalize(text):
    return " ".join(text.lower().strip().split())

def find_command(text):
    for cmd, aliases in COMMANDS.items():
        for alias in aliases:
            if alias in text:
                return cmd
    return None

def play_response_for(cmd):
    wav = RESPONSES.get(cmd)
    if wav and os.path.exists(wav):
        try:
            playsound(wav)
        except Exception as e:
            print("Ошибка при воспроизведении:", e)
            
def handle_command(cmd):
    if cmd == "time":
        play_response_for("time")
        webbrowser.open("https://time.is/")
        now = datetime.now().strftime("%H:%M:%S")
        print("Текущее время:", now)
    elif cmd == "youtube":
        play_response_for("youtube")
        webbrowser.open("https://www.youtube.com/")
    elif cmd == "translator":
        play_response_for("translator")
        webbrowser.open("https://translate.yandex.ru/")
    elif cmd == "telegram":
        play_response_for("telegram")
        webbrowser.open("https://web.telegram.org/")
    elif cmd == "calculator":
        play_response_for("calculator")
        os.name == "nt"
        os.system("start calc")
    elif cmd == "window":
        play_response_for("window")
    try:
        def enum_handler(hwnd, result):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        win32gui.EnumWindows(enum_handler, None)
        print("Все окна свернуты (Windows).")
    except Exception as e:
        print("Ошибка при сворачивании окон (Windows):", e)


def process_recognized(text):
    global active_mode
    text = normalize(text)
    print("Распознано:", text)

    # управление режимом
    if WAKE_ACTIVATE in text:
        if not active_mode:
            active_mode = True
            print("Режим активирован — теперь слушаю команды.")
        else:
            print("Режим уже активен.")
        return

    if WAKE_DEACTIVATE in text:
        if active_mode:
            active_mode = False
            print("Режим деактивирован — больше не слушаю команды.")
        else:
            print("Режим уже неактивен.")
        return

    # если режим неактивен — игнорируем обычные команды
    if not active_mode:
        print("Режим пассивный — команда проигнорирована.")
        return

    # режим активен — ищем и выполняем команду
    cmd = find_command(text)
    if not cmd:
        print("Команда не распознана.")
        return

    print(f"Выполняю команду: {cmd}")
    try:
        handle_command(cmd)
    except Exception as e:
        print("Ошибка при выполнении команды:", e)

def main():
    print("Запуск прослушивания... Говорите.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
    while True:
        with mic as source:
            print("Слушаю...")
            audio = recognizer.listen(source, phrase_time_limit=6)
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            process_recognized(text)
        except sr.UnknownValueError:
            print("Не распознано (шум / молчание).")
        except sr.RequestError as e:
            print("Ошибка сервиса распознавания:", e)
        except Exception as e:
            print("Неожиданная ошибка:", e)
        time.sleep(0.3)

if __name__ == "__main__":
    main()


        
