import asyncio
import json
import re
import speech_recognition as sr
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

def remove_brackets_with_numbers(text):
    return re.sub(r'\[\s*\^\d+\^\s*\]', '', text)

def listen_for_trigger_phrase():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ascolto attivatore vocale...")
        audio = r.listen(source, timeout=5)
    try:
        text = r.recognize_google(audio).lower()
        return "ok bing" in text
    except sr.UnknownValueError:
        return False

async def main():
    # Carica i cookies dal file
    cookies = json.loads(open("bing_cookies.json", encoding="utf-8").read())
    
    while True:
        # Aspetta che venga rilevato l'attivatore vocale
        print("In attesa dell'attivatore vocale 'Ok Bing'...")
        trigger_detected = listen_for_trigger_phrase()
        if not trigger_detected:
            print("Attivatore vocale non rilevato.")
            continue
        
        print("Attivatore vocale rilevato. Attendi il comando...")
        
        # Crea il chatbot utilizzando i cookies
        bot = await Chatbot.create(cookies=cookies)
        
        # Interazione con l'utente
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Ascolto...")
                audio = r.listen(source, timeout=3)
            
            try:
                prompt = r.recognize_google(audio)
                print(f"Hai detto: {prompt}")
                
                # Verifica se l'utente ha detto "dimmi"
                if "dimmi" in prompt.lower():
                    print("Dimmi")
                    continue
                
                # Usa il chatbot per generare una risposta
                response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
                
                # Rimuovi le occorrenze [^x^] dalle risposte
                cleaned_response = remove_brackets_with_numbers(response["text"])
                
                # Stampa l'output generato dal chatbot senza le occorrenze
                print(cleaned_response)
                
            except sr.UnknownValueError:
                print("Nessun input rilevato. In attesa...")
            
            except sr.RequestError as e:
                print(f"Errore nella richiesta a Google: {e}")
            
            # Riavvia automaticamente il chatbot
            await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
