details_list = []
def similar_images_description_tag(metadata_dict,similar_images):
    for path in similar_images:
        if path in metadata_dict:
            details = {
                "path": path,
                "description": metadata_dict[path]["description"],
                "tag": ", ".join(metadata_dict[path]["tag"])
            }
            details_list.append(details)

     # Return the results
    return details_list
