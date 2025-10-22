import time
import webbrowser
import os
import speech_recognition as sr
from playsound import playsound
from datetime import datetime


WAKE_WORD = "лора"
TRIGGER_PHRASE = "сколько время"
TRIGGER_PHRASE1 = "открой youtube"
TRIGGER_PHRASE2 = "открой переводчик"
TRIGGER_PHRASE3 = "открой telegram"
TRIGGER_PHRASE4 = "открой калькулятор"
WAKE_RESPONSE_WAV = "lora_time.wav"  
WAKE_RESPONSE_WAV1 = "lora_Tube.wav"
WAKE_RESPONSE_WAV2 = "lora_Perevod.wav"
WAKE_RESPONSE_WAV3 = "lora_TG.wav"
WAKE_RESPONSE_WAV4 = "lora_Calkular.wav"

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
        if time.time() - awaiting_command["since"] > 7:
            print("Время ожидания команды истекло.")
            awaiting_command["active"] = False
            return
            # таймаут ожидания команды 
        if TRIGGER_PHRASE in text:
            print("Команда распознана — воспроизведение и показ времени")
            try:
                playsound(WAKE_RESPONSE_WAV)
            except Exception as e:
                print("Не удалось воспроизвести WAV:", e)
            webbrowser.open("https://time.is/")
            now = datetime.now().strftime("%H:%M:%S")
            print("Текущее время:", now)
            #время
        if TRIGGER_PHRASE1 in text:
            print("Команда распознана — Открываем ютуб")
            try:
                playsound(WAKE_RESPONSE_WAV1)
            except Exception as e:
                print("Не удалось воспроизвести WAV:", e)
            webbrowser.open("https://www.youtube.com/")
            print("Запрос выполнен")
            #ютуб
        if TRIGGER_PHRASE2 in text:
            print("Команда распознана — Открываем переводчик")
            try:
                playsound(WAKE_RESPONSE_WAV2)
            except Exception as e:
                print("Не удалось воспроизвести WAV:", e)
            webbrowser.open("https://translate.yandex.ru/")
            print("Запрос выполнен")
            #переводчик 
        if TRIGGER_PHRASE3 in text:
            print("Команда распознана — Открываем телеграм")
            try:
                playsound(WAKE_RESPONSE_WAV3)
            except Exception as e:
                print("Не удалось воспроизвести WAV:", e)
            webbrowser.open("https://web.telegram.org/k/")
            print("Запрос выполнен")
            #телеграм
        if TRIGGER_PHRASE4 in text:
            print("Команда распознана — Открываем калькулятор")
            try:
                playsound(WAKE_RESPONSE_WAV4)
            except Exception as e:
                print("Не удалось воспроизвести WAV:", e)
            os.startfile("calc.exe")
            print("Запрос выполнен")
            #калькулятор
        else:
            print("Команда не распознана. Вот список команд: ")
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

        
