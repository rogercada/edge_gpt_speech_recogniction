import speech_recognition as sr

def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("In attesa del comando 'Ok Bing'...")

        while True:
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio, language="it-IT")
                print("Hai detto:", text)

                if "Ok Bing" in text:
                    print("Riconoscimento attivato. Parla ora.")

                    # Ascolta fino a 3 secondi di silenzio
                    audio = r.listen(source, timeout=3)

                    try:
                        transcription = r.recognize_google(audio, language="it-IT")
                        print("Trascrizione:", transcription)
                    except sr.WaitTimeoutError:
                        print("Nessun suono rilevato. Riconoscimento terminato.")

            except sr.UnknownValueError:
                pass  # Ignora quando il riconoscimento non è riuscito
            except sr.RequestError as e:
                print("Errore durante la richiesta a Google Speech Recognition; {0}".format(e))

if __name__ == "__main__":
    main()
