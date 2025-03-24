

def find_image_in_database(image, metadata_dict) :
    """Find metadata for an image in the metadata dictionary."""
    # print("Searching for image in database:", image)
    # print("type: ",type(image))
    for key in metadata_dict.keys():
        if image==key :
            print("found")
        
       # print(f"Key: {key}, Type: {type(key)}")
    
    if image not in metadata_dict.keys():
        print("DATA NOT FOUND IN DATABASE")
        
        return None
    # print("DATA FOUND IN DATABASE")
   
    return metadata_dict[image]

