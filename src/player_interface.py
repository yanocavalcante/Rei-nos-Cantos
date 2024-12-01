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

        # Frame superior para o player_turn_label
        self._top_frame = tk.Frame(self._root, bg='darkgreen')
        self._top_frame.pack(side=tk.TOP, fill=tk.X)

        # Frame central para os cards
        self._center_frame = tk.Frame(self._root, bg='darkgreen')
        self._center_frame.pack(expand=True)

        # Frame inferior para o player_hand_frame
        self._bottom_frame = tk.Frame(self._root, bg='darkgreen')
        self._bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self._card_images = self.load_card_images()
        self._dog_server_interface = DogActor()
        self._partida = Partida()
        
        self.show_welcome_screen()

    def load_card_images(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
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

    def update_player_turn_label(self, message):
        self.player_turn_label.config(text=f"{self.player_name}, {message}")

    def create_game_widgets(self):
        self.card_frames = {}
        for direction in ['0', '1', '2', '3']:
            frame = tk.Frame(self._center_frame, width=150, height=100, relief=tk.RAISED)
            
            if direction == '0':
                frame.grid(row=0, column=2, rowspan=2, pady=10)
            elif direction == '1':
                frame.grid(row=3, column=2, rowspan=2, pady=10)
            elif direction == '2':
                frame.grid(row=2, column=3, columnspan=2, pady=10)
            elif direction == '3':
                frame.grid(row=2, column=0, columnspan=2, pady=10)

            self.card_frames[direction] = frame

        for canto in ['C0', 'C1', 'C2', 'C3']:
            frame = tk.Frame(self._center_frame, width=150, height=100, relief=tk.RAISED)
            frame.grid(row={'C0': 1, 'C1': 3, 'C2': 3, 'C3': 1}[canto],
                    column={'C0': 3, 'C1': 3, 'C2': 1, 'C3': 1}[canto], pady=10)
            frame.grid_propagate(False)  # Desativa a propagação do tamanho
            self.card_frames[canto] = frame



        self.place_initial_cards()
        self.load_reverse_card_image()

        self.buy_button = tk.Button(self._center_frame, text="Comprar Carta", command=self.buy_card, bg="#f81313")
        self.buy_button.grid(row=2, column=2)
    
    def get_codigo_cartas(self, cartas):
        nome_correto_cartas = []
        for carta in cartas:
            nome_correto_cartas.append(f'{carta.get_numero()}_of_{carta._naipe.value.lower()}')
        return nome_correto_cartas
    
    def get_nome_carta(self, codigo_carta):
        letra_para_naipe = {
            "H": 'hearts',
            "S": 'spades',
            "D": 'diamonds',
            "C": 'clubs',
        }
        letra_naipe = codigo_carta[0]
        numero = codigo_carta[1:]
        
        naipe = letra_para_naipe.get(letra_naipe, "Unknown")
        return f"{numero}_of_{naipe}"
    
    def place_initial_cards(self):
        directions = ['0', '1', '2', '3']
        pilhas_mesa = self._partida._mesa._pilhas[:4]
        cartas_mesa = []

        for pilha in pilhas_mesa:
            cartas_mesa.append(pilha._cartas[0]) 

        nome_png_cartas = self.get_codigo_cartas(cartas_mesa)

        for i, direction in enumerate(directions):
            card_image = self._card_images[nome_png_cartas[i]]

            if direction in ['2', '3']:
                pil_image = Image.open(os.path.join(self._base_dir, "images", "cartas", f"{nome_png_cartas[i]}.png"))
                pil_image = pil_image.resize((70, 100), Image.Resampling.LANCZOS)
                rotated_image = pil_image.rotate(90, expand=True)
                card_image = ImageTk.PhotoImage(rotated_image)

            label = tk.Label(self.card_frames[direction], image=card_image)
            label.pack()
            label.direction = direction

            self.card_frames[direction].image = card_image

        self.atualizar_mao()

    def atualizar_mao(self):
        for widget in self._bottom_frame.winfo_children():
            widget.destroy()

        self.place_card_button = tk.Button(self._bottom_frame, text="Colocar Carta", command=self.place_card, bg="#f81313")
        self.place_card_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.place_king_button = tk.Button(self._bottom_frame, text="Colocar Rei no Canto", command=self.place_king, bg="#f81313")
        self.place_king_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.move_card_button = tk.Button(self._bottom_frame, text="Manipular Cartas", command=self.move_card, bg="#f81313")
        self.move_card_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.pass_turn_button = tk.Button(self._bottom_frame, text="Passar a Vez", command=self.pass_turn, bg="#f81313")
        self.pass_turn_button.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        self.give_up_button = tk.Button(self._bottom_frame, text="Desistir da Partida", command=self.show_welcome_screen, bg="#f81313")
        self.give_up_button.grid(row=0, column=4, padx=10, pady=5, sticky="w")

        self.player_hand_frame = tk.Frame(self._bottom_frame, bg='darkgreen')
        self.player_hand_frame.grid(row=1, column=0, columnspan=3, pady=5)  # Cartas ficam abaixo dos botões

        cartas_mao_jogador = self._partida._jogador_local._cartas
        nome_png_cartas_jogador = self.get_codigo_cartas(cartas_mao_jogador)

        for card in nome_png_cartas_jogador:
            card_image = self._card_images[card]
            label = tk.Label(self.player_hand_frame, image=card_image, bg='white')
            label.carta_nome = card
            label.pack(side=tk.LEFT, padx=5)
    
    def buy_card(self):
        self.update_player_turn_label("é sua vez de jogar")
        dicionario, compra = self._partida.comprar_carta()
        messagebox.showinfo("Ação", dicionario['mensagem'])
        self.atualizar_mao()
        if compra is not None:
            self._dog_server_interface.send_move(compra)

    def selecionar_carta_mao(self):
        self.variavel_carta_selecionada = tk.StringVar() 

        def on_click(event):
            nome_carta_selecionada = event.widget.carta_nome
            self.variavel_carta_selecionada.set(nome_carta_selecionada) 
            messagebox.showinfo("Carta Selecionada", f"Você selecionou a carta: {nome_carta_selecionada}")

        for widget in self.player_hand_frame.winfo_children():
            widget.bind("<Button-1>", on_click)

        # Aguarda até que a variável seja definida (o usuário clique em uma carta)
        self._root.wait_variable(self.variavel_carta_selecionada)

        return self.variavel_carta_selecionada.get()
    
    def selecionar_pilha(self):
        self.pilha_selecionada = tk.StringVar()

        def on_button_click(direction):
            """Define a direção selecionada e destrói os botões."""
            self.pilha_selecionada.set(direction)
            for button in self.selection_buttons.values():
                button.destroy()

        self.selection_buttons = {}

        for direction, frame in self.card_frames.items():
            button = tk.Button(frame, text="Selecionar", command=lambda dir=direction: on_button_click(dir))
            button.place(relx=0.5, rely=0.5, anchor="center")
            self.selection_buttons[direction] = button

        self._root.wait_variable(self.pilha_selecionada)

        return self.pilha_selecionada.get()

    def place_card(self):
        self.update_player_turn_label("selecione uma carta para jogar na mesa!")
        carta_selecionada = self.selecionar_carta_mao()
        self.update_player_turn_label("selecione uma pilha de destino!")
        pilha_selecionada = self.selecionar_pilha()
        dicionario, jogar_carta = self._partida.jogar_carta(carta_selecionada, pilha_selecionada)
        messagebox.showinfo("Ação", dicionario['mensagem'])
        
        if jogar_carta is not None:
            self.place_card_interface(jogar_carta)
            self.atualizar_mao()
            self._dog_server_interface.send_move(jogar_carta)

        self.update_player_turn_label("é sua vez de jogar!")

    def place_card_interface(self, jogar_carta: dict):
        nome_carta = self.get_nome_carta(jogar_carta['cartas'])
        direcao_pilha = jogar_carta['pilha_adiciona']

        card_image = self._card_images[nome_carta]
        if direcao_pilha in ['2', '3']:
            pil_image = Image.open(os.path.join(self._base_dir, "images", "cartas", f"{nome_carta}.png"))
            pil_image = pil_image.resize((70, 100), Image.Resampling.LANCZOS)
            rotated_image = pil_image.rotate(90, expand=True)
            card_image = ImageTk.PhotoImage(rotated_image)

        existing_cards = self.card_frames[direcao_pilha].winfo_children()
        x_offset_increment = 10 
        y_offset_increment = 10  
        if direcao_pilha in ['3']:
            offset_x = 15
            offset_y = 0
            offset_x += len(existing_cards) * x_offset_increment
        if direcao_pilha in ['1']:
            offset_x = 0
            offset_y = -15
            offset_y -= len(existing_cards) * y_offset_increment
        if direcao_pilha in ['0']:
            offset_x = 0
            offset_y = 15
            offset_y += len(existing_cards) * y_offset_increment
        else:
            offset_x = -15
            offset_y = 0
            offset_x -= len(existing_cards) * y_offset_increment

        label = tk.Label(self.card_frames[direcao_pilha], image=card_image)
        label.image = card_image  
        label.place(relx=0.5, rely=0.5, anchor="center", x=offset_x, y=offset_y)

    def move_card(self):
        cartas = self.selecionar_cartas_mesa()
        pilha1 = None
        pilha2 = self.selecionar_destion()
        dicionario, mover = self._partida.mover_cartas(cartas, pilha1, pilha2)
        messagebox.showinfo("Ação", dicionario['mensagem'])
        if mover is not None:
            self._dog_server_interface.send_move(mover)

    def place_king(self):
        self.update_player_turn_label("selecione um Rei para jogar na mesa!")
        carta_selecionada = self.selecionar_carta_mao()
        self.update_player_turn_label("selecione um Canto de destino!")
        pilha_selecionada = self.selecionar_pilha()
        dicionario, rei_no_canto = self._partida.colocar_rei(carta_selecionada, pilha_selecionada)
        messagebox.showinfo("Ação", dicionario['mensagem'])
        
        if rei_no_canto is not None:
            self.place_king_interface(rei_no_canto)
            self.atualizar_mao()
            self._dog_server_interface.send_move(rei_no_canto)

    def place_king_interface(self, rei_no_canto: dict):
        nome_carta = self.get_nome_carta(rei_no_canto['cartas'])
        codp = rei_no_canto['pilha_adiciona']
        card_image = self._card_images[nome_carta]

        if codp in ['C2', 'C3']:
            pil_image = Image.open(os.path.join(self._base_dir, "images", "cartas", f"{nome_carta}.png"))
            pil_image = pil_image.resize((70, 100), Image.Resampling.LANCZOS)
            rotated_image = pil_image.rotate(90, expand=True)
            card_image = ImageTk.PhotoImage(rotated_image)
        
        elif codp in ['C0', 'C1']:
            pil_image = Image.open(os.path.join(self._base_dir, "images", "cartas", f"{nome_carta}.png"))
            pil_image = pil_image.resize((70, 100), Image.Resampling.LANCZOS)
            rotated_image = pil_image.rotate(270, expand=True)
            card_image = ImageTk.PhotoImage(rotated_image)

        existing_cards = self.card_frames[codp].winfo_children()
        x_offset_increment = 10
        y_offset_increment = 10  
        if codp in ['C3']:
            offset_x = 15
            offset_y = 0
            offset_x += len(existing_cards) * x_offset_increment

        elif codp in ['C1']:
            offset_x = 0
            offset_y = -15
            offset_y -= len(existing_cards) * y_offset_increment

        elif codp in ['C0']:
            offset_x = 0
            offset_y = 15
            offset_y += len(existing_cards) * y_offset_increment
        else:
            offset_x = -15
            offset_y = 0
            offset_x -= len(existing_cards) * y_offset_increment

        label = tk.Label(self.card_frames[codp], image=card_image)
        label.image = card_image  
        label.place(relx=0.5, rely=0.5, anchor="center", x=offset_x, y=offset_y)

    def pass_turn(self):
        dicionario, passar = self._partida.passar_a_vez()
        messagebox.showinfo("Ação", dicionario['mensagem'])
        if passar is not None:
            self._dog_server_interface.send_move(passar)
            self.update_player_turn_label("é a vez do seu oponente jogar")

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
                self.player_turn_label = tk.Label(self._top_frame, font=("Arial", 20), bg='darkgreen', wraplength=150, justify='left')
                self.player_turn_label.grid(row=0, column=0, pady=10)
                self.update_player_turn_label("compre uma carta")

                jogadores = start_status.get_players()
                inicio = self._partida.comecar_partida(jogadores)
                self.create_game_widgets()
                self._dog_server_interface.send_move(inicio)
                # status_jogo = self._partida.obtem_status()    #Não sei pra que serve

    def receive_start(self, start_status):
        jogadores = start_status.get_players()
        self._partida.receive_start(jogadores)

        message = start_status.get_message()
        messagebox.showinfo(message=message)
        self.clear_screen()
        self.player_turn_label = tk.Label(self._top_frame, font=("Arial", 20), bg='darkgreen', wraplength=150, justify='left')
        self.player_turn_label.grid(row=0, column=0, pady=10)
        self.update_player_turn_label("é a vez do seu oponente jogar")

        # status_jogo = self._partida.obtem_status()    #Continuo sem saber pra que serve

    def receive_move(self, a_move):
        print(a_move)
        self._partida.receber_jogada(a_move)
        if a_move['tipo_jogada'] == 'inicio':
            self.create_game_widgets()

        elif a_move['tipo_jogada'] == 'jogar':
            self.place_card_interface(a_move)

        elif a_move['tipo_jogada'] == 'rei_no_canto':
            self.place_king_interface(a_move)

        elif a_move['tipo_jogada'] == 'passar':
            self.update_player_turn_label("compre uma carta")
        
    def receber_notificacao_de_abandono(self):
        self._partida.set_partida_em_andamento
        messagebox.showinfo("Ação", "O seu oponente desistiu da partida")
        self._root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayerInterface(root)
    root.mainloop()
