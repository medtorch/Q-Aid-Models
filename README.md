# Q-Aid-Models

Visual Question Answering is a challenging task for modern Machine Learning. It requires an AI system that can understand both text and language, such that it is able to answer text-based questions given the visual context (an image, CT scan, MRI scan etc.).

Researchers are continuously developing many sophisticated methods for VQA, such as Oscar [1] or VL-BERT [2].

Neural network-based approaches do typically require large amounts of data. Due to the fact that medical data is scarce, developing neural-based models for medicine is a lot harder: the models must be accurate using small amounts of data.

Our VQA engine is based on MedVQA, a state-of-the-art model trained on medical images and questions, using Meta-Learning and a Convolutional Autoencoder for representation extraction.

[1]: https://www.microsoft.com/en-us/research/publication/oscar-object-semantics-aligned-pre-training-for-vision-language-tasks/
[2]: https://www.microsoft.com/en-us/research/publication/vl-bert-pre-training-of-generic-visual-linguistic-representations/
[3]: https://github.com/aioz-ai/MICCAI19-MedVQA/tree/c076f2cc174def26fa597fce4235b93f56658cc8
