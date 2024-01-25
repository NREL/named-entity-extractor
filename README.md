
# Named Entity Extractor

## Overview
This repository contains a collection of Jupyter Notebooks and Python scripts for Named Entity Recognition (NER) focused on various domains like Electrical, Plumbing, and HVAC systems. The project utilizes spaCy, a popular library for advanced Natural Language Processing (NLP) in Python, to train and apply custom NER models.

## Key Components
- **Electrical, Plumbing, and HVAC Notebooks**: These Jupyter Notebooks contain the code for training and validating custom NER models tailored to specific domains (Electrical, Plumbing, HVAC). They demonstrate the process of loading training data, updating tokenizer configurations, and applying the trained model to new texts.

- **`disaggregate_units.py`**: A Python script for processing and standardizing units and values in datasets. It includes functions to handle fractions, convert unit strings to standardized forms, and infer missing units based on data patterns.

- **Training and Validation Data**: JSON files containing annotated training and validation data for the NER models.

## Prerequisites
- Python 3.10.10
- spaCy 3.7.2
- Additional dependencies as listed in the respective notebooks and scripts.

## Installation
To set up the environment for this project, follow these steps:
1. Install spaCy and its language models:
   ```bash
   pip install -U spacy
   python -m spacy download en_core_web_lg
   ```
2. Clone the repository:
   ```bash
   git clone https://github.com/NREL/named-entity-extractor.git
   ```
3. Navigate to the cloned directory and install any additional required packages.

## Usage
- Run the Jupyter Notebooks to train or apply the NER models for Electrical, Plumbing, and HVAC data.
- Use `disaggregate_units.py` to process and standardize units in your datasets.

## Contributing
Contributions to this project are welcome. Please ensure to follow the coding standards and submit pull requests for any new features or bug fixes.

## License
This project is distributed under the OpenStudio® License. For more details, see the [LICENSE.md](LICENSE.md) file.

## Contact
- **Author**: [Your Name]
- **Email**: [Your Email]
