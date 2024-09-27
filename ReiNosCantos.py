import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  

class ReiNosCantosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rei nos Cantos")

        self.root.geometry("900x600")  
        self.root.resizable(False, False) 

        self.card_images = self.load_card_images()

        self.show_welcome_screen()

    def load_card_images(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']  
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']  
        images = {}
        for suit in suits:
            for rank in ranks:
                image_path = f"C:/Users/marin/Documents/ReiNCnts_interface/Rei-nos-Cantos/images/cartas/{rank}_of_{suit}.png"
                image = Image.open(image_path)
                image = image.resize((70, 100), Image.Resampling.LANCZOS)
                images[f"{rank}_of_{suit}"] = ImageTk.PhotoImage(image)

        return images
    
    def load_reverse_card_image(self):
        image = Image.open("C:/Users/marin/Documents/ReiNCnts_interface/Rei-nos-Cantos/images/carta_ao_contrario.png")  
        image = image.resize((90, 120), Image.Resampling.LANCZOS)
        self.card_image = ImageTk.PhotoImage(image)

        self.card_label = tk.Label(self.root, image=self.card_image)
        self.card_label.grid(row=2, column=2)

    def show_welcome_screen(self):
        self.clear_screen()
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        logo_image_path = "C:/Users/marin/Documents/ReiNCnts_interface/Rei-nos-Cantos/images/logo.png"
        logo_image = Image.open(logo_image_path)
        logo_image = logo_image.resize((400, 400), Image.Resampling.LANCZOS) 
        self.logo_photo = ImageTk.PhotoImage(logo_image) 

        self.logo_label = tk.Label(self.root, image=self.logo_photo)
        self.logo_label.grid(row=1, column=0, pady=20)  

        self.start_button = tk.Button(self.root, text="Iniciar Jogo", command=self.show_name_entry_screen)
        self.start_button.grid(row=3, column=0, pady=20)  

    def show_name_entry_screen(self):
        self.clear_screen()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.name_label = tk.Label(self.root, text="Digite seu nome:", font=("Arial", 14))
        self.name_label.grid(row=1, column=0, pady=10)

        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=2, column=0, pady=10)

        self.confirm_button = tk.Button(self.root, text="Confirmar", command=self.confirm_name)
        self.confirm_button.grid(row=3, column=0, pady=20)

    def confirm_name(self):
        self.player_name = self.name_entry.get()
        if not self.player_name:
            messagebox.showwarning("Atenção", "Por favor, insira seu nome.")
        else:
            self.start_game()

    def start_game(self):
        self.clear_screen()

        self.player_label = tk.Label(self.root, text=f"Jogador: {self.player_name}", font=("Arial", 14))
        self.player_label.grid(row=10, column=1, pady=10)

        self.create_game_widgets()

    def create_game_widgets(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(4, weight=1)

        self.card_frames = {}
        for direction in ['Norte', 'Sul', 'Leste', 'Oeste']:
            frame = tk.Frame(self.root, width=100, height=150, relief=tk.RAISED, borderwidth=2)
            frame.grid(row={'Norte': 1, 'Sul': 3, 'Leste': 2, 'Oeste': 2}[direction], 
                    column={'Norte': 2, 'Sul': 2, 'Leste': 3, 'Oeste': 1}[direction], padx=10, pady=10)
            self.card_frames[direction] = frame

        self.place_initial_cards()

        self.load_reverse_card_image()

        self.buy_button = tk.Button(self.root, text="Comprar Carta", command=self.buy_card)
        self.buy_button.grid(row=2, column=2)

        self.place_card_button = tk.Button(self.root, text="Colocar Carta", command=self.place_card)
        self.place_card_button.grid(row=4, column=2, pady=10)

        self.move_card_button = tk.Button(self.root, text="Mover Carta", command=self.move_card)
        self.move_card_button.grid(row=4, column=3, pady=10)

        self.place_king_button = tk.Button(self.root, text="Colocar Rei no Canto", command=self.place_king)
        self.place_king_button.grid(row=4, column=4, pady=10)


    def place_initial_cards(self):
        import random
        directions = ['Norte', 'Sul', 'Leste', 'Oeste']

        random_cards_table = random.sample(list(self.card_images.keys()), 4)

        for i, direction in enumerate(directions):
            card_image = self.card_images[random_cards_table[i]]
            label = tk.Label(self.card_frames[direction], image=card_image)
            label.pack()

        remaining_cards = list(set(self.card_images.keys()) - set(random_cards_table))
        random_cards_hand = random.sample(remaining_cards, 7)

        self.player_hand_frame = tk.Frame(self.root)
        self.player_hand_frame.grid(row=5, column=0, columnspan=4, pady=20)

        for card in random_cards_hand:
            card_image = self.card_images[card]
            label = tk.Label(self.player_hand_frame, image=card_image)
            label.pack(side=tk.LEFT, padx=5)


    def buy_card(self):
        messagebox.showinfo("Ação", "Você comprou uma carta!")

    def place_card(self):
        messagebox.showinfo("Ação", "Você colocou uma carta na mesa!")

    def move_card(self):
        messagebox.showinfo("Ação", "Você moveu uma carta!")

    def place_king(self):
        messagebox.showinfo("Ação", "Você colocou um Rei em um canto!")

    def clear_screen(self):
        """Remove todos os widgets da tela atual."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReiNosCantosApp(root)
    root.mainloop()
