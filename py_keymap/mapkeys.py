'''
keymap.py
按键精灵
'''
import keyboard
import mouse
import pprint
import json

def load_config(config_file):
    """加载 JSON 配置文件""" 
    try: 
        print("load from " + config_file)
        with open(config_file, 'r', encoding='utf8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("配置文件 config.json 未找到！") 
        return None
    except json.JSONDecodeError: 
        print("配置文件格式错误！") 
        return None
def remap_mouse_position(key, position):
    def handler(event):
        if event.event_type == keyboard.KEY_DOWN:
            mouse.move(position[0], position[1], absolute=True)
        return False
    return keyboard.hook_key(key, handler, suppress=True)

def remap_mouse(key, mouse_action):
    MOVE_DISTANCE = 10      # 鼠标每次移动的像素距离
    SCROLL_AMOUNT = 1       # 滚轮每次滚动的"格数"
    def handler(event):
        if event.event_type == keyboard.KEY_DOWN:
            match mouse_action:
                case "mouse_left_button":
                    mouse.press(mouse.LEFT)
                case "mouse_right_button":
                    mouse.press(mouse.RIGHT)
                case "mouse_middle_button":
                    mouse.press(mouse.MIDDLE)
                case "mouse_scroll_up":
                    mouse.wheel(SCROLL_AMOUNT)
                case "mouse_scroll_down":
                    mouse.wheel(-SCROLL_AMOUNT)
                case "mouse_move_left":
                    mouse.move(-MOVE_DISTANCE, 0, absolute=False)
                case "mouse_move_right":
                    mouse.move(MOVE_DISTANCE, 0, absolute=False)
                case "mouse_move_up":
                    mouse.move(0, -MOVE_DISTANCE, absolute=False)
                case "mouse_move_down":
                    mouse.move(0, MOVE_DISTANCE, absolute=False)
                case _:
                    pass
        else:
            match mouse_action:
                case "mouse_left_button":
                    mouse.release(mouse.LEFT)
                case "mouse_right_button":
                    mouse.release(mouse.RIGHT)
                case "mouse_middle_button":
                    mouse.release(mouse.MIDDLE)
                case "mouse_scroll_up":
                    pass
                    # mouse.wheel(SCROLL_AMOUNT)
                case "mouse_scroll_down":
                    pass
                    # mouse.wheel(-SCROLL_AMOUNT)
                case "mouse_move_left":
                    pass 
                    # mouse.move(-MOVE_DISTANCE, 0, absolute=False)
                case "mouse_move_right":
                    pass 
                    # mouse.move(MOVE_DISTANCE, 0, absolute=False)
                case "mouse_move_up":
                    pass 
                    # mouse.move(0, -MOVE_DISTANCE, absolute=False)
                case "mouse_move_down":
                    pass
                    # mouse.move(0, MOVE_DISTANCE, absolute=False)
                case _:
                    pass
        return False
    return keyboard.hook_key(key, handler, suppress=True)

def map_keys(config_file):
    """只修改按键""" 
    config = load_config(config_file) 
    if not config: 
        return # 配置加载失败，退出
    
    # 监听所有键盘事件并传递配置
    # 按键
    replacement_map = config.get('replacement_map', {})
    if replacement_map:
        print("remap keys: ")
        pprint.pprint(replacement_map)
        for key,val in replacement_map.items():
            keyboard.remap_key(key, val)
    # 鼠标按键和移动
    mouse_map = config.get('mouse_map', {})
    if mouse_map:
        print("remap mouse: ")
        pprint.pprint(mouse_map)
        for key,val in mouse_map.items():
            remap_mouse(key, val)
    # 鼠标定位
    mouse_position = config.get('mouse_position', {})
    if mouse_position:
        print("remap mouse position: ")
        pprint.pprint(mouse_position)
        for key, position in mouse_position.items():
            remap_mouse_position(key, position)

    print("程序已启动，按 Ctrl+C 退出。")

    try: 
        keyboard.wait() 
    except KeyboardInterrupt: 
        print("\n程序已停止。")

if __name__ == "__main__": 
    map_keys("keys_map.json")