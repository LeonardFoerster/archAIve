# archAIve: arXiv AI Summarizer

archAIve is a simple tool to fetch the latest scientific papers from arXiv and summarize their abstracts using a locally-run AI model. It allows you to quickly get the gist of new research without having to read through lengthy papers.

## ✨ Features

- **Comprehensive Coverage**: Access all categories across Computer Science, Mathematics, Physics, and more.
- **AI-Powered Summaries**: Uses a local Hugging Face transformers model (distilbart-cnn-12-6) to generate concise summaries of paper abstracts.
- **Command-Line Interface**: A powerful and easy-to-use CLI for scripting and quick lookups.
- **Save for Later**: Export the generated summaries to a `.txt` file in a directory of your choice.

## ⚙️ Installation

Follow these steps to get archAIve up and running on your local machine.

### 1. Prerequisites

- Python 3.7 or newer
- `pip`

### 2. Clone the Repository

First, clone this repository to your local machine using Git:

```bash
git clone https://github.com/your-username/archAIve.git
cd archAIve
```

### 3. Install Dependencies

Install dependencies by running the following command in your terminal:

```bash
pip install -r requirements.txt
```

**Note**: The first time you run the tool, the script will download the summarization model from Hugging Face, which may take a few minutes and require a stable internet connection.

## 🚀 Usage

The primary way to use archAIve is through its command-line interface.

### Basic Command

Navigate to the `src` directory and run `cli.py` with the following structure:

```bash
python src/cli.py --category <CATEGORY_CODE> --number <NUM_PAPERS> --outdir <SAVE_DIRECTORY>
```

### Arguments

- `-c, --category` (Required): The arXiv category code you want to fetch papers from (e.g., `cs.LG` for Machine Learning).
- `-n, --number` (Optional): The number of papers to fetch. Defaults to 3.
- `-o, --outdir` (Optional): The directory path where the output `.txt` file will be saved. If not specified, the output will only be printed to the console.

### Example

To get the 5 latest papers from the Computer Vision and Pattern Recognition (`cs.CV`) category and save them to a folder named `cv_summaries`, you would run:

```bash
python src/cli.py --category cs.CV --number 5 --outdir ./cv_summaries
```

The tool will then fetch the papers, summarize their abstracts, print the results to your console, and save them in a timestamped `.txt` file inside the `cv_summaries` directory.
