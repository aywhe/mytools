'''
keymap.py
按键精灵
'''
import keyboard
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
        
def map_keys(config_file):
    """只修改按键""" 
    config = load_config(config_file) 
    if not config: 
        return # 配置加载失败，退出
    replacement_map = config.get('replacement_map', {})
    # 监听所有键盘事件并传递配置 
    print("remap keys: ")
    pprint.pprint(replacement_map)

    for key,val in replacement_map.items():
        keyboard.remap_key(key, val)

    print("程序已启动，按 Ctrl+C 退出。")

    try: 
        keyboard.wait() 
    except KeyboardInterrupt: 
        print("\n程序已停止。")

if __name__ == "__main__": 
    map_keys("remap_keys.json")