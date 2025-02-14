import tkinter as tk
import customtkinter as ctk
import asyncio
import websockets
import threading


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Chat")
        self.root.geometry("400x500")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Set up the chat display area
        self.chat_box = ctk.CTkTextbox(self.root, width=380, height=300, state="disabled")
        self.chat_box.grid(row=0, column=0, padx=10, pady=10)

        # Input area for new messages
        self.message_entry = ctk.CTkEntry(self.root, width=300)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)

        # Send button
        self.send_button = ctk.CTkButton(
            self.root, text="Send", command=self.send_message
        )
        self.send_button.grid(row=1, column=1, padx=10)

        # Button to send a predefined message
        self.send_hello_button = ctk.CTkButton(
            self.root, text="Send Hello", command=self.send_hello
        )
        self.send_hello_button.grid(row=2, column=0, padx=10, pady=10)

        # WebSocket connection
        self.ws_url = "ws://localhost:8000/ws/testroom"
        self.websocket = None

    async def connect_to_server(self):
        self.websocket = await websockets.connect(self.ws_url)
        await self.receive_messages()

    async def receive_messages(self):
        while True:
            message = await self.websocket.recv()
            self.display_message(message)

    def send_message(self):
        message = self.message_entry.get()
        print("🐍 self.message_entry", self.message_entry)
        print("🐍 self.message_entry", self.message_entry.get())

        if message:
            asyncio.run(self.websocket.send(message))
            self.display_message(f"You: {message}")
            self.message_entry.delete(0, tk.END)

    def send_hello(self):
        predefined_message = "Hello from the client!"
        asyncio.run(self.websocket.send(predefined_message))
        self.display_message(f"You: {predefined_message}")

    def display_message(self, message):
        self.chat_box.configure(state="normal")
        self.chat_box.insert(tk.END, message + "\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.yview(tk.END)

    def run(self):
        # Start the WebSocket connection in a separate thread
        threading.Thread(target=lambda: asyncio.run(self.connect_to_server())).start()
        self.root.mainloop()


if __name__ == "__main__":
    # Create the GUI window
    root = ctk.CTk()
    chat_app = ChatApp(root)
    chat_app.run()
