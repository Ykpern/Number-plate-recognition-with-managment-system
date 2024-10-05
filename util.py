import string
import easyocr
import re
import numpy as np
import pytesseract


def convol(image, kernel):

    # Flip the kernel
    kernel = np.flipud(np.fliplr(kernel))
    # convolution output
    output = np.zeros_like(image)

    # Add zero padding to the input image
    image_padded = np.zeros((image.shape[0] + 2, image.shape[1] + 2))
    image_padded[1:-1, 1:-1] = image

    # Loop over every pixel of the image
    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            # element-wise multiplication of the kernel and the image
            output[y, x] = (kernel * image_padded[y: y+3, x: x+3]).sum()

    return output


# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=True)
regex = (r"^(0[1-9]|[1-7][0-9]|8[01])((\s?[a-zA-Z]\s?)(\d{4,5})|(\s?[a-zA-Z]{2}\s?)(\d{3,4})|(\s?[a-zA-Z]{3}\s?)(\d{2,"
         r"3}))$")

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'A': '4',
                    'G': '6',
                    'S': '5',
                    'B': '3'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S',
                    '3': 'B'}
dummy = {
    'x': 'X'
}


def write_csv(results, output_path):

    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{}\n'.format('frame_nmr',
                                          'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                          'license_number_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                print(results[frame_nmr][car_id])
                if 'car' in results[frame_nmr][car_id].keys() and \
                        'license_plate' in results[frame_nmr][car_id].keys() and \
                        'text' in results[frame_nmr][car_id]['license_plate'].keys():
                    f.write('{},{},{},{},{}\n'.format(frame_nmr,
                                                      '[{} {} {} {}]'.format(
                                                          results[frame_nmr][car_id]['license_plate']['bbox'][0],
                                                          results[frame_nmr][car_id]['license_plate']['bbox'][1],
                                                          results[frame_nmr][car_id]['license_plate']['bbox'][2],
                                                          results[frame_nmr][car_id]['license_plate']['bbox'][3]),
                                                      results[frame_nmr][car_id]['license_plate']['bbox_score'],
                                                      results[frame_nmr][car_id]['license_plate']['text'],
                                                      results[frame_nmr][car_id]['license_plate']['text_score'])
                            )
        f.close()


def license_complies_format(text):
    """
    Check if the license plate text complies with the required format.

    Args:
        text (str): License plate text.

    Returns:
        bool: True if the license plate complies with the format, False otherwise.

    if len(text) != 7:
        return False

        if (text[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[0] in dict_char_to_int.keys()) and \
       (text[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[1] in dict_char_to_int.keys()):

       (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_int_to_char.keys()) and \
       (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_int_to_char.keys()) and \
       (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys()) and \
       (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys()) and \
       (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys()):
    """

    if re.match(regex, text):
        return True
    else:
        return False


def format_license(text):

    license_plate_ = ''
    if len(text) == 7:
        mapping = {0: dict_char_to_int, 1: dict_char_to_int, 2: dict_int_to_char, 3: dummy,
                   4: dummy, 5: dict_char_to_int, 6: dict_char_to_int
                   }
        for j in [0, 1, 2, 3, 4, 5, 6]:
            if text[j] in mapping[j].keys():
                license_plate_ += mapping[j][text[j]]
            else:
                license_plate_ += text[j]

    elif len(text) == 8:
        mapping = {0: dict_char_to_int, 1: dict_char_to_int, 2: dict_int_to_char, 3: dummy,
                   4: dummy, 5: dict_char_to_int, 6: dict_char_to_int, 7: dict_char_to_int
                   }
        for j in [0, 1, 2, 3, 4, 5, 6, 7]:
            if text[j] in mapping[j].keys():
                license_plate_ += mapping[j][text[j]]
            else:
                license_plate_ += text[j]
    return license_plate_


def read_license_plate(license_plate_crop):
    """
    Read the license plate text from the given cropped image.

    Args:
        license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.

    Returns:
        tuple: Tuple containing the formatted license plate text and its confidence score.
    """

    detections = reader.readtext(license_plate_crop)
    plate_text = ''
    score = None
    for detection in detections:
        bbox, text, score = detection

        text = text.upper().replace(' ', '').replace('_', '').replace('?', '').replace('&', '').replace('%', '').replace('\'', '').replace('.', '').replace('~', '').replace(';', '').replace('(', '').replace(')', '').replace('[)]', '').replace(']', '')
        plate_text += text

    #if license_complies_format(plate_text):
    licence_plate_formatted = format_license(plate_text)
    if license_complies_format(licence_plate_formatted):
        return licence_plate_formatted, score

    return None, None
