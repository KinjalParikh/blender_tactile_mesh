import numpy as np

def generate_data(anchor_point, level_num, repeat_num, shuffle):
    data = []
    for i in range(level_num):
        for _ in range(repeat_num):
            if np.random.rand() > 0.5:
                data.append([anchor_point, i+1])
            else:
                data.append([i+1, anchor_point])
    data = np.array(data)
    print(data.shape)
    if shuffle:
        # shuffle the first axis
        np.random.shuffle(data)
    return data


if __name__ == "__main__":
    anchor_point = 4
    level_num = 7
    repeat_num = 10
    shuffle = True
    print(generate_data(anchor_point, level_num, repeat_num, shuffle))