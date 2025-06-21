# Jira Duplicate Issue Detector

Finds duplicate or near-duplicate Jira tickets by comparing summary/description via semantic similarity.

**How it works:**
- Fetches tickets from Jira
- Embeds text meaning using Sentence Transformers
- Groups similar issues using Agglomerative Clustering

## Usage

1. Install requirements:
    pip install -r requirements.txt

2. Set your Jira credentials and run:
    python main.py

## Testing

    pytest

## Customization

- Adjust the `similarity_threshold` in `main.py` for stricter/looser grouping.
