# Table Selector with LLM

This project uses a Large Language Model (LLM) to select the most relevant table, columns, and row labels from a cleaned Excel dataset based on a user question.

## Project Structure

- `config.yml`: Project configuration (LLM, prompt, dataset path)
- `data/W48Tables_Cleaned.xlsx`: Cleaned Excel data with tables
- `extractiontables.py`: Extracts tables and metadata from Excel
- `selecttables.py`: Main script: config → extract → prompt → LLM → output
- `table_selector.txt`: LLM prompt template with instructions and example
- `requirements.txt`: Python dependencies

## Setup

1. Clone the repository and navigate to the project directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place your cleaned Excel file in the `data/` directory (default: `W48Tables_Cleaned.xlsx`).
4. Update `config.yml` with your OpenAI API key and any other settings.

## Usage

Run the main script:
```bash
python selecttables.py
```

This will:
- Load the configuration and dataset
- Extract tables and metadata
- Build a prompt for the LLM
- Query the LLM to select the most relevant table, columns, and row labels for a sample question
- Print the LLM's raw output

## Notes
- The project uses the `aqxle` library to interface with the LLM. Make sure it is installed and configured.
- You can modify the user question in `selecttables.py` or adapt the script for interactive use.

## License
MIT 