'''
Для корректной работы проекта необходимо установить CUDA 11.8
Если этот скрипт запустится без ошибок, то torch и CUDA Toolkit установлены корректно.
'''
import torch


torch.zeros(1).cuda()
print(torch.cuda.is_available())
print(torch.cuda.device_count())