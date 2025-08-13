import json
import time
from pynput.keyboard import Listener, KeyCode, Key
from pynput.mouse import Controller, Button
import threading

# ================== 配置 ==================
MAPPING_FILE = "remap_mouse.json"
MOVE_DISTANCE = 10      # 鼠标每次移动的像素距离
SCROLL_AMOUNT = 1       # 滚轮每次滚动的“格数”
REPEAT_DELAY = 0.02     # 按住时连续动作的延迟（秒）

# 初始化鼠标
mouse = Controller()

# 存储当前被按下的键（用于连续动作）
pressed_keys = set()
# 存储线程控制标志
key_threads = {}

# ================== 动作定义 ==================
def mouse_left_click():
    mouse.click(Button.left, 1)

def mouse_right_click():
    mouse.click(Button.right, 1)

def mouse_middle_click():
    mouse.click(Button.middle, 1)

def mouse_scroll_up():
    mouse.scroll(0, SCROLL_AMOUNT)

def mouse_scroll_down():
    mouse.scroll(0, -SCROLL_AMOUNT)

def mouse_move_left():
    mouse.move(-MOVE_DISTANCE, 0)

def mouse_move_right():
    mouse.move(MOVE_DISTANCE, 0)

def mouse_move_up():
    mouse.move(0, -MOVE_DISTANCE)

def mouse_move_down():
    mouse.move(0, MOVE_DISTANCE)

# 动作映射字典（后面从 JSON 补充）
action_map = {
    "mouse_left_click": mouse_left_click,
    "mouse_right_click": mouse_right_click,
    "mouse_middle_click": mouse_middle_click,
    "mouse_scroll_up": mouse_scroll_up,
    "mouse_scroll_down": mouse_scroll_down,
    "mouse_move_left": mouse_move_left,
    "mouse_move_right": mouse_move_right,
    "mouse_move_up": mouse_move_up,
    "mouse_move_down": mouse_move_down,
}

# ================== 连续按键处理 ==================
def start_repeating(key_str):
    """启动一个后台线程，持续执行某个动作（如移动）"""
    if key_str in key_threads and key_threads[key_str].get("running"):
        return  # 已在运行

    stop_event = threading.Event()
    key_threads[key_str] = {"stop_event": stop_event, "running": True}

    def repeat_action():
        action = action_map.get(key_str)
        if not action:
            return
        while not stop_event.is_set():
            action()
            time.sleep(REPEAT_DELAY)

    thread = threading.Thread(target=repeat_action, daemon=True)
    thread.start()

def stop_repeating(key_str):
    """停止连续动作"""
    if key_str in key_threads:
        key_threads[key_str]["stop_event"].set()
        key_threads[key_str]["running"] = False

# ================== 键盘事件处理 ==================
def on_press(key):
    try:
        if isinstance(key, KeyCode):
            char = key.char  # 单字符按键
        else:
            # 处理特殊键（如 Ctrl、Shift）
            # 检查是否按下了 Ctrl+C
            if key == Key.ctrl_l or key == Key.ctrl_r:
                pressed_keys.add('ctrl')
            # 只拦截映射文件中定义的按键
            return key in [Key.ctrl_l, Key.ctrl_r]  # 不在映射中的特殊键不拦截
    except AttributeError:
        return

    # 检查是否同时按下了 Ctrl 和 C
    if char == 'c' and 'ctrl' in pressed_keys:
        print("\n检测到 Ctrl+C，程序退出")
        return False  # 停止监听

    # 如果按键在映射中，则拦截它
    if char in key_mapping:
        action = key_mapping[char]
        
        # 单次触发动作（点击、滚动）
        if "click" in action or "scroll" in action:
            action_map[action]()
        # 连续动作（移动）：启动重复线程
        elif "move" in action:
            if char not in pressed_keys:
                pressed_keys.add(char)
                start_repeating(action)
        
        # 拦截这个按键
        return True
    
    # 不在映射中的按键不拦截
    return None

def on_release(key):
    try:
        if isinstance(key, KeyCode):
            char = key.char
        else:
            # 处理 Ctrl 键释放
            if key == Key.ctrl_l or key == Key.ctrl_r:
                pressed_keys.discard('ctrl')
            # 只拦截映射文件中定义的按键
            return key in [Key.ctrl_l, Key.ctrl_r]  # 不在映射中的特殊键不拦截
    except AttributeError:
        return

    if char == 'c' and 'ctrl' in pressed_keys:
        return False  # 停止监听

    # 如果按键在映射中，则拦截它
    if char in key_mapping:
        action = key_mapping[char]

        # 如果是移动类动作，松开时停止重复
        if "move" in action and char in pressed_keys:
            pressed_keys.discard(char)
            stop_repeating(action)
        
        # 拦截这个按键
        return True
    
    # 不在映射中的按键不拦截
    return None

# ================== 主程序 ==================
if __name__ == "__main__":
    # 读取映射文件
    try:
        with open(MAPPING_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"成功加载映射文件：{MAPPING_FILE}")
        if not config: 
            print(f"错误：JSON 文件格式错误：{e}")
            exit(1)
        key_mapping = config.get('replacement_map', {})
    except FileNotFoundError:
        print(f"错误：找不到文件 {MAPPING_FILE}，请确保它存在。")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"错误：JSON 文件格式错误：{e}")
        exit(1)

    print("按键映射已启动：")
    for k, v in key_mapping.items():
        print(f"    '{k}' → {v.replace('_', ' ').title()}")
    print("按下 Ctrl+C 组合键退出程序...")

    # 启动监听，添加 suppress=True 来阻止按键传递给系统
    with Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\n\n程序已通过 Ctrl+C 退出。")
