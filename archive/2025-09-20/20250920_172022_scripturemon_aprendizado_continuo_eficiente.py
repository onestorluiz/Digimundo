
# Q-Learning Básico para Decisões Estratégicas no Digimundo
class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

    def get_state(self):
        return random.choice(["estado_1", "estado_2", "estado_3"])

    def select_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        if state not in self.q_table:
            self.q_table[state] = [0] * len(self.actions)
        return self.actions[self.q_table[state].index(max(self.q_table[state]))]

    def update_q_value(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = [0] * len(self.actions)
        if next_state not in self.q_table:
            self.q_table[next_state] = [0] * len(self.actions)
        action_index = self.actions.index(action)
        best_next_action = max(self.q_table[next_state])
        self.q_table[state][action_index] = self.q_table[state][action_index] + self.alpha * (reward + self.gamma * best_next_action - self.q_table[state][action_index])

# CLIP para Comparação de Texto e Imagem
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

def load_clip_model():
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
    return model, processor

def process_and_compare_text_image(model, processor, text, image_path):
    image = Image.open(image_path)
    inputs = processor(text=text, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    return probs
