import pygame
import sys
from snake import settings as s
from snake.scenes.solo_leveling import SoloLeveling
from snake.scenes.intro import Intro
from snake.scenes.play_mode import PlayMode 
from snake.scenes.select_info import SelectInfo
from snake.scenes.play_together import PlayTogether 
from snake.scenes.rules import Rules
from snake import save_manager

class SnakeApp:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        pygame.display.set_caption("Mấy con rắn độc")
        self.current_scene_name = "INTRO"
        self.current_scene_obj = None
        self.nickname_player1 = ""
        self.nickname_player2 = ""
        self.selected_mode = None # <--- THÊM BIẾN LƯU CHẾ ĐỘ CHƠI
        self.rules = None
        self.difficulty = None

    def run(self):
        while True:
            # 1. INTRO: Scene Mở đầu (Chọn Play/Load/Quit)
            if self.current_scene_name == "INTRO":
                self.current_scene_obj = Intro(self.screen)
                mode, save_name = self.current_scene_obj.run() # mode: PLAY, LOAD, QUIT, AI

                if mode == "PLAY":
                    self.current_scene_name = "PLAY_MODE" # Chuyển đến Scene Chọn Mode
                elif mode == "LOAD":
                    state = save_manager.load_game(save_name)
                    if state:
                        self.current_scene_obj = SoloLeveling(self.screen, state["nickname"], state, save_name)
                        self.current_scene_name = "SOLO_LEVELING"
                    else:
                        self.current_scene_name = "INTRO"
                elif mode == "AI":
                    self.current_scene_name = "INTRO"
                elif mode == "QUIT":
                    break
            
            # 2. PLAYMODE: Scene Chọn Chế độ (Solo, Battle Royale)
            # Lưu ý: Scene PlayMode phải trả về tên chế độ (e.g., "SOLO_LEVELING")
            elif self.current_scene_name == "PLAY_MODE":
                
                self.current_scene_obj = PlayMode(self.screen)
                self.selected_mode = self.current_scene_obj.run() # Lấy tên mode

                if self.selected_mode in ["SOLO_LEVELING", "PLAY_TOGETHER", "BATTLE_ROYALE"]:
                    self.current_scene_name = "SELECT_INFO" # Chuyển đến select info
                elif self.selected_mode == "QUIT":
                    self.current_scene_name = "INTRO" # Quay lại Intro
                else:
                    self.current_scene_name = "INTRO" # Quay lại nếu người chơi hủy
            
            # 3. PLAYER_SETUP: Scene Nhập Thông tin Người chơi (Phụ thuộc vào mode)
            elif self.current_scene_name == "SELECT_INFO":
                print("ok")
                # Khởi tạo Setup Scene và truyền chế độ đã chọn vào
                print(self.selected_mode)
                self.current_scene_obj = SelectInfo(self.screen, self.selected_mode)
                self.selcected_mode, self.nickname_player1, self.nickname_player2, self.difficulty = self.current_scene_obj.run() # Lấy danh sách thông tin người chơi
                    # Chuyển đến Mode với thông tin người chơi đã nhập
                    
                if self.selected_mode in ["SOLO_LEVELING", "PLAY_TOGETHER", "BATTLE_ROYALE"]:
                    self.current_scene_name = "RULES"
                    print("ko")
                elif self.selected_mode == "QUIT":
                    self.current_scene_name = "PLAY_MODE" # Quay lại PlayMode
                else:
                    self.current_scene_name = "INTRO" # Quay lại nếu hủy
            
            # 4. RULES: Scene Hiển thị Luật Chơi
            elif self.current_scene_name == "RULES":
                self.current_scene_obj = Rules(self.screen, self.selected_mode)
                self.current_scene_obj.run()
                print (self.selected_mode)
                if self.selected_mode in ["SOLO_LEVELING", "PLAY_TOGETHER", "BATTLE_ROYALE"]:
                    if self.selected_mode == "SOLO_LEVELING":
                        self.current_scene_name = "SOLO_LEVELING"
                    elif self.selected_mode == "PLAY_TOGETHER":
                        self.current_scene_name = "PLAY_TOGETHER"
                    elif self.selected_mode == "BATTLE_ROYALE":
                        self.current_scene_name = "BATTLE_ROYALE"
                elif self.selected_mode == "QUIT":
                    print("Quay lại Select Info")
                    self.current_scene_name = "SELECT_INFO" # Quay lại Select Info
                else:
                    self.current_scene_name = "INTRO" # Quay lại nếu hủy
                

            # 5. Scene Chơi Game Chính

            elif self.current_scene_name == "SOLO_LEVELING":
                self.current_scene_obj = SoloLeveling(self.screen, self.nickname_player1, self.difficulty)
                next_scene = self.current_scene_obj.run() 
                self.current_scene_name = next_scene
            elif self.current_scene_name == "PLAY_TOGETHER":
                self.current_scene_obj = PlayTogether(self.screen, self.nickname_player1, self.nickname_player2)
                next_scene = self.current_scene_obj.run()
                self.current_scene_name = next_scene
            elif self.current_scene_name == "BATTLE_ROYALE":
                self.current_scene_obj = PlayTogether(self.screen, self.nickname_player1, self.nickname_player2) # Tạm thời dùng PlayTogether cho Battle Royale
                next_scene = self.current_scene_obj.run()
                self.current_scene_name = next_scene
            
            # Xử lý các trường hợp khác (ví dụ: ERROR)
            else:
                self.current_scene_name = "INTRO"


        pygame.quit()
        sys.exit()