'''
@Author: xxxmy
@Github: github.com/VectXmy
@Date: 2019-09-26
@Email: xxxmy@foxmail.com
'''
from model.fcos import FCOSDetector
import torch
from dataloader.VOC_dataset import VOCDataset
import math,time
import numpy as np

#from torch.utils.tensorboard import SummaryWriter

train_dataset=VOCDataset("/root/VOC2007",resize_size=[512,800],split='train')
val_dataset=VOCDataset("/root/VOC2007",resize_size=[512,800],split='val')

model=FCOSDetector(mode="training").cuda()
#model.load_state_dict(torch.load("./checkpoints/voc_512x800_loss2.0635.pth"))
optimizer=torch.optim.Adam(model.parameters(),lr=1e-4)

BATCH_SIZE=6
EPOCHS=30
WARMPUP_STEPS_RATIO=0.12
train_loader=torch.utils.data.DataLoader(train_dataset,batch_size=BATCH_SIZE,shuffle=True,collate_fn=train_dataset.collate_fn)
val_loader=torch.utils.data.DataLoader(val_dataset,batch_size=BATCH_SIZE,shuffle=True,collate_fn=val_dataset.collate_fn)
steps_per_epoch=len(train_dataset)//BATCH_SIZE
TOTAL_STEPS=steps_per_epoch*EPOCHS
WARMPUP_STEPS=TOTAL_STEPS*WARMPUP_STEPS_RATIO

GLOBAL_STEPS=1
LR_INIT=5e-5
LR_END=1e-6

#writer=SummaryWriter(log_dir="./logs")

def lr_func():
    if GLOBAL_STEPS<WARMPUP_STEPS:
        lr=GLOBAL_STEPS/WARMPUP_STEPS*LR_INIT
    else:
        lr=LR_END+0.5*(LR_INIT-LR_END)*(
            (1+math.cos((GLOBAL_STEPS-WARMPUP_STEPS)/(TOTAL_STEPS-WARMPUP_STEPS)*math.pi))
        )
    return float(lr)

model.train()
cls_loss_list=[]
cnt_loss_list=[]
reg_loss_list=[]
for epoch in range(EPOCHS):
    for epoch_step,data in enumerate(train_loader):

        batch_imgs,batch_boxes,batch_classes=data
        batch_imgs=batch_imgs.cuda()
        batch_boxes=batch_boxes.cuda()
        batch_classes=batch_classes.cuda()

        lr=lr_func()
        for param in optimizer.param_groups:
            param['lr']=lr
        
        start_time=time.time()

        optimizer.zero_grad()
        losses=model([batch_imgs,batch_boxes,batch_classes])
        loss=losses[-1]
        loss.backward()
        optimizer.step()

        end_time=time.time()
        cost_time=int((end_time-start_time)*1000)

        cls_loss_list.append(losses[0].detach().cpu().numpy())
        cnt_loss_list.append(losses[1].detach().cpu().numpy())
        reg_loss_list.append(losses[2].detach().cpu().numpy())
        #writer.add_scalar("loss/cls_loss",losses[0],global_step=GLOBAL_STEPS)
        #writer.add_scalar("loss/cnt_loss",losses[1],global_step=GLOBAL_STEPS)
        #writer.add_scalar("loss/reg_loss",losses[2],global_step=GLOBAL_STEPS)
        #writer.add_scalar("lr",lr,global_step=GLOBAL_STEPS)

        GLOBAL_STEPS+=1
    
    torch.save(model.state_dict(),"./FCOS.Pytorch-master"+str(epoch)+".pth")
    np.save('cls_loss'+str(epoch),np.array(cls_loss_list))
    np.save('cnt_loss'+str(epoch),np.array(cnt_loss_list))
    np.save('reg_loss'+str(epoch),np.array(reg_loss_list))
    print("global_steps:%d epoch:%d steps:%d/%d cls_loss:%.4f cnt_loss:%.4f reg_loss:%.4f cost_time:%dms lr=%.4e"%\
            (GLOBAL_STEPS,epoch+1,epoch_step+1,steps_per_epoch,losses[0],losses[1],losses[2],cost_time,lr))
torch.save(model.state_dict(),"./FCOS.Pytorch-master.pth")
np.save('cls_loss',np.array(cls_loss_list))
np.save('cnt_loss',np.array(cnt_loss_list))
np.save('reg_loss',np.array(reg_loss_list))