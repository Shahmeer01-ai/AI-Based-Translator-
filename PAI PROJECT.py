from tkinter import *
from tkinter import ttk
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

# Supported languages
LANGUAGES = {
    'English': 'en', 'Urdu': 'ur', 'French': 'fr',
    'Spanish': 'es', 'German': 'de', 'Arabic': 'ar',
    'Hindi': 'hi', 'Chinese': 'zh-CN'
}

# Main window setup
root = Tk()
root.title("AI Language Translator with TTS")
root.geometry("600x500")
root.config(bg="#e0f7fa")

# Function: Translate & Speak
def translate_text():
    try:
        input_text = text_input.get("1.0", END).strip()
        selected_lang = lang_box.get()
        target_lang = LANGUAGES.get(selected_lang, 'en')
        
        if not input_text:
            status_label.config(text="❗ Please enter text.")
            return
        
        translated = GoogleTranslator(source='auto', target=target_lang).translate(input_text)
        text_output.config(state=NORMAL)
        text_output.delete("1.0", END)
        text_output.insert(END, translated)
        text_output.config(state=DISABLED)

        tts = gTTS(text=translated, lang=target_lang)
        tts.save("translated.mp3")
        if os.name == "nt":
            os.system("start translated.mp3")
        elif os.name == "posix":
            os.system("afplay translated.mp3")  # macOS
        else:
            os.system("mpg123 translated.mp3")  # for Linux if mpg123 installed

        status_label.config(text="✅ Translation complete.")
    except Exception as e:
        status_label.config(text=f"❌ Error: {str(e)}")

# Function: Clear All Fields
def clear_fields():
    text_input.delete("1.0", END)
    text_output.config(state=NORMAL)
    text_output.delete("1.0", END)
    text_output.config(state=DISABLED)
    status_label.config(text="🧹 Fields cleared.")

# Heading
Label(root, text="🌐 AI Language Translator", font=("Arial", 18, "bold"), bg="#e0f7fa").pack(pady=10)

# Input text area
Label(root, text="Enter Text:", font=("Arial", 12), bg="#e0f7fa").pack()
text_input = Text(root, height=4, width=60)
text_input.pack(pady=5)

# Language selection dropdown
Label(root, text="Select Target Language:", font=("Arial", 12), bg="#e0f7fa").pack()
lang_box = ttk.Combobox(root, values=list(LANGUAGES.keys()), width=30, state="readonly")
lang_box.set("Urdu")
lang_box.pack(pady=5)

# Buttons: Translate & Clear
btn_frame = Frame(root, bg="#e0f7fa")
btn_frame.pack(pady=10)
Button(btn_frame, text="Translate & Speak", command=translate_text, bg="green", fg="white", width=20).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Clear", command=clear_fields, bg="red", fg="white", width=10).grid(row=0, column=1, padx=5)

# Output text area (read-only)
Label(root, text="Translated Text:", font=("Arial", 12), bg="#e0f7fa").pack()
text_output = Text(root, height=4, width=60, state=DISABLED)
text_output.pack(pady=5)

# Status label
status_label = Label(root, text="", bg="#e0f7fa", fg="blue", font=("Arial", 10, "italic"))
status_label.pack(pady=5)

# Start GUI loop
root.mainloop()