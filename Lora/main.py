import time
import webbrowser
import speech_recognition as sr
from playsound import playsound
from datetime import datetime

WAKE_WORD = "лора"
TRIGGER_PHRASE = "сколько время"
WAKE_RESPONSE_WAV = "lora_time.wav"  # ваш WAV

r = sr.Recognizer()
mic = sr.Microphone()

# состояние ожидания команды после срабатывания wake word
awaiting_command = {"active": False, "since": None}

def handle_command_text(text):
    text = text.lower()
    print("Распознано:", text)
    if WAKE_WORD in text:
        print("Услышала имя — ожидаю команду...")
        awaiting_command["active"] = True
        awaiting_command["since"] = time.time()
        return

    if awaiting_command["active"]:
        # таймаут ожидания команды (например, 5 сек)
        if time.time() - awaiting_command["since"] > 7:
            print("Время ожидания команды истекло.")
            awaiting_command["active"] = False
            return
        if TRIGGER_PHRASE in text:
            print("Команда распознана — воспроизведение и показ времени")
            try:
                playsound(WAKE_RESPONSE_WAV)
            except Exception as e:
                print("Не удалось воспроизвести WAV:", e)
            webbrowser.open("https://time.is/")
            now = datetime.now().strftime("%H:%M:%S")
            print("Текущее время:", now)
        else:
            print("Команда не распознана. Скажите 'сколько время'.")
        awaiting_command["active"] = False

def callback(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        handle_command_text(text)
    except sr.UnknownValueError:
        # тишина или нечленораздельная речь — ничего не делаем
        pass
    except sr.RequestError as e:
        print("Ошибка сервиса распознавания речи:", e)
    except Exception as e:
        print("Неожиданная ошибка в callback:", e)

def main():
    print("Лора запущена в фоновом режиме. Говорите...")
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
    # запускаем фоновое прослушивание; phrase_time_limit можно подстроить
    stop_listening = r.listen_in_background(mic, callback, phrase_time_limit=6)

    try:
        while True:
            # основной поток может выполнять другие задачи или просто спать
            time.sleep(1)
    except KeyboardInterrupt:
        print("Остановка...")
        stop_listening(wait_for_stop=False)
if __name__ == "__main__":
    main()

        
