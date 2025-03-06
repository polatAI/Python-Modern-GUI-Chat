import socket
import threading
import customtkinter as ctk
from tkinter import simpledialog

# CustomTkinter ayarları
ctk.set_appearance_mode("dark")  # "light" veya "dark" olarak değiştirilebilir
ctk.set_default_color_theme("green")  # Tema seçenekleri: "blue", "dark-blue", "green"

HOST = "127.0.0.1"
PORT = 9090

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        # Kullanıcıdan nickname alma
        self.nickname = simpledialog.askstring("Nickname", "Lütfen bir kullanıcı adı seçin")
        if not self.nickname:
            self.nickname = "Guest"

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = ctk.CTk()
        self.win.title("Modern Chat")
        self.win.geometry("500x600")
        self.win.resizable(False, False)

        # Üst panel (Başlık + Durum)
        self.header_frame = ctk.CTkFrame(self.win, corner_radius=10)
        self.header_frame.pack(pady=10, padx=10, fill="x")

        self.chat_label = ctk.CTkLabel(self.header_frame, text="💬 Sohbet Odası", font=("Arial", 18, "bold"))
        self.chat_label.pack(side="left", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(self.header_frame, text="🟢 Online", font=("Arial", 12), text_color="green")
        self.status_label.pack(side="right", padx=10)

        # Chat Alanı (Mesajları Gösteren Alan)
        self.text_area = ctk.CTkTextbox(self.win, width=480, height=350, state="disabled", wrap="word")
        self.text_area.pack(pady=10, padx=10)

        # Mesaj Gönderme Alanı
        self.input_frame = ctk.CTkFrame(self.win, corner_radius=10)
        self.input_frame.pack(pady=5, padx=10, fill="x")

        self.input_area = ctk.CTkEntry(self.input_frame, width=380, placeholder_text="Mesajınızı yazın...")
        self.input_area.pack(side="left", padx=10, pady=10)
        self.input_area.bind("<Return>", self.write)  # Enter'a basınca mesaj göndersin

        self.send_button = ctk.CTkButton(self.input_frame, text="➤", width=50, command=self.write)
        self.send_button.pack(side="right", padx=10, pady=10)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self, event=None):
        message = self.input_area.get().strip()
        if message:
            self.sock.send(f"{self.nickname}: {message}".encode("UTF-8"))
            self.input_area.delete(0, "end")

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode("UTF-8")
                if message == "NICK":
                    self.sock.send(self.nickname.encode("UTF-8"))
                else:
                    if self.gui_done:
                        self.text_area.configure(state="normal")
                        self.text_area.insert("end", message + "\n")
                        self.text_area.configure(state="disabled")
                        self.text_area.see("end")
            except:
                print("Bağlantı Hatası!")
                self.sock.close()
                break

client = Client(HOST, PORT)
