from asposewordscloud import WordsApi
from asposewordscloud.models.requests import ConvertDocumentRequest, SplitDocumentOnlineRequest

import aspose.words as aw
from pathlib import Path
import zipfile

app_sid = '2b1b5ec0-821f-4cf7-8640-8f8ef8d1e501'
app_key = 'ef75436211bf551f4b798480d9867547'

words_api = WordsApi(app_sid, app_key)

# Supporting formats
mask_group = [".docx", ".pdf", ".doc", ".html", ".docm", ".dotx", ".dot", ".md", ".rtf", ".odt", ".ott", ".txt",
              ".epub", ".mht", ".mhtml", ".svg"]

mask_group_pic = [".bmp", ".png", ".jpg", ".jpeg", ".gif"]

mask_group_arch = [".zip", ".rar", ".7z", ".tar", ".tar.gz"]

error_convert = """
htm - format is wrong!
mobi - format is wrong!
xht - format is wrong!
xhtml - format is wrong!
chm - format is wrong!
wps - format is wrong!
wpt - format is wrong!
webp - format is wrong!
tiff
"""


def converter(file_path: Path, mask: str) -> None:
    _mask = file_path.suffix
    try:
        if mask in mask_group_arch:
            """ Packing any files or images in an archive """
            with zipfile.ZipFile(file_path.with_suffix(mask), 'w') as out_file:
                out_file.write(file_path)

        elif _mask in mask_group:
            doc = open(file_path, 'rb')
            if mask in mask_group:
                """ Conversion from file to file, without split """
                request = ConvertDocumentRequest(doc, format=mask[1:])
                result = words_api.convert_document(request)
                with open(file_path.with_suffix(mask), 'wb') as out_file:
                    out_file.write(result)
            elif mask in mask_group_pic:
                """ Conversion from file to image, with split in zip """
                request = SplitDocumentOnlineRequest(doc, format=mask[1:], zip_output=True)
                result = words_api.split_document_online(request)
                with open(file_path.with_suffix('.zip'), 'wb') as out_file:
                    out_file.write(list(result.document.values())[0])

                # bytes_io = io.BytesIO(list(result.document.values())[0])
                # zip_file = zipfile.ZipFile(bytes_io)
                # zip_file.extractall('destination_folder')

        elif _mask in mask_group_pic:
            if mask in mask_group:
                """ Conversion from images to file """
                """ Функционал который надо реализовать """
                pass
            elif mask in mask_group_pic:
                """ Conversion from image to image """
                doc = aw.Document()
                builder = aw.DocumentBuilder(doc)
                shape = builder.insert_image(file_path.as_posix())
                with open(file_path.with_suffix(mask), 'wb') as out_file:
                    shape.image_data.save(out_file)


    except:
        print(f'from {_mask} to {mask} - is error!')


"""
from pathlib import Path
for msk in mask_group_pic:
    converter(Path('sample.pdf'), msk)
"""