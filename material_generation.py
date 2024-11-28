# Regenerate the UNSPSC material data file without duplicates
def generate_unique_unspsc_materials(num_entries):
    materials = []
    seen_material_numbers = set()
    
    while len(materials) < num_entries:
        unspsc_code = random.choice(list(unspsc_categories.keys()))
        category_name = unspsc_categories[unspsc_code]
        description = random.choice(descriptions_by_category[unspsc_code])
        material_number = f"{unspsc_code}-{str(len(materials)+1).zfill(4)}"  # Format like UNSPSC-0001, UNSPSC-0002, etc.
        
        if material_number not in seen_material_numbers:
            seen_material_numbers.add(material_number)
            materials.append({
                "material_number": material_number,
                "description": f"{category_name} - {description}"
            })
    
    return materials

# Generate unique materials data based on UNSPSC
unique_unspsc_materials_data = generate_unique_unspsc_materials(1000)

# Save to a new file without duplicates
unique_unspsc_file_path = '/mnt/data/unique_unspsc_materials.json'
with open(unique_unspsc_file_path, "w") as f:
    json.dump(unique_unspsc_materials_data, f, indent=4)

unique_unspsc_file_path

