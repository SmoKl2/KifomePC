import customtkinter as ctk

# Configuração da aparência
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Troca de Telas no Mesmo Frame")
        self.geometry("400x300")

        # Container principal para os frames
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Inicializa os frames
        self.frames = {}
        for F in (Frame1, Frame2):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Mostra a primeira tela
        self.show_frame(Frame1)

    def show_frame(self, cont):
        """Traz o frame desejado para a frente"""
        frame = self.frames[cont]
        frame.tkraise()  # Coloca o frame no topo da pilha


# --- Tela 1 ---
class Frame1(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Tela 1", font=("Arial", 20))
        label.pack(pady=20)

        button = ctk.CTkButton(self, text="Ir para Tela 2",
                               command=lambda: controller.show_frame(Frame2))
        button.pack(pady=10)


# --- Tela 2 ---
class Frame2(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Tela 2", font=("Arial", 20))
        label.pack(pady=20)

        button = ctk.CTkButton(self, text="Voltar para Tela 1",
                               command=lambda: controller.show_frame(Frame1))
        button.pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()