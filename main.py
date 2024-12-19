import asyncio
from g4f.client import AsyncClient
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import speech_recognition as sr


async def main():
    global question
    question = entry.get()
    text.insert(END, "Вопрос: " + question + "\n\n")
    client = AsyncClient()

    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        stream=True,
    )

    text.insert(END, "Ответ: ")
    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            answer = chunk.choices[0].delta.content
            text.insert(END, answer)

    entry.delete(0, END)
    text.insert(END, "\n\n")
    entry.focus()


def send(event=None):
    if entry.get().lstrip():
        asyncio.run(main())
    entry.focus()


def record_recognition():
    entry.delete(0, END)
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        text_question = recognizer.recognize_google(audio, language="ru-RU")
    except sr.UnknownValueError:
        mb.showerror("Ошибка распознавания", "Не удалось распознать речь")
        return None
    except sr.RequestError as e:
        mb.showerror("Ошибка", f"Ошибка сервиса распознавания: {e}")
        return None
    except Exception as e:
        mb.showerror("Ошибка", f"Непредвиденная ошибка: {e}")
        return None
    entry.insert(END, text_question)
    send()


question = ""

window = Tk()
window.title("AI GPT-3.5")
window.geometry("750x520+300+100")

text = Text(font="Arial 12", wrap="word")
text.pack()
entry = ttk.Entry(width=50, font="Arial 12")
entry.pack()
ttk.Button(text="Отправить", command=send).pack()
ttk.Button(text="Задать вопрос голосом", command=record_recognition).pack()
entry.focus()
entry.bind("<Return>", lambda event: send())

window.mainloop()