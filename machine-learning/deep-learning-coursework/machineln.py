
import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt

dataset = datasets.ImageFolder("malimg_paper_dataset_imgs", transform=transform)
