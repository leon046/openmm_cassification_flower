import glob
import os
import shutil
import random

train_prop = 0.7
val_prop = 2 / 3
class_name = ['daisy', 'dandelion','rose','sunflower','tulip']
# 这个类别名是要讲顺序的，要按文件夹的字典序来排序。否则会出现loss在降低，但是acc也在降低的情况。

class_num=len(class_name)
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, 'crop_jpgs')
work_dir = os.path.join(root_dir, 'slice_cls_crop_dataset')
if os.path.exists(work_dir):
    shutil.rmtree(work_dir)
os.makedirs(work_dir)


def split():
    class_data_dir = []
    for i in range(class_num):
        class_data_dir.append(os.path.join(data_dir, class_name[i]))
    print(class_data_dir)

    images_data = []
    for i in class_data_dir:
        images_data.append(os.listdir(i))


    train_index, valtest_index, val_index, test_index = [], [], [], []
    for i in range(class_num):
        train_index.append(random.sample(range(len(images_data[i])), int(len(images_data[i]) * train_prop)))
        valtest_index = list(set(range(len(images_data[i]))) - set(train_index[i]))
        val_index.append(random.sample(valtest_index, int(len(valtest_index) * val_prop)))
        test_index.append(list(set(valtest_index) - set(val_index[i])))

    for i in range(class_num):
        os.makedirs(os.path.join(work_dir, "train", class_name[i]))
        os.makedirs(os.path.join(work_dir, "val", class_name[i]))
        os.makedirs(os.path.join(work_dir, "test", class_name[i]))

    for i in range(class_num):
        for j in train_index[i]:
            shutil.copy(os.path.join(class_data_dir[i], images_data[i][j]),
                        os.path.join(work_dir, "train", class_name[i]))
        for j in val_index[i]:
            shutil.copy(os.path.join(class_data_dir[i], images_data[i][j]),
                        os.path.join(work_dir, "val", class_name[i]))
        for j in test_index[i]:
            shutil.copy(os.path.join(class_data_dir[i], images_data[i][j]),
                        os.path.join(work_dir, "test", class_name[i]))

    print('-' * 50)
    for i in range(class_num):
        print('|' + class_name[i] + ' train num' + ': ' + str(len(train_index[i])))
        print('|' + class_name[i] + ' val num' + ': ' + str(len(val_index[i])))
        print('|' + class_name[i] + ' test num' + ': ' + str(len(test_index[i])))
        print()
    print('-' * 50)


def create_clsses_txt():
    with open(os.path.join(work_dir, 'classes.txt'), 'w') as f:
        for i in range(class_num):
            f.write(f'{class_name[i]}\n')
    print('| classes.txt create successful')
    print('| classes.txt path:' + os.path.join(work_dir, 'classes.txt'))
    print('-' * 50)


def create_txt():
    def generate_txt(images_dir, map_dict):
        imgs_dirs = glob.glob(images_dir + "/*/*.jpg")
        # print(imgs_dirs)
        typename = images_dir.split("/")[-1]
        target_txt_path = os.path.join(work_dir, typename + ".txt")
        f = open(target_txt_path, "w")
        for img_dir in imgs_dirs:
            #filename = img_dir.split("/")[-2]       # linux
            filename = img_dir.split("\\")[-2]     # windows
            num = map_dict[filename]
            #relate_name = os.path.join(img_dir.split('/')[-2], img_dir.split('/')[-1])      # linux
            relate_name = os.path.join(img_dir.split('\\')[-2], img_dir.split('\\')[-1])    # windows
            f.write(relate_name + " " + num + "\n")     # windows 保存的下划线是 '\' ，根据自己需求更改


    train_dir = os.path.join(work_dir, "train")
    val_dir = os.path.join(work_dir, "val")
    test_dir = os.path.join(work_dir, "test")

    class_map_dict = {}
    for i in range(class_num):
        class_map_dict[class_name[i]] = str(i)
    generate_txt(images_dir=train_dir, map_dict=class_map_dict)
    generate_txt(images_dir=val_dir, map_dict=class_map_dict)
    generate_txt(images_dir=test_dir, map_dict=class_map_dict)
    print('| train.txt, val.txt, test.txt create successful')
    print('| train dir', train_dir)
    print('| val dir', val_dir)
    print('| test dir', test_dir)
    print('-' * 50)

if __name__ == '__main__':
    split()
    create_clsses_txt()
    create_txt()
