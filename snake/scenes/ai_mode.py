import pygame
import torch
import numpy as np
from pathlib import Path
from snake import settings as s
from snake.scenes.solo_leveling import SoloLeveling
from snake.rl.agent_dqn import DQNAgent

class AIMode:
    def __init__(self, screen, difficulty):
        self.screen = screen
        self.env = SnakeEnv()
        self.agent = DQNAgent() 
        # Nạp model
        model_path = Path(__file__).parent.parent / "model/model.pth"
        self.agent.model.load_state_dict(torch.load(model_path))
        self.agent.model.eval()
        
        self.current_speed = difficulty # AI có thể chạy rất nhanh, bạn nên để speed cao

    def _update_game(self):
        # AI tự đưa ra quyết định tại mỗi khung hình
        self._handle_ai_input()
        
        # Thực hiện bước đi trong môi trường
        state, reward, done, info = self.env.step(self.env.direction)

        if done:
            self.env.reset() # AI tự chơi lại ván mới hoặc hiện Menu

    def run(self):
        while self.running:
            # Vẫn cần pygame.event.get() để tránh bị treo cửa sổ hoặc bấm Esc để thoát
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                if event.key == pygame.K_ESCAPE: self.running = False

            self._update_game()
            self._draw_elements() # Hàm vẽ rắn giống solo_leveling.py
            
            pygame.display.update()
            self.clock.tick(self.current_speed)