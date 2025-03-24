from pathlib import Path
def filepath_to_localpath(filepath):
    """
    Convert a file path to a local path string with escaped backslashes and quotes.
    
    Args:
        filepath (str): The original file path (e.g., "C:\\path\\Data\\file.jpg")
    
    Returns:
        str: The converted path (e.g., "C:\\\\path\\\\data\\\\file.jpg")
    """
    if isinstance(filepath, Path):
        filepath = str(filepath)
    converted_path = f'"{filepath.replace("\\", "\\\\").replace("Data", "data")}"'
    # print(converted_path)  # Optional
    return converted_path

