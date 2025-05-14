import kivy.app
import pygame
from kivy.core.text.text_pygame import pygame_cache
from kivy.uix.screenmanager import ScreenManager, Screen # type: ignore
from kivy.uix.boxlayout import BoxLayout # type: ignore
from kivy.uix.label import Label # type: ignore
from kivy.uix.button import Button # type: ignore
from kivy.uix.textinput import TextInput # type: ignore
import random

truths = [
    "What is your biggest fear?",
    "Have you ever lied to your best friend?",
    "What's your most embarrassing moment?",
    "Have you ever stolen anything?",
    "What is a secret you’ve never told anyone?",
    "Who was your first crush?",
    "What is the most childish thing you still do?"
]

dares = [
    "Do 10 jumping jacks.",
    "Sing a song loudly.",
    "Do your best animal impression.",
    "Spin around 5 times and walk straight.",
    "Say the alphabet backward.",
    "Talk in a funny accent for 1 minute.",
    "Act like a baby for 30 seconds."
]

# Screens
class PlayerInputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Enter number of players:")
        self.input = TextInput(multiline=False, input_filter='int')
        self.button = Button(text="Start Game")
        self.button.bind(on_press=self.start_game)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.input)
        self.layout.add_widget(self.button)
        self.add_widget(self.layout)

    def start_game(self, instance):
        num = self.input.text
        if num.isdigit() and int(num) > 0:
            self.manager.players = [f"Player {i+1}" for i in range(int(num))]
            self.manager.scores = {player: 0 for player in self.manager.players}
            self.manager.current_player_index = 0
            self.manager.current = "game"

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.info_label = Label(text="")
        self.task_label = Label(text="", font_size=18)
        self.truth_button = Button(text="Truth")
        self.dare_button = Button(text="Dare")
        self.done_button = Button(text="Done", disabled=True)
        self.scoreboard_label = Label(text="Scoreboard")

        self.truth_button.bind(on_press=self.show_truth)
        self.dare_button.bind(on_press=self.show_dare)
        self.done_button.bind(on_press=self.next_turn)

        self.layout.add_widget(self.info_label)
        self.layout.add_widget(self.task_label)
        self.layout.add_widget(self.truth_button)
        self.layout.add_widget(self.dare_button)
        self.layout.add_widget(self.done_button)
        self.layout.add_widget(self.scoreboard_label)

        self.add_widget(self.layout)

    def on_enter(self):
        self.update_ui()

    def update_ui(self):
        player = self.manager.players[self.manager.current_player_index]
        self.info_label.text = f"{player}, it's your turn!"
        self.task_label.text = ""
        self.done_button.disabled = True
        self.scoreboard_label.text = self.get_scoreboard()
        self.truth_button.disabled = False
        self.dare_button.disabled = False

    def show_truth(self, instance):
        self.task_label.text = random.choice(truths)
        self.after_choice()

    def show_dare(self, instance):
        self.task_label.text = random.choice(dares)
        self.after_choice()

    def after_choice(self):
        self.truth_button.disabled = True
        self.dare_button.disabled = True
        self.done_button.disabled = False

    def next_turn(self, instance):
        player = self.manager.players[self.manager.current_player_index]
        self.manager.scores[player] += 1
        self.manager.current_player_index = (self.manager.current_player_index + 1) % len(self.manager.players)
        self.update_ui()

    def get_scoreboard(self):
        return "\n".join(f"{p}: {s}" for p, s in self.manager.scores.items())

# Screen Manager
class TruthOrDareApp(kivy.app.App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PlayerInputScreen(name="input"))
        sm.add_widget(GameScreen(name="game"))
        sm.players = []
        sm.scores = {}
        sm.current_player_index = 0
        return sm

if __name__ == '__main__':
    TruthOrDareApp().run()




