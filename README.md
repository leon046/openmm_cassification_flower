# openmm_cassification_flower 任务介绍
使用 MMClassification 训练花卉图片分类模型。

学习使用 MMClassification 的文档以及教学视频，整理训练数据集，修改配置文件，基于 MMClassification 提供的预训练模型，在 flowers 数据集上完成分类模型的微调训练。

## 1. 整理 flower 数据集


flower 数据集包含 5 种类别的花卉图像：雏菊 daisy 588张，蒲公英 dandelion 556张，玫瑰 rose 583张，向日葵 sunflower 536张，郁金香 tulip 585张。

数据集下载链接：

- 国际网：https://www.dropbox.com/s/snom6v4zfky0flx/flower_dataset.zip?dl=0
- 国内网：https://pan.baidu.com/s/1RJmAoxCD_aNPyTRX6w97xQ 提取码: 9x5u

#### 对数据集进行划分

1. 将数据集按照 8:2 的比例划分成训练和验证子数据集，并将数据集整理成 ImageNet的格式。这个过程同学们可以通过 Python 或其他脚本程序完成。具体步骤如下：

2. 将训练子集和验证子集放到 train 和 val 文件夹下。

文件结构如下：

```
flower_dataset
|--- classes.txt
|--- train.txt
|--- val.txt
|    |--- train
|    |    |--- daisy
|    |    |    |--- NAME1.jpg
|    |    |    |--- NAME2.jpg
|    |    |    |--- ...
|    |    |--- dandelion
|    |    |    |--- NAME1.jpg
|    |    |    |--- NAME2.jpg
|    |    |    |--- ...
|    |    |--- rose
|    |    |    |--- NAME1.jpg
|    |    |    |--- NAME2.jpg
|    |    |    |--- ...
|    |    |--- sunflower
|    |    |    |--- NAME1.jpg
|    |    |    |--- NAME2.jpg
|    |    |    |--- ...
|    |    |--- tulip
|    |    |    |--- NAME1.jpg
|    |    |    |--- NAME2.jpg
|    |    |    |--- ...
|    |--- val
|    |    |--- daisy
|    |    |    |--- NAME1.jpg
|    |    |    |--- NAME2.jpg
|    |    |    |--- ...
|    |    |--- dandelion
|    |    |    |--- NAME1.jpg
|    |    |    |--- NAME2.jpg
|    |    |    |--- ...
|    |    |--- rose
|    |    |    |--- NAME1.jpg
|    |    |    |--- NAME2.jpg
|    |    |    |--- ...
|    |    |--- sunflower
|    |    |    |--- NAME1.jpg
|    |    |    |--- NAME2.jpg
|    |    |    |--- ...
|    |    |--- tulip
|    |    |    |--- NAME1.jpg
|    |    |    |--- NAME2.jpg
|    |    |    |--- ...
```

3. 创建并编辑标注文件将所有类别的名称写到 `classes.txt` 中，每行代表一个类别。

4. 生成训练（可选）和验证子集标注列表 `train.txt` 和  `val.txt` ，每行应包含一个文件名和其对应的标签。样例：

```
...
daisy/NAME**.jpg 0
daisy/NAME**.jpg 0
...
dandelion/NAME**.jpg 1
dandelion/NAME**.jpg 1
...
rose/NAME**.jpg 2
rose/NAME**.jpg 2
...
sunflower/NAME**.jpg 3
sunflower/NAME**.jpg 3
...
tulip/NAME**.jpg 4
tulip/NAME**.jpg 4
```

为了节约线上时间，这个过程可以在本地完成。

整理完成后，将处理好的数据集迁移到 `mmclassification/data ` 文件夹下。

## 2. 构建模型微调的配置文件

使用 `_base_` 继承机制构建用于微调的配置文件，可以继承任何 MMClassification 提供的基于 ImageNet 的配置文件并进行修改。

### 修改模型配置

修改分类头，将模型适应为 flowers 中的数据类别数。

### 修改数据配置

修改训练和验证集的数据路径，数据集标注列表，以及类别名文件路径。

将评估方法修改为仅使用 top-1 分类错误率。

### 学习率策略

微调一般会使用更小的学习率和更少的训练周期。因此请在配置文件中修改学习率和训练周期。

### 配置预训练模型

从 Model Zoo 中找到原配置文件对应的模型文件，并下载到平台或本地环境中，通常放置在 `checkpoints` 文件夹中。

在配置文件中配置预训练模型的路径，完成 finetune 训练。


## 3. 使用工具进行模型微调

使用 `tools/train.py` 进行模型微调，并通过 `work_dir` 参数指定工作路径，该路径中会保存训练的模型。调整参数，或使用不同的预训练模型，尝试获得更高的分类精度。
