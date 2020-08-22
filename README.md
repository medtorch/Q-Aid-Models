# Q-Aid-Models

Q-Aid models are the pytorch modules currently used in the Q-Aid-Core, trained on publicly available datasets. Each model has a brief explanation below and an example of how to make inference on the model.

### Visual Question Answerion :question:

Visual Question Answering is a challenging task for modern Machine Learning. It requires an AI system that can understand both text and language, such that it is able to answer text-based questions given the visual context (an image, CT scan, MRI scan etc.).

Researchers are continuously developing many sophisticated methods for VQA, such as [Oscar](https://www.microsoft.com/en-us/research/publication/oscar-object-semantics-aligned-pre-training-for-vision-language-tasks/) or [VL-BERT](https://www.microsoft.com/en-us/research/publication/vl-bert-pre-training-of-generic-visual-linguistic-representations/).

Neural network-based approaches do typically require large amounts of data. Due to the fact that medical data is scarce, developing neural-based models for medicine is a lot harder: the models must be accurate using small amounts of data.

Our VQA engine is based on MedVQA, a state-of-the-art model trained on medical images and questions, using Meta-Learning and a Convolutional Autoencoder for representation extraction, as presented [here](https://github.com/aioz-ai/MICCAI19-MedVQA/tree/c076f2cc174def26fa597fce4235b93f56658cc8).

### Medical Brain Segmentation

Medical segmentation is the task of highlighting a region or a set of regions with a specific property. While this task is mostly solved in the general-purpose setup, in the medical scene this task is quite hard because of the difficulty of the problem, humans have a bigger error rate when highlighting abnormalities in the brain and the lack of data.

Our model uses an [UNet](https://arxiv.org/pdf/1505.04597.pdf) architecture, a residual network based on downsampling and upsampling that has good performances on the localization of different features, as presented in the Pytorch [hub](https://pytorch.org/hub/mateuszbuda_brain-segmentation-pytorch_unet/), thanks to the work of Mateusz Buda.

The input image is a 3-channel brain MRI image, the output is a one-channel probability map of abnormality regions, being afterwards transformed into a binary segmentation mask.

### Medical Labelling

Medical labelling is the task of choosing what kind of image the user is feeding into the app, the possible labels are brain, chest, breast, eyes, heart, elbow, forearm, hand, humerus, shoulder, wrist. Currently, our VQA model has support only for brain and chest, but we are working on adding support to multiple labels.

Our model uses a Densenet121 architecture from the [torchvision](https://pytorch.org/docs/stable/torchvision/models.html) module, the architecture being proved better in medical imagery by projects like [MONAI](https://github.com/Project-MONAI/MONAI) that uses it extensively.

### Medical Filtering

Medical filtering is the task of labelling images in two sets, medical and non-medical, as we want to filter all non-medical from being fed into the other machine learning models.

Our model uses a Densenet121 architecture from the [torchvision](https://pytorch.org/docs/stable/torchvision/models.html) module.

## Datasets

The datasets used in this project are augumented version of:
* [Tiny ImageNet](https://tiny-imagenet.herokuapp.com/)
* [Medical Decathlon](http://medicaldecathlon.com/)
* [Mednist](https://www.dropbox.com/s/5wwskxctvcxiuea/MedNIST.tar.gz) - the dataset is kindly made available by [Dr. Bradley J. Erickson M.D., Ph.D.](https://www.mayo.edu/research/labs/radiology-informatics/overview) (Department of Radiology, Mayo Clinic) under the Creative Commons [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/).
