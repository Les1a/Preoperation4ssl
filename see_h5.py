import h5py
import numpy as np

file_path_1 = 'ECD/h5/slider_depth.h5'
file_path_2 = '4.h5'
file_path_3 = 'T_4.h5'


def see_h5(file_path):

    with h5py.File(file_path, 'r') as f:
        print("Attributes:")
        for key, val in f.attrs.items():
            print(key, val)
        print('Keys:', list(f.keys()))
        for key in f.keys():
            print(key)
            if isinstance(f[key], h5py.Group):
                for subkey in f[key].keys():
                    print('  ', subkey)


def trans2ssl(file_path):

    # 打开输入文件和输出文件
    with h5py.File('./data4ssl/' + file_path, "r") as input_file, \
            h5py.File('./data4ssl/' + 'T_' + file_path, "w") as output_file:
        # 创建 "events" 和 "images" 数据集组
        events_group = output_file.create_group("events")
        images_group = output_file.create_group("images")

        # 将 "p", "t", "x", "y" 转换为 "events" 中的数据集
        events_group.create_dataset("ps", data=input_file["p"])
        events_group.create_dataset("ts", data=input_file["t"])
        events_group.create_dataset("xs", data=input_file["x"])
        events_group.create_dataset("ys", data=input_file["y"])

        # 定义属性及其值
        num_events = len(input_file["p"])
        num_pos = np.sum(input_file["p"])
        num_neg = num_events - num_pos
        sensor_resolution = np.array([480, 640])
        t0 = np.min(input_file["t"])
        tk = np.max(input_file["t"])
        duration = tk - t0

        attributes = {
            "duration": duration,
            "num_events": num_events,
            "num_imgs": 0,
            "num_neg": num_neg,
            "num_pos": num_pos,
            "sensor_resolution": sensor_resolution,
            "t0": t0,
            "tk": tk
        }

        for key, val in attributes.items():
            output_file.attrs[key] = val


if __name__ == "__main__":
    trans2ssl(file_path_2)
    see_h5(file_path_3)
