import string
import easyocr

reader = easyocr.Reader(['en'], gpu=True)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}
def license_complies_format(text):
    n=len(text)
    for i in range (n):
        if (text[i] in string.ascii_uppercase):
            return True
        elif (text[i] in dict_int_to_char.keys()):
            return True
        elif (text[i] in dict_char_to_int.keys()):
            return True
        else:
            return False


def format_license(text):
    license_plate_ = ''
    n= len(text)
    for j in range(n):
        mapping = {j: dict_int_to_char}
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_


def read_license_plate(license_plate_crop):

    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        bbox, text, score = detection

        text = text.upper().replace(' ', '')
        if license_complies_format(text):
            return format_license(text), score

    return None, None
