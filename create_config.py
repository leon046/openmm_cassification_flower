import os
from mmcv import Config

########################### 下面是一些超参数，可以自行修改  #############################

# model内参数设置
num_classes = 5 # 修改为自己的类别数
topk = (1,)  # 修改为自己的topk,
# datasets内参数设置
root_path = os.getcwd()
model_name = 'convnext-large_64xb64_in1k'  # 改成自己要使用的模型名字
work_dir = os.path.join(root_path, "work_dirs", 'convnext-large_64xb64_in1k_job2')  # 训练保存文件的路径，job1，job2，，自己修改。
baseline_cfg_path = os.path.join('configs', 'convnext', 'convnext-large_64xb64_in1k.py')  # 改成自己要使用的模型的路径
save_cfg_path = os.path.join(work_dir, 'config.py')  # 生成的配置文件保存的路径

train_data_prefix = os.path.join(root_path, 'data', 'thyroid_cls', 'data', 'train')  # 改成自己训练集图片的目录。
val_data_prefix = os.path.join(root_path, 'data', 'thyroid_cls', 'data', 'val')  # 改成自己验证集图片的目录。
test_data_prefix = os.path.join(root_path, 'data', 'thyroid_cls', 'data', 'test')  # 改成自己测试集图片的目录，没有测试机的发，可以用验证集。

train_ann_file = os.path.join(root_path, 'data', 'thyroid_cls', 'data', 'train.txt')  # 修改为自己的数据集的训练集txt文件
val_ann_file = os.path.join(root_path, 'data', 'thyroid_cls', 'data', 'val.txt')  # 修改为自己的数据集的验证集txt文件
test_ann_file = os.path.join(root_path, 'data', 'thyroid_cls', 'data', 'test.txt')  # 修改为自己的数据集的测试集txt文件，没有测试集的话，可以用验证集。

classes = os.path.join(root_path, 'data', 'thyroid_cls', 'data', 'classes.txt')  # 在自己的数据集目录下创建一个类别文件classes.txt，每行一个类别。

# 去找个网址里找你对应的模型的网址: https://mmclassification.readthedocs.io/en/latest/model_zoo.html
# 下载下来后，放到work_dir下面，并把名字改为checkpoint.pth。
load_from = os.path.join(work_dir, 'checkpoint.pth')

#  一些超参数，可以自行修改
gpu_num = 1  # 修改为自己的gpu数量
total_epochs = 100  # 改成自己想训练的总epoch数
batch_size = 2 ** 4  # 根据自己的显存，改成合适数值，建议是2的倍数。
num_worker = 8  # 比batch_size小，可以根据CPU核心数调整。
log_interval = 5  # 日志打印的间隔
checkpoint_interval = 15  # 权重文件保存的间隔


# lr = 0.02  # 学习率


########################### 上边是一些超参数，可以自行修改  #############################


def create_config():
    cfg = Config.fromfile(baseline_cfg_path)

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    cfg.work_dir = work_dir

    # model内参数设置
    cfg.model.head.num_classes = num_classes
    cfg.model.head.topk = topk
    if num_classes < 5:
        cfg.evaluation = dict(metric_options={'topk': (1,)})

    # datasets内参数设置
    cfg.data.train.data_prefix = train_data_prefix
    # cfg.data.train.ann_file = train_ann_file
    cfg.data.train.classes = classes

    cfg.data.val.data_prefix = val_data_prefix
    cfg.data.val.ann_file = val_ann_file
    cfg.data.val.classes = classes

    cfg.data.test.data_prefix = test_data_prefix
    cfg.data.test.ann_file = test_ann_file
    cfg.data.test.classes = classes

    cfg.data.samples_per_gpu = batch_size  # Batch size of a single GPU used in testing
    cfg.data.workers_per_gpu = num_worker  # Worker to pre-fetch data for each single GPU

    # 超参数设置
    cfg.log_config.interval = log_interval
    cfg.load_from = load_from
    cfg.runner.max_epochs = total_epochs
    cfg.total_epochs = total_epochs
    # cfg.optimizer.lr = lr
    cfg.checkpoint_config.interval = checkpoint_interval

    # 保存配置文件
    cfg.dump(save_cfg_path)

    print("—" * 80)
    print(f'CONFIG:\n{cfg.pretty_text}')
    print("—" * 80)
    print("| Save config path:", save_cfg_path)
    print("—" * 80)
    print("| Load pretrain model path:", load_from)
    print("—" * 80)
    print('Please download the model pre-training weights, rename the "checkpoint.pth" '
          'and put it in the following directory:', save_cfg_path[:-9])
    print("—" * 80)


if __name__ == '__main__':
    create_config()
