# NNDL_HW2
神经网络与深度学习 作业2 <br>
## Faster R-CNN <br>
首先下载数据集，放在根目录 <br>
### 训练
将网盘Faster R-CNN目录下，预训练文件夹内的两个预训练模型放在backbone文件夹下<br>
然后输入命令 <pre><code>python train_resnet50_fpn.py</code></pre>进行训练<br>
### 测试
输入命令<pre><code>python predict.py</code></pre> <br>
## resnet
1.tensorboard可视化
<pre><code>tensorboard --logdir='runs' --port=6006 --host='localhost'</code></pre>

2.baseline训练及测试
<pre><code>python train.py -net resnet18 -gpu -method baseline</code></pre>
<pre><code>python train.py -net resnet18 -gpu -method baseline -resume</code></pre>

3.cutmix训练及测试
<pre><code>python train.py -net resnet18 -gpu -method cutmix</code></pre>
<pre><code>python train.py -net resnet18 -gpu -method cutmix -resume</code></pre>

4.cutout训练及测试
<pre><code>python train.py -net resnet18 -gpu -method cutout</code></pre>
<pre><code>python train.py -net resnet18 -gpu -method cutout -resume</code></pre>

5.mixup训练及测试
<pre><code>python train.py -net resnet18 -gpu -method mixup</code></pre>
<pre><code>python train.py -net resnet18 -gpu -method mixup -resume</code></pre>
