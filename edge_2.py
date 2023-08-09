import asyncio
import json
import re
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

def remove_brackets_with_numbers(text):
    return re.sub(r'\[\s*\^\d+\^\s*\]', '', text)

async def main():
    # Carica i cookies dal file
    cookies = json.loads(open("bing_cookies.json", encoding="utf-8").read())
    
    while True:
        # Crea il chatbot utilizzando i cookies
        bot = await Chatbot.create(cookies=cookies)
        
        # Interazione con l'utente
        while True:
            prompt = input("> ")
            
            # Verifica se l'utente vuole uscire
            if prompt == "!exit":
                print("Arrivederci!")
                await bot.close()
                return
            
            # Usa il chatbot per generare una risposta
            response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
            
            # Rimuovi le occorrenze [^x^] dalle risposte
            cleaned_response = remove_brackets_with_numbers(response["text"])
            
            # Stampa l'output generato dal chatbot senza le occorrenze
            print(cleaned_response)
            
            # Riavvia automaticamente il chatbot
            await bot.close()
            break

if __name__ == "__main__":
    asyncio.run(main())
