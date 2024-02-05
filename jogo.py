import openai
import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class PokemonRPGApp(App):
    def build(self):
        self.game_state_file = 'game_state.json'
        self.load_game_state()

        self.layout = BoxLayout(orientation='vertical', padding=10)

        # Área para mostrar a história
        self.story_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.75))
        self.story_label = Label(text="Início da aventura...", size_hint=(1, None), halign='left', valign='top')
        self.story_label.bind(size=self.story_label.setter('text_size'))
        self.story_scroll_view = ScrollView(size_hint=(1, 1))
        self.story_scroll_view.add_widget(self.story_label)
        self.story_layout.add_widget(self.story_scroll_view)

        # Área para entrada de texto e botão enviar
        self.input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.25))
        self.text_input = TextInput(size_hint=(0.8, 1), hint_text='Digite sua ação...')
        self.enter_button = Button(text='Enviar', size_hint=(0.2, 1), on_press=self.process_input)
        self.input_layout.add_widget(self.text_input)
        self.input_layout.add_widget(self.enter_button)

        self.layout.add_widget(self.story_layout)
        self.layout.add_widget(self.input_layout)

        self.update_story(initial=True)

        return self.layout

    def load_game_state(self):
        if os.path.exists(self.game_state_file):
            with open(self.game_state_file, 'r') as file:
                self.game_state = json.load(file)
        else:
            self.game_state = {'history': [], 'mode': 'Exploration', 'location': 'Pallet Town'}

    def save_game_state(self):
        with open(self.game_state_file, 'w') as file:
            json.dump(self.game_state, file)

    def process_input(self, instance):
        action_text = self.text_input.text.strip()
        if action_text:
            self.game_state['history'].append(str(action_text))
            self.save_game_state()
            self.update_story()
            self.text_input.text = ''  # Limpa o campo de texto

    def update_story(self, initial=False):
        openai.api_key = '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'
        prompt = self.create_prompt(initial)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}]
            )
            story_update = response.choices[0].message['content']
            self.story_label.text = story_update
        except Exception as e:
            self.story_label.text = f"Erro ao atualizar a história: {str(e)}"

    def create_prompt(self, initial):
        if initial:
            prompt = ("Você é um jovem treinador Pokémon em Pallet Town, iniciando sua jornada no mundo Pokémon. "
                      "Com um espírito aventureiro e seu primeiro Pokémon ao seu lado, você se dirige ao laboratório do Professor Oak "
                      "para pegar seus primeiros suprimentos. Enquanto caminha, você pensa sobre todas as possíveis aventuras que estão à sua frente. "
                      "Chegando lá, o Professor Oak te saúda calorosamente. 'Bem-vindo! Estou tão empolgado por você começar sua jornada. Antes de tudo, "
                      "qual é o seu nome e qual Pokémon você escolhe como seu primeiro companheiro?'")
        else:
            actions_text = ". ".join(self.game_state['history']) + "."
            prompt = (f"Até agora em sua aventura, você já {actions_text} Agora, você se encontra em {self.game_state['location']}, "
                      "ponderando sobre seu próximo movimento. O que você fará a seguir? Lembre-se, suas ações podem levar a novos encontros, "
                      "batalhas ou descobertas. Escolha sabiamente.")
        
        return prompt

if __name__ == '__main__':
    PokemonRPGApp().run()
