﻿This document outlines the download, extraction, generation, and discrimination tasks required by Homework 2 and guides you to the corresponding Python source codes and relevant files.


Final Dataset: TSV_v2.tsv
Final Report: HW2 FINAL REPORT.pdf




PDFs download (folder name: DownloadedPDFs)
* DownloadedPDFs/download_pdf.py
* Input file: DownloadedPDFs/PMC.csv
* Output file: DownloadedPDFs/PDFs


Tika content extraction (folder name: ExtractedContent)
* ExtractedContent/extract_content.py
* Input file: DownloadedPDFs/PDFs, ExtractedContent/pdfs.csv
* Output file: ExtractedContent/PDFContent


Tika image extraction (folder name: ExtractedImages)
* ExtractedImages/extract_image.py
* Output file: ExtractedImages/PDFImages


Grover text generation (folder name: GeneratedContent)
* GeneratedContent/generate_text_pre.py
* Input file: FakeName.csv
* Output file: new_input.jsonl, GeneratedContent/GeneratedContent


Grover text discriminator (folder name: GroverDiscriminator)
* GroverDiscriminator/test-probs.npy: the machine:human results directly produced from Grover discriminator
* GroverDiscriminator/load_test.py and groverdiscrim_prob.csv: convert test-probs.npy to a csv file generated by load_test.py


DCGAN face generation and Docker image caption(folder name: GANFakepictures)
* GANFakepictures/face_generator.py: generate the new faces
* GANFakepictures/photos_from_epoch_28: faces generated from epoch28 
* GANFakepictures/photos_from_epoch_8: faces generated from epoch8
* GANFakepictures/image_urls.csv and generate_caption.py: load image urls for caption generation
* GANFakepictures/cap.csv and cap2.csv: captions generated from Tika docker through generate_caption.py
* GANFakepictures/Sample.png: screenshot for generation & caption process


LaTeX Generation (folder name: GaneratedLaTex)
* GaneratedLaTex/Generate_tex.py
* Output file: GaneratedLaTex/LaTex


PDF Generation (folder name: GeneratedPDFs)
* GeneratedPDFs/tex-pdf.py
* Output file: GeneratedPDFs/GeneratedPDFs