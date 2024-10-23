# Compression and Decompression of Large Files

This repository contains a project focused on implementing some methods for compressing and decompressing large files. The goal is to explore and demonstrate the effectiveness of different compression techniques. The project includes three compression methods:

1. **Huffman Coding**
2. **BWT (Burrows-Wheeler Transform)**
3. **MTF + ZRLE (Move-to-Front + Zero-Run Length Encoding)**

## Overview of the Methods

### 1. Huffman Coding
Huffman coding is a lossless data compression algorithm that uses variable-length codes to represent symbols. The method builds a binary tree where the most frequent symbols are assigned shorter codes, while less frequent symbols receive longer codes. This approach reduces the overall number of bits needed to store the data, achieving compression by exploiting symbol frequency.

### 2. BWT (Burrows-Wheeler Transform)
The Burrows-Wheeler Transform is a technique used to improve the efficiency of text compression algorithms. It rearranges the input data into runs of similar characters, making the data more amenable to compression techniques such as Run-Length Encoding. BWT itself does not compress the data but transforms it in a way that other compression algorithms can be more effective.

### 3. MTF + ZRLE (Move-to-Front + Zero-Run Length Encoding)
This method combines two techniques:
- **Move-to-Front (MTF)**: Reorders a sequence of symbols by moving the most recently used symbols to the front. This step helps to cluster identical symbols together, making it easier for subsequent compression.
- **Zero-Run Length Encoding (ZRLE)**: Encodes sequences of zeros (or repeated symbols) more efficiently by representing consecutive occurrences with a count. In this project, ZRLE is implemented with a bijective binary representation to ensure a unique encoding for each sequence.

## How to Use

Each method is implemented as a separate script in this repository:
- `huffman.py` – Implements Huffman coding for compression and decompression.
- `bwt.py` – Implements the Burrows-Wheeler Transform and its inverse for data transformation.
- `zrle_mtf.py` – Combines Move-to-Front and Zero-Run Length Encoding for compression and decompression.

## Dependencies

This project requires Python 3.x and does not rely on any external libraries beyond the standard library. 


