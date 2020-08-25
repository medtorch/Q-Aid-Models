import torch
from torch import nn
import os
import time
import copy
import argparse
from torchvision import datasets, models, transforms
from collections import OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument("--data_dir", default="./data", type=str)
parser.add_argument("--num_classes", type=int, default=2)
parser.add_argument("--num_epochs", type=str, default=25)
parser.add_argument("--batch_size", type=int, default=450)
parser.add_argument("--scripted_model_file", type=str, default="scripted_model.pt")
args = parser.parse_args()

data_dir = args.data_dir

num_classes = args.num_classes
batch_size = args.batch_size
num_epochs = args.num_epochs
input_size = 224
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def train_model(model, dataloaders, criterion, optimizer):
    since = time.time()

    val_acc_history = []

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(args.num_epochs):
        for phase in ["train", "val"]:
            if phase == "train":
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == "train"):
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                    _, preds = torch.max(outputs, 1)

                    if phase == "train":
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

            print("{} Loss: {:.4f} Acc: {:.4f}".format(phase, epoch_loss, epoch_acc))

            if phase == "val" and epoch_acc >= best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

            if phase == "val":
                val_acc_history.append(epoch_acc)

        print()

    time_elapsed = time.time() - since
    print(
        "Training complete in {:.0f}m {:.0f}s".format(
            time_elapsed // 60, time_elapsed % 60
        )
    )
    print("Best val Acc: {:4f}".format(best_acc))

    model.load_state_dict(best_model_wts)
    return model, val_acc_history


def get_transforms():
    return {
        "train": transforms.Compose(
            [
                transforms.RandomResizedCrop(input_size),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        ),
        "val": transforms.Compose(
            [
                transforms.Resize(input_size),
                transforms.CenterCrop(input_size),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        ),
    }


def get_model_backbone():
    model = models.densenet121(pretrained=True)
    num_ftrs = model.classifier.in_features

    for param in model.parameters():
        param.requires_grad = False

    model.classifier = nn.Sequential(
        OrderedDict(
            [("drop", nn.Dropout(0.2)), ("class", nn.Linear(num_ftrs, num_classes))]
        )
    )

    return model


def train():
    model = get_model_backbone()
    data_transforms = get_transforms()

    image_datasets = {
        x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
        for x in ["train", "val"]
    }

    dataloaders_dict = {
        x: torch.utils.data.DataLoader(
            image_datasets[x], batch_size=batch_size, shuffle=True, num_workers=4
        )
        for x in ["train", "val"]
    }

    for param in model.parameters():
        param.requires_grad = True

    model = model.to(device)
    optimizer_ft = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    criterion = nn.CrossEntropyLoss()

    model, hist = train_model(model, dataloaders_dict, criterion, optimizer_ft)

    torch.save(
        model.state_dict(),
        os.path.abspath(os.path.dirname(__file__)) + "/saved_state_dict.pt",
    )


def load_classifier(path):
    model = models.densenet121(pretrained=False)
    num_ftrs = model.classifier.in_features
    model.classifier = model.classifier = nn.Sequential(
        OrderedDict(
            [("drop", nn.Dropout(0.2)), ("class", nn.Linear(num_ftrs, num_classes))]
        )
    )
    state_dict = torch.load(path)
    model.load_state_dict(state_dict)
    return model


if __name__ == "__main__":
    train()
