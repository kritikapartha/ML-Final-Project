"""
Download arxiv dataset using tensorflow
https://www.tensorflow.org/datasets/community_catalog/huggingface/scientific_papers 

Other download methods available here:
https://github.com/armancohan/long-summarization
"""
import tensorflow_datasets as tfds

builder = tfds.builder("scientific_papers", data_dir="./dataset")
builder.download_and_prepare(download_dir="./dataset")