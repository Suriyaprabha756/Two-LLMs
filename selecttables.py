import os
import json
import yaml
import aqxle
from extractingtables import extract_tables_from_excel, get_table_metadata

# === Load config ===
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "config.yml")

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# === Set OpenAI API key ===
os.environ["OPENAI_API_KEY"] = config["llm_config"]["codegen_llm"]["params"]["api_key"]

# === Init Aqxle ===
aqxle.init(config_path)

# === Load Excel + extract tables ===
excel_path = os.path.join(base_dir, config["dataset_path"])
table_dict = extract_tables_from_excel(excel_path)
metadata = get_table_metadata(table_dict, sample_rows=2)

# === User question ===
question = "Is there a relationship between commercial attitudes and switching intent?"

# === Load prompt template ===
prompt_path = os.path.join(base_dir, config["llm_config"]["codegen_llm"]["system_prompt"]
)
with open(prompt_path, "r") as f:
    prompt_template = f.read()

# === Inject values into prompt ===
table_blocks = []
for table in metadata:
    row_lines = "\n    - ".join(table["row_labels"][:10])  # Limit to top 10 for brevity
    block = f"""- {table['title']}
  Columns: {table['columns']}
  Row Labels:
    - {row_lines}"""
    table_blocks.append(block)

tables_text = "\n\n".join(table_blocks)
prompt = prompt_template.replace("{{question}}", question).replace("{{metadata}}", tables_text)


# === Ask LLM to select table + columns ===
with aqxle.params(name="table_select", history_length=0, logging=True):
    response = aqxle.llm("codegen_llm", message=prompt)

# === Just print the raw LLM response ===
print("\n🧠 LLM RAW OUTPUT:")
print(response.data)