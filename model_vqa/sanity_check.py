import base64
import json
from pathlib import Path

import requests
import re
import nltk
import string
import json

from inference import VQA

nltk.download("punkt")
nltk.download("wordnet")


model_root = Path("MICCAI19-MedVQA")

data = json.load(open(model_root / "data_RAD/testset.json"))
img_folder = model_root / "data_RAD/images/"

questions = {}
for entry in data:
    if entry["image_organ"] not in questions:
        questions[entry["image_organ"]] = []

    question = entry["question"]
    filename = img_folder / entry["image_name"]

    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    obj = {
        "image_b64": encoded_string,
        "name": entry["image_name"],
        "question": question,
        "expected_answer": entry["answer"],
    }
    questions[entry["image_organ"]].append(obj)

fail = 0
ok = 0
total = 0

vqa = VQA()

for tag in questions:
    for q in questions[tag]:
        result = vqa.ask(q["question"], q["image_b64"])
        expected = str(q["expected_answer"]).lower()
        actual = str(result).lower()
        if expected == actual:
            print("OK: {}".format(q["name"]))
            ok += 1
        else:
            print("Failed: {}".format(q["name"]))
            fail += 1

        total += 1

print("Total ", total)
print("ok ", ok)
print("failed ", fail)
