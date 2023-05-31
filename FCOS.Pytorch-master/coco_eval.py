import torch
import math,time
import numpy as np
from torch.utils.tensorboard import SummaryWriter
writer=SummaryWriter(log_dir="./logs")
cls_loss=np.load('cls_loss17.npy')
cnt_loss=np.load('cnt_loss17.npy')
reg_loss=np.load('reg_loss17.npy')
cls_loss=torch.tensor(np.expand_dims(cls_loss,1))
cnt_loss=torch.tensor(np.expand_dims(cnt_loss,1))
reg_loss=torch.tensor(np.expand_dims(reg_loss,1))
print(cls_loss.shape)
print(len(reg_loss)/18)
for i in range(len(cls_loss)):
  writer.add_scalar("loss/cls_loss",cls_loss[i],global_step=i%1345)
  writer.add_scalar("loss/cnt_loss",cnt_loss[i],global_step=i%1345)
  writer.add_scalar("loss/reg_loss",reg_loss[i],global_step=i%1345)