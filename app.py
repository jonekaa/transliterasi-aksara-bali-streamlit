import cv2
import copy
import numpy as np
import streamlit as st

from PIL import Image
from ultralytics import YOLO


def transliterate(results):
    predictions = []
    
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            label = r[0].names[int(box.cls)]
            
            predictions.append([x1.item(),
                               y1.item(),
                               x2.item(),
                               y2.item(),
                               str(label)])
            
    predictions = np.array(predictions)
    
    # Bagi per baris
    words = []
    lines = group_bounding_boxes_by_lines(predictions)
    for i, line in enumerate(lines):
        line = fix_sorting(line)
        
        string_values = [word[-1] for word in line]
        word = read_labels(string_values)
        words.append(word)
        
    return words


def group_bounding_boxes_by_lines(bounding_boxes, line_tolerance=75):
    # Sort berdasarkan y
    bounding_boxes = sorted(bounding_boxes, key=lambda box: float(box[1]))

    lines = []
    current_line = []

    for box in bounding_boxes:
        x_min, y_min, x_max, y_max, label = box

        if not current_line:
            current_line.append((float(x_min), float(
                y_min), float(x_max), float(y_max), str(label)))
        else:
            # Cek jarak atau overlap
            last_box = current_line[-1]
            _, last_y_min, _, last_y_max, label = last_box

            if abs(float(y_min) - float(last_y_min)) <= line_tolerance or abs(float(y_max) - float(last_y_max)) <= line_tolerance:
                current_line.append(box)
            else:
                # If no overlap, finalize the current line and start a new one
                lines.append(current_line)
                current_line = [box]

    if current_line:
        lines.append(current_line)

    return lines


def fix_sorting(bounding_boxes, x_tolerance=1):
    bounding_boxes = sorted(bounding_boxes, key=lambda x: (
        float(x[0]), float(x[1]), float(x[3])))
    bounding_boxes = np.array(bounding_boxes, dtype=object)

    for i in range(len(bounding_boxes)):
        bounding_boxes[i, :4] = bounding_boxes[i, :4].astype(float)

    for i in range(len(bounding_boxes) - 1):
        x1_i, y1_i, _, _, label_i = bounding_boxes[i]
        x1_j, y1_j, _, _, label_j = bounding_boxes[i + 1]

        if 'gantungan' in label_i:
            result = y1_i > y1_j
        else:
            result = y1_i < y1_j

        if abs(x1_i - x1_j) < x_tolerance and result:
            bounding_boxes[i], bounding_boxes[i + 1] = copy.deepcopy(
                bounding_boxes[i + 1]), copy.deepcopy(bounding_boxes[i])

    return bounding_boxes


def read_labels(labels):
    words = []

    for id, label in enumerate(labels):
        # Ketika depan adalah taleng
        if label == 'taleng':
            label = ''

            # Ketika berada di ke dua paling belakang otomatis pasti e
            if len(labels) - id == 2:
                labels[id + 1] = labels[id +
                                        1].replace(list(labels[id + 1])[-1], 'é')
                continue

            elif len(labels) - id > 2:
                # apabila hanya taleng la tedong
                if labels[id + 2] == 'tedong':
                    if 'rambat' in labels[id + 1]:
                        labels[id + 1] = 'n'
                        labels[id + 2] = 'o'
                        continue

                    else:
                        labels[id + 1] = labels[id +
                                                1].replace(list(labels[id + 1])[-1], 'o')
                        labels[id + 2] = ''
                    continue

                elif len(labels) - id > 3:
                    if labels[id + 3] == 'tedong':
                        # diambli ng dan ny saja sehinga lo - ng
                        if 'gantungan-nya' in labels[id + 2] or 'gantungan-nga' in labels[id + 2]:
                            labels[id + 1] = labels[id +
                                                    1].replace(list(labels[id + 1])[-1], '')
                            labels[id + 2] = labels[id + 2][-3:]
                            labels[id + 3] = labels[id +
                                                    2].replace(list(labels[id + 2])[-1], 'o')
                            continue

                        elif 'surang' in labels[id + 2] or 'cecek' in labels[id + 2] or 'bisah' in labels[id + 2]:
                            labels[id + 1] = labels[id +
                                                    1] .replace(list(labels[id + 1])[-1], 'o')
                            labels[id + 3] = ''
                            continue

                        else:
                            labels[id + 1] = labels[id +
                                                    1].replace(list(labels[id + 1])[-1], '')
                            labels[id + 3] = 'o'
                            continue

                    else:
                        labels[id + 1] = labels[id +
                                                1].replace(list(labels[id + 1])[-1], 'é')
                        continue

                else:
                    labels[id + 1] = labels[id +
                                            1].replace(list(labels[id + 1])[-1], 'é')

        elif label == 'ulu':
            last_char = words.pop()
            label = last_char.replace(list(last_char)[-1], 'i')

        elif label == 'suku':
            last_char = words.pop()

            if len(labels) - id >= 2:
                if labels[id + 1] == 'gantungan-pa':
                    label = last_char
                    labels[id + 1] = 'gantungan-sa'

                elif labels[id - 1] == 'cecek-ng-' or labels[id - 1] == 'surang-r-':
                    label = last_char.replace(list(last_char)[1], 'u')

                else:
                    label = last_char.replace(list(last_char)[-1], 'u')

            else:
                label = last_char.replace(list(last_char)[-1], 'u')

        elif label == 'pepet':
            if id >= 1:
                if labels[id - 1] == 'adeg-adeg':
                    labels[id + 1] = labels[id +1].replace(list(labels[id + 1])[-1], 'e')
                    label = ''
                else:
                    last_char = words.pop()
                    label = last_char.replace(list(last_char)[-1], 'e')

        elif label == 'adeg-adeg':
            last_char = words.pop()
            label = last_char.replace(list(last_char)[-1], ' ')

        elif label == 'cecek-ng-':
            last_char = words.pop()
            label = ''.join((last_char, 'ng'))

        elif label == 'surang-r-':
            last_char = words.pop()
            label = ''.join((last_char, 'r'))

        elif label == 'bisah-h-':
            last_char = words.pop()
            label = ''.join((last_char, 'h'))

        elif label == 'na-rambat':
            label = 'na'
        elif label == 'da-madu':
            label = 'dha'
        elif label == 'ta-latik':
            label = 'tha'
        elif label == 'ta-tawa':
            label = 'ta'
        elif label == 'sa-sapa':
            label = 'sa'
        elif label == 'sa-saga':
            label = 'sa'
        elif label == 'ga-gora':
            label = 'ga'
        elif label == 'ba-kembang':
            label = 'ba'
        elif label == 'pa-kapal':
            label = 'pa'
        elif label == 'ca-kaca':
            label = 'ca'
        elif label == 'ja-jera':
            label = 'ja'
        elif label == 'a-kara':
            label = 'a'
        elif label == 'i-kara':
            label = 'i'
        elif label == 'u-kara':
            label = 'u'
        elif label == 'e-kara':
            label = 'e'
        elif label == 'o-kara':
            label = 'o'
        elif label == 'ra-repa':
            label = 'ra'
        elif label == 'le-lenga':
            label = 'le'

        elif label == 'tedong':
            last_char = words.pop()
            label = ''.join((last_char, last_char[-1]))

        elif label == 'gantungan-ha':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'h', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'h', last_char[1:]))

        elif label == 'gantungan-na':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'n', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'n', last_char[1:]))

        elif label == 'gantungan-ca':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'c', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'c', last_char[1:]))

        elif label == 'gantungan-ra':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'r', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'r', last_char[1:]))

        elif label == 'gantungan-ka':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'k', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'k', last_char[1:]))

        elif label == 'gantungan-da':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'd', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'd', last_char[1:]))

        elif label == 'gantungan-ta':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 't', last_char[2:]))
            else:
                label = ''.join((last_char[0], 't', last_char[1:]))

        elif label == 'gantungan-sa':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 's', last_char[2:]))
            else:
                label = ''.join((last_char[0], 's', last_char[1:]))

        elif label == 'gantungan-wa':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'w', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'w', last_char[1:]))

        elif label == 'gantungan-la':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'l', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'l', last_char[1:]))

        elif label == 'gantungan-ma':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:2], 'm', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'm', last_char[1:]))

        elif label == 'gantungan-ga':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'g', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'g', last_char[1:]))

        elif label == 'gantungan-ba':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'b', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'b', last_char[1:]))

        elif label == 'gantungan-nga':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'ng', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'ng', last_char[1:]))

        elif label == 'gantungan-pa':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'p', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'p', last_char[1:]))

        elif label == 'gantungan-ja':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'j', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'j', last_char[1:]))

        elif label == 'gantungan-ya':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'y', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'y', last_char[1:]))

        elif label == 'gantungan-nya':
            last_char = words.pop()
            if 'gantungan' in labels[id - 1]:
                label = ''.join((last_char[:1], 'ny', last_char[2:]))
            else:
                label = ''.join((last_char[0], 'ny', last_char[1:]))

        elif label == 'end':
            label = '\n'

        # if ('nya' in label or label == 'nga') and ('gantungan' in labels[id + 1]):
        #     label = ''.join((label[0], label[2:]))
        words.append(label)
    return ''.join(word for word in words).lower()
           

def app():
    st.header('Tranliterasi Aksara Bali')
    
    model = YOLO('models/best.pt')

    with st.form('my_form'):
        uploaded_image = st.file_uploader(
            'Choose an Image ...', type=['jpg', 'png', 'jpeg'])
        st.form_submit_button(label='Transliterate', type='primary', use_container_width=True)

    if uploaded_image:
        input_path = uploaded_image.name
        before, after = st.columns(2)
        
        image = Image.open(uploaded_image)
        
        before.image(image, caption=input_path, use_container_width='auto')

        results = model.predict(image, iou=0.5)
        
        after.image(cv2.cvtColor(results[0].plot(), cv2.COLOR_BGR2RGB),
                 caption='Detected Objects.', use_container_width='auto')
        
        try:
            words = transliterate(results)
            for word in words:  
                st.header(word)
        except Exception:
            st.error('Maaf, gambar tidak bisa di transliterasi!')
    

if __name__ == '__main__':
    app()