# Crop Weed Classification

This repository uses image data to classify desired crops from unwanted weeds


[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Z75ffmmFIvQZ91ksWE6xCglssYIy89yh?usp=sharing)


## Repository Structure

- scripts: python files for prepocessing the input dataset
- data: folder where the data resides for the prepocessing functions (omitted by `.gitignore`)
- pytorch-vision: open source helper functions

## References

### Data Sources

This project uses images from the [Sugar Beets 2016 Dataset](https://www.ipb.uni-bonn.de/data/sugarbeets2016/). The data can be downloaded [here](https://www.ipb.uni-bonn.de/datasets_IJRR2017/).

```
@article{chebrolu2017ijrr,
title = {Agricultural robot dataset for plant classification, localization and mapping on sugar beet fields},
author = {Nived Chebrolu and Philipp Lottes and Alexander Schaefer and Wera Winterhalter and Wolfram Burgard and Cyrill Stachniss},
journal = {The International Journal of Robotics Research},
year = {2017}
doi = {10.1177/0278364917720510},
}
```

### Developer References

- [PyTorch Vision](https://github.com/pytorch/vision)
- [PyTorch Vision Helper Functions](https://discuss.pytorch.org/t/modulenotfounderror-no-module-named-engine/59564)
- [Example: Image Segmentation in Cancer Patients](https://seymatas.medium.com/pytorch-image-segmentation-tutorial-for-beginners-i-88d07a6a63e4)
- [Example: Semantic Segmentation with PyTorch](https://learnopencv.com/pytorch-for-beginners-semantic-segmentation-using-torchvision/)
- [Tutorial: Object Detection with TorchVision](https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html)
- [Tutorial: Image Classification with PyTorch](https://towardsdatascience.com/a-beginners-tutorial-on-building-an-ai-image-classifier-using-pytorch-6f85cb69cba7)
- [Using Google Colab with GitHub](https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb#scrollTo=8QAWNjizy_3O)
