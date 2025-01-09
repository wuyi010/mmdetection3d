import json
import pickle



def save_to_pickle(timestamp_dict, file_path):
    # one_line_json = json.dumps(timestamp_dict, separators=(',', ':'))
    with open(file_path, 'wb') as pickle_file:
        pickle.dump(timestamp_dict, pickle_file)
def load_from_pickle(file_path):
    try:
        with open(file_path, 'rb') as pickle_file:
            return pickle.load(pickle_file)
    except Exception as e:
        print(f"无法打开或加载文件: {e}")
        return None  # 如果发生错误，返回 None 或退出
