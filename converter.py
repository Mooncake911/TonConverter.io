# Import Aspose.Words for Python via .NET module
import aspose.words as aw
from pathlib import Path

# Supporting formats
mask_group_1 = [".html", ".odt", ".docx", ".doc", ".txt", ".epub", ".rtf", ".xps", ".md", ".pdf"]
mask_group_2 = [".BMP", ".tiff", ".jpg", ".png", ".gif", ".svg"]


def converter(file_name, mask):
    # Function to convert DataStorage
    try:
        doc = aw.Document(file_name)
        builder = aw.DocumentBuilder(doc)

        if Path(file_name).suffix in mask_group_1:
            if mask in mask_group_1:
                doc.save("DataStorage/{0}{1}".format(Path(file_name).stem, mask))
            elif mask in mask_group_2:
                for page in range(0, doc.page_count):
                    extractedPage = doc.extract_pages(page, 1)
                    extractedPage.save(f"DataStorage/%s/Output_{page + 1}%s" % Path(file_name).stem, mask)

        elif Path(file_name).suffix in mask_group_2:
            shape = builder.insert_image("Input.jpg")
            shape.image_data.save("Output.png")

    except None:
        print("Not correct format")


