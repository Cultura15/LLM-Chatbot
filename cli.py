from chatbot.chat_handler import chat
from voice import listen, speak, speak_in_language

BOT_NAME = "Lingua"

MODE_CHAT = "chat"
MODE_TRANSLATE = "translate"


def main():
    current_mode = MODE_CHAT
    
    print("Commands: 'switch to translate mode', or type '/translate'")
    print("Type 'clear' to reset conversation. Ctrl+C to exit.\n")
    
    greet = (
        "Hello! I'm your Japanese language assistant. "
        "Ask me to translate English to Japanese, or chat about Japanese culture!"
    )
    print(f"{BOT_NAME}: {greet}\n")
    speak(greet)
    
    while True:
        try:
            mode_label = "TRANSLATE" if current_mode == MODE_TRANSLATE else "CHAT"
            print(f"[Listening... | Mode: {mode_label}]")
            user_input = listen()
            
            if not user_input:
                print("Sorry, I didn't catch that. Try again!\n")
                continue
            
            print(f"You: {user_input}\n")
            
            if user_input.lower().strip() in ("exit", "quit", "goodbye", "bye"):
                goodbye = "Nice talking to you! Bye!"
                print(f"{BOT_NAME}: {goodbye}\n")
                speak(goodbye)
                break

            if user_input.strip() == "/translate":
                user_input = "switch to translate mode"
            elif user_input.strip() == "/chat":
                user_input = "switch to chat mode"
            
            result = chat(user_input, current_mode=current_mode)
            
            if "mode_change" in result:
                current_mode = result["mode_change"]
                print(f"[Mode: {current_mode.upper()}]")
            
            response = result["response"]
            print(f"{BOT_NAME}: {response}\n")
            speak(response)
            
            if result.get("is_translation") and result.get("translated_word"):
                translated = result["translated_word"]
                pronunciation = result.get("pronunciation", "")
                language = result["language"]
                
                if pronunciation:
                    print(f"  Pronunciation: {pronunciation}\n")
                
                print(f"[Speaking in {language.capitalize()}...]")
                speak_in_language(translated, language)
          
            elif result.get("is_translation") and not result.get("translated_word"):
                pass
            
        except KeyboardInterrupt:
            print("\n")
            goodbye = "Talk to you later! Bye!"
            print(f"{BOT_NAME}: {goodbye}")
            speak(goodbye)
            break

        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
