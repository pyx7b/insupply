import pandas as pd

# Load the Excel file
excel_file = 'material_list.xlsx'
sheet_name = 'Sheet1'


# Read the Excel file
df = pd.read_excel(excel_file, sheet_name=sheet_name)

#filter record
filtered_df = df[
    (df['GenItemCatGroup'] == 'RP') 
]

# Specify the columns to keep
columns_to_keep = ['material_number', 'description', 'GL Account']

#convert column value to text
filtered_df['material_number'] = filtered_df['material_number'].astype(str)

# Filter the DataFrame to include only these columns
filtered_df = filtered_df[columns_to_keep]

# Convert the filtered DataFrame to JSON
json_data = filtered_df.to_json(orient='records', indent=4)

# Save JSON to a file
with open('output_filtered.json', 'w') as json_file:
    json_file.write(json_data)

print("Selected columns have been converted to JSON successfully!")
