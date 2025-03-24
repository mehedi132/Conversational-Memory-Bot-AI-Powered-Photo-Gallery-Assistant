import os

def find_path_in_database(image_path, metadata_dict):
    """Find metadata by matching core filename, ignoring timestamps or prefixes."""
    # Extract filename from uploaded path
    uploaded_filename = os.path.basename(image_path.strip('"'))
    # Core name: remove leading timestamp if present (e.g., "1740396390750-")
    if uploaded_filename.count("-") > 1 and uploaded_filename.split("-")[0].isdigit():
        core_uploaded = "-".join(uploaded_filename.split("-")[1:])
    else:
        core_uploaded = uploaded_filename

    # print("Searching for core filename:", core_uploaded)
    # print("Database filenames:", [os.path.basename(k.strip('"')) for k in metadata_dict.keys()])

    for key in metadata_dict:
        db_filename = os.path.basename(key.strip('"'))
        # Core name from database: remove timestamp if present
        if db_filename.count("-") > 1 and db_filename.split("-")[0].isdigit():
            core_db = "-".join(db_filename.split("-")[1:])
        else:
            core_db = db_filename
        
        # Match if core names are equal
        # print("Comparing with uploas filename:", core_db)
        # print("Comparing with database filename:", core_uploaded)
        if core_db == core_uploaded:
            print(f"Match found: {db_filename} matches {uploaded_filename}")
            return metadata_dict[key]

    print("No match found in database")
    return None                       