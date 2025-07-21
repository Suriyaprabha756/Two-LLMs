import pandas as pd
import re
from typing import Dict, List


def extract_tables_from_excel(file_path: str, sheet_name: str = None) -> Dict[str, pd.DataFrame]:
   """
   Extract tables from a cleaned Excel file into a dictionary.
   """
   if sheet_name:
       df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
   else:
       df = pd.read_excel(file_path, header=None)

   tables = {}
   current_table_title = None
   current_table_headers = None
   current_table_data = []


   for idx, row in df.iterrows():
       row_values = [str(val) if pd.notna(val) else '' for val in row.tolist()]
       is_empty_row = all(val.strip() == '' or val == 'nan' for val in row_values)
       first_cell = row_values[0].strip()
       is_table_title = bool(re.match(r'^Table\s+\d+:', first_cell, re.IGNORECASE))


       if is_table_title:
           if current_table_title and current_table_headers and current_table_data:
               table_df = pd.DataFrame(current_table_data, columns=current_table_headers)
               tables[current_table_title] = table_df
           current_table_title = first_cell
           current_table_headers = None
           current_table_data = []


       elif current_table_title and not current_table_headers and not is_empty_row:
           headers = [val.strip() for val in row_values if val.strip() != '' and val != 'nan']
           if headers:
               current_table_headers = headers


       elif current_table_title and current_table_headers and not is_empty_row:
           data_row = row_values[:len(current_table_headers)]
           cleaned_data = []
           for val in data_row:
               if val == 'nan' or val.strip() == '':
                   cleaned_data.append(None)
               else:
                   try:
                       cleaned_data.append(float(val) if '.' in val else int(val))
                   except (ValueError, TypeError):
                       cleaned_data.append(val.strip())
           current_table_data.append(cleaned_data)


       elif is_empty_row and current_table_title and current_table_headers and current_table_data:
           table_df = pd.DataFrame(current_table_data, columns=current_table_headers)
           tables[current_table_title] = table_df
           current_table_title = None
           current_table_headers = None
           current_table_data = []


   if current_table_title and current_table_headers and current_table_data:
       table_df = pd.DataFrame(current_table_data, columns=current_table_headers)
       tables[current_table_title] = table_df


   return tables


def get_table_metadata(table_dict: Dict[str, pd.DataFrame], sample_rows: int = 2) -> List[Dict]:
   """
   Generate metadata (title, column names, sample rows) for each table.
   Now also includes row labels from the 'Category' column if present.
   """
   metadata = []
   for title, df in table_dict.items():
       row_labels = []
       if "Category" in df.columns:
           row_labels = df["Category"].dropna().astype(str).tolist()  # <-- all labels
       sample = df.head(sample_rows).to_dict(orient="records")
       metadata.append({
           "title": title,
           "columns": list(df.columns),
           "row_labels": row_labels,
           "sample_rows": sample
       })
   return metadata

# Optional: run as script
if __name__ == "__main__":
   file_path = "./W48Tables_Cleaned.xlsx"
   tables_dict = extract_tables_from_excel(file_path)
   print(f"✅ Extracted {len(tables_dict)} tables.")


   print("\n📋 Table Titles:")
   for i, title in enumerate(tables_dict.keys(), 1):
       print(f"{i}. {title}")


   print("\n🧪 Metadata Preview:")
   metadata = get_table_metadata(tables_dict)
   for entry in metadata[:2]:
       print(f"\nTitle: {entry['title']}")
       print("Columns:", entry["columns"])
       print("Sample Rows:", entry["sample_rows"])