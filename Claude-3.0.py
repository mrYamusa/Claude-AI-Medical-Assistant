import tkinter as tk
import anthropic
import pyttsx3
import speech_recognition as sr
from PIL import ImageTk, Image

class ClaudeAssistant:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key='Your Claude Anthropic API Key')

    def generate_response(self, prompt):
        message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0,
            system="Respond only as a seasoned medical professional with years of clinical expertise.",
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]}]
        )
        return message.content

class GUI:
    def __init__(self, master, assistant):
        self.master = master
        self.assistant = assistant
        self.engine = pyttsx3.init()

        self.frame = tk.Frame(master, width=150, height=30)
        self.frame.pack()
        self.frame.place(x=20, y=20)

        self.DisplayLogo()
        self.prompt_label = tk.Label(master, text="Enter a prompt:")
        self.prompt_label.pack()
        self.prompt_label.place(x=90, y=200)

        self.prompt_entry = tk.Entry(master, width=50)
        self.prompt_entry.pack()
        self.prompt_entry.place(x=90, y=250)

        self.response_label = tk.Label(master, text="Response:")
        self.response_label.pack()
        self.response_label.place(x=450, y=90)

        self.response_text = tk.Text(master, width=50, height=20)
        self.response_text.pack()
        self.response_text.place(x=450, y=140)

        self.generate_button = tk.Button(master, text="Generate Response", command=self.generate_response1)
        self.generate_button.pack()
        self.generate_button.place(x=90, y=280)

        self.read_button = tk.Button(master, text="Read", command=self.read_response)
        self.read_button.pack()
        self.read_button.place(x=450, y=480)

        self.speak_button = tk.Button(master, text="Speak", command=self.speak_to_text)
        self.speak_button.pack()
        self.speak_button.place(x=210, y=280)


    def generate_response1(self):
        prompt = self.prompt_entry.get()
        response = self.assistant.generate_response(prompt)
        text = response[0].text
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, text)

    def DisplayLogo(self):
        # Opening the image
        image = Image.open('Claude-removebg.png')
        # Resizing the image
        resized_image = image.resize((300, 200))

        self.img1 = ImageTk.PhotoImage(resized_image)
        # A Label Widget to display the Image
        label = tk.Label(self.frame, bg="white", image=self.img1)
        label.pack()

    def read_response(self):
        text = self.response_text.get(1.0, tk.END)
        self.engine.say(text)
        self.engine.runAndWait()

    def speak_to_text(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print("You said: " + text)
                self.prompt_entry.delete(0, tk.END)
                self.prompt_entry.insert(tk.END, text)
                self.generate_response()
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand your audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    api_key = "Your Claude Anthropic API Key"
    assistant = ClaudeAssistant()

    root = tk.Tk()
    root.title("Claude AI Assistant")
    root.config(bg="white")
    root.minsize(height=150, width=300)
    root.geometry("900x540")

    gui = GUI(root, assistant)
    root.mainloop()