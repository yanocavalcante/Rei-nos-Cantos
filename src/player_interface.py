import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # type: ignore
import os

from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from core.partida import Partida

class PlayerInterface(DogPlayerInterface):
    def __init__(self, root):
        self._root = root
        self._root.title("Rei nos Cantos")
        self._root.geometry("1280x700")
        self._root.configure(bg='darkgreen')

        self._base_dir = os.path.dirname(os.path.abspath(__file__))

        self._center_frame = tk.Frame(self._root, bg='darkgreen')
        self._center_frame.pack(expand=True)  

        self._card_images = self.load_card_images()

        self._dog_server_interface = DogActor()
        
        self._partida = Partida()
        
        self.show_welcome_screen()

    def load_card_images(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        images = {}
        for suit in suits:
            for rank in ranks:
                image_path = os.path.join(self._base_dir, "images", "cartas", f"{rank}_of_{suit}.png")
                image = Image.open(image_path)
                image = image.resize((70, 100), Image.Resampling.LANCZOS)
                images[f"{rank}_of_{suit}"] = ImageTk.PhotoImage(image)
        return images

    def load_reverse_card_image(self):
        image = Image.open(os.path.join(self._base_dir, "images", "carta_ao_contrario.png"))
        image = image.resize((90, 120), Image.Resampling.LANCZOS)
        self.card_image = ImageTk.PhotoImage(image)

        self.card_label = tk.Label(self._center_frame, image=self.card_image, bg='darkgreen')
        self.card_label.grid(row=2, column=2)

    def show_welcome_screen(self):
        self.clear_screen()

        logo_image_path = os.path.join(self._base_dir, "images", "logo.png")
        logo_image = Image.open(logo_image_path)
        logo_image = logo_image.resize((500, 500), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)

        self.logo_label = tk.Label(self._center_frame, image=self.logo_photo, bg='darkgreen')
        self.logo_label.grid(row=0, column=0)

        self.name_label = tk.Label(self._center_frame, text="Digite seu nome:", font=("Arial", 14), bg='darkgreen', padx=40)
        self.name_label.grid(row=1, column=0, pady=(0, 10))

        self.name_entry = tk.Entry(self._center_frame)
        self.name_entry.grid(row=2, column=0)

        self.connect_to_dog = tk.Button(self._center_frame, text="Conectar ao Servidor", command=self.confirm_name, bg='#f81313', width=20, height=2)
        self.connect_to_dog.grid(row=3, column=0, columnspan=1, pady=(10, 10))


        self.start_button = tk.Button(self._center_frame, text="Iniciar Jogo", command=self.start_game, bg='#f81313', width=20, height=2)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=(10, 10))

    def confirm_name(self):
        self.player_name = self.name_entry.get()
        if not self.player_name:
            messagebox.showwarning("Atenção", "Por favor, insira seu nome.")
        else:
            message = self._dog_server_interface.initialize(self.player_name, self)
            messagebox.showinfo(message=message)

    def update_player_turn_label(self, action):
        if action == "start":
            self.player_turn_label.config(text=f"{self.player_name}, compre uma carta")
        elif action == "buy_card" or action == "place_card" or action=="place_king" or action=="move_card":
            self.player_turn_label.config(text=f"{self.player_name}, sua vez de jogar")
        elif action == "pass_turn":
            self.player_turn_label.config(text=f"{self.player_name}, compre uma carta")

    def create_game_widgets(self):
        self.card_frames = {}
        for direction in ['Norte', 'Sul', 'Leste', 'Oeste']:
            frame = tk.Frame(self._center_frame, width=150, height=100, relief=tk.RAISED)
            frame.grid(row={'Norte': 1, 'Sul': 3, 'Leste': 2, 'Oeste': 2}[direction],
                        column={'Norte': 2, 'Sul': 2, 'Leste': 3, 'Oeste': 1}[direction], pady=10)
            self.card_frames[direction] = frame

        self.place_initial_cards()
        self.load_reverse_card_image()

        self.buy_button = tk.Button(self._center_frame, text="Comprar Carta", command=self.buy_card, bg="#f81313")
        self.buy_button.grid(row=2, column=2)

        self.place_card_button = tk.Button(self._center_frame, text="Colocar Carta", command=self.place_card, bg="#f81313")
        self.place_card_button.grid(row=5, column=0, pady=10)

        self.place_king_button = tk.Button(self._center_frame, text="Colocar Rei no Canto", command=self.place_king, bg="#f81313")
        self.place_king_button.grid(row=5, column=1, pady=10, padx=(0, 10))

        self.move_card_button = tk.Button(self._center_frame, text="Manipular Cartas", command=self.move_card, bg="#f81313")
        self.move_card_button.grid(row=5, column=2, pady=10, padx=(0, 10))

        self.move_card_button = tk.Button(self._center_frame, text="Passar a Vez", command=self.pass_turn, bg="#f81313")
        self.move_card_button.grid(row=5, column=3, pady=10, padx=(0, 10))

        self.give_up_button = tk.Button(self._center_frame, text="Desistir da Partida", command=self.receber_notificacao_de_abandono, bg="#f81313")
        self.give_up_button.grid(row=5, column=4, pady=10)

    def place_initial_cards(self):
        import random
        directions = ['Norte', 'Sul', 'Leste', 'Oeste']
        random_cards_table = random.sample(list(self._card_images.keys()), 4)

        for i, direction in enumerate(directions):
            card_image = self._card_images[random_cards_table[i]]

            if direction in ['Leste', 'Oeste']:
                pil_image = Image.open(os.path.join(self._base_dir, "images", "cartas", f"{random_cards_table[i]}.png"))
                pil_image = pil_image.resize((70, 100), Image.Resampling.LANCZOS)
                rotated_image = pil_image.rotate(90, expand=True)
                card_image = ImageTk.PhotoImage(rotated_image)

            label = tk.Label(self.card_frames[direction], image=card_image)
            label.pack()

            self.card_frames[direction].image = card_image

        remaining_cards = list(set(self._card_images.keys()) - set(random_cards_table))
        random_cards_hand = random.sample(remaining_cards, 7)

        self.player_hand_frame = tk.Frame(self._center_frame, bg='darkgreen')  
        self.player_hand_frame.grid(row=6, column=0, columnspan=4, pady=20)

        for card in random_cards_hand:
            card_image = self._card_images[card]
            label = tk.Label(self.player_hand_frame, image=card_image, bg='white')  
            label.pack(side=tk.LEFT, padx=5, pady=5)

    def buy_card(self):
        messagebox.showinfo("Ação", "Você comprou uma carta!")
        self.update_player_turn_label("buy_card")

    def place_card(self):
        messagebox.showinfo("Ação", "Você colocou uma carta na mesa!")
        self.update_player_turn_label("place_card")

    def move_card(self):
        messagebox.showinfo("Ação", "Você manipulou uma carta!")

    def place_king(self):
        messagebox.showinfo("Ação", "Você colocou um Rei em um canto!")
        self.update_player_turn_label("place_king")

    def pass_turn(self):
        messagebox.showinfo("Ação", "Você passou a vez!")
        self.update_player_turn_label("pass_turn")

    def clear_screen(self):
        """Remove todos os widgets da tela atual."""
        for widget in self._center_frame.winfo_children():
            widget.destroy()

    def start_game(self):
        print("Clicou no Botão Iniciar Jogo")
        if self._partida.get_partida_em_andamento() == False:
            start_status = self._dog_server_interface.start_match(2)

            if start_status.get_code() == "1" or start_status.get_code() == "0":
                message = start_status.get_message()
            
            else: 
                message = start_status.get_message()
                messagebox.showinfo(message=message)

                self.clear_screen()
                self.player_turn_label = tk.Label(self._center_frame, font=("Arial", 20), bg='darkgreen', wraplength=150, justify='left')
                self.player_turn_label.grid(row=0, column=0, pady=10)
                self.update_player_turn_label("start")
                self.create_game_widgets()

                jogadores = start_status.get_players()
                inicio = self._partida.comecar_partida(jogadores)
                self._dog_server_interface.send_move(inicio)
                # status_jogo = self._partida.obtem_status()    #Não sei pra que serve

    def receive_start(self, start_status):
        jogadores = start_status.get_players()
        self._partida.receive_start(jogadores)

        message = start_status.get_message()
        messagebox.showinfo(message=message)
        self.clear_screen()
        self.player_turn_label = tk.Label(self._center_frame, font=("Arial", 20), bg='darkgreen', wraplength=150, justify='left')
        self.player_turn_label.grid(row=0, column=0, pady=10)
        self.update_player_turn_label("start")
        self.create_game_widgets()

        # status_jogo = self._partida.obtem_status()    #Continuo sem saber pra que serve
    def receive_move(self, a_move):
        print(a_move)
        self._partida.receber_jogada(a_move)
    

    def receber_notificacao_de_abandono(self):
        self._partida.set_partida_em_andamento
        messagebox.showinfo("Ação", "O seu oponente desistiu da partida")
        self._root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayerInterface(root)
    root.mainloop()
