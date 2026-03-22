import pymupdf

def extract_text_from_pdf(file_path: str) ->str:
    text=""
    try:
        with pymupdf.open(file_path) as doc:
            for page in doc:
                subText = page.get_text()
                text+=subText
        return text
    except Exception as e:
        print(f"An error occured while extracting text {e}")


def extract_images_from_pdf(file_path: str)->str:
    try:
        with pymupdf.open(file_path) as doc:
            for page_index in range(len(doc)):
                page=doc[page_index]
                image_list=page.get_images()
                
            if(image_list):
                print(f"Found {len(image_list)} images on Page number {page_index}")
            else:
                print(f"No images found at {page_index}")
    except Exception as e:
        print(f"An error occured while extracting images {e}")
        