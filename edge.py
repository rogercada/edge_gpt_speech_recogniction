import asyncio
import json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

async def main():
    # Carica i cookies dal file
    cookies = json.loads(open("bing_cookies.json", encoding="utf-8").read())
    
    # Crea il chatbot utilizzando i cookies
    bot = await Chatbot.create(cookies=cookies)
    
    # Ciclo di input dell'utente
    while True:
        prompt = input("> ")
        
        # Verifica se l'utente vuole uscire
        if prompt == "!exit":
            print("Arrivederci!")
            break
        
        # Usa il chatbot per generare una risposta
        response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
        
        # Stampa l'output generato dal chatbot
        print(response["text"])
    
    # Chiudi il chatbot
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
