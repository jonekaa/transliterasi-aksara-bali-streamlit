import cv2
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
    sorted_predictions = sorted(predictions, key=lambda x: (
        float(x[0]), float(x[1]), float(x[3])))

    # st.write(sorted_predictions)
    
    labels = [label for _, (x1, y1, x2, y2, label) in enumerate(sorted_predictions)]
    word = read_labels(labels)
    
    return word

def read_labels(labels):
    words = []
    
    for id, label in enumerate(labels):
        # Ketika depan adalah taleng        
        if label == 'taleng':
            if len(labels) - id == 2:
                labels[id + 1] = labels[id + 1].replace(list(labels[id + 1])[-1], 'é')
                continue
                
            elif len(labels) - id == 3:
                if labels[id + 2] == 'tedong':
                    label = ''
                    labels[id + 1] = labels[id +
                                           1].replace(list(labels[id + 1])[-1], 'o')
                    labels[id + 2] = ''
                    continue
                
                if id < len(labels) - 1:
                    labels[id + 1] = labels[id +
                                            1].replace(list(labels[id + 1])[-1], 'é')
                    continue
                    
            else:
                if labels[id + 2] == 'tedong':
                    label = ''
                    labels[id + 1] = labels[id +
                                            1].replace(list(labels[id + 1])[-1], 'o')
                    labels[id + 2] = ''
                    continue
                
                elif labels[id + 3] == 'tedong':
                    label = ''
                    labels[id + 2] = labels[id +
                                            2].replace(list(labels[id + 2])[-1], 'o')
                    labels[id + 3] = ''
                    continue
                
                if id < len(labels) - 1:
                    labels[id + 1] = labels[id +
                                            1].replace(list(labels[id + 1])[-1], 'é')
                    continue
                    
        
        if words:
            if label == 'ulu':
                last_char = words.pop()
                label = last_char.replace(list(last_char)[-1], 'i')
            elif label == 'suku':
                last_char = words.pop()
                label = last_char.replace(list(last_char)[-1], 'u')
            elif label == 'pepet':
                last_char =  words.pop()
                label = last_char.replace(list(last_char)[-1], 'e')
            elif label == 'adeg-adeg':
                last_char = words.pop()
                label = last_char.replace(list(last_char)[-1], '')
            elif label == 'cecek-ng-':
                label = 'ng'
            elif label == 'surang-r-':
                label = 'r'
            elif label == 'bisah-h-':
                label = 'h'
            elif label =='na-rambat':
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
                label ='ra'
            elif label =='le-lenga':
                label = 'le'
            elif label == 'tedong':
                last_char = words.pop()
                label = ''.join((last_char, last_char[-1]))
            elif label == 'gantungan-ha':
                last_char = words.pop()
                label = ''.join((last_char[0], 'h', last_char[1:]))
            elif label == 'gantungan-na':
                last_char = words.pop()
                label = ''.join((last_char[0], 'n', last_char[1:]))
            elif label == 'gantungan-ca':
                last_char = words.pop()
                label = ''.join((last_char[0], 'c', last_char[1:]))
            elif label == 'gantungan-ra':
                last_char = words.pop()
                label = ''.join((last_char[0], 'r', last_char[1:]))
            elif label == 'gantungan-ka':
                last_char = words.pop()
                label = ''.join((last_char[0], 'k', last_char[1:]))
            elif label == 'gantungan-da':
                last_char = words.pop()
                label = ''.join((last_char[0], 'd', last_char[1:]))
            elif label == 'gantungan-ta':
                last_char = words.pop()
                label = ''.join((last_char[0], 't', last_char[1:]))
            elif label == 'gantungan-sa':
                last_char = words.pop()
                label = ''.join((last_char[0], 's', last_char[1:]))
            elif label == 'gantungan-wa':
                last_char = words.pop()
                label = ''.join((last_char[0], 'w', last_char[1:]))
            elif label == 'gantungan-la':
                last_char = words.pop()
                label = ''.join((last_char[0], 'l', last_char[1:]))
            elif label == 'gantungan-ma':
                last_char = words.pop()
                label = ''.join((last_char[0], 'm', last_char[1:]))
            elif label == 'gantungan-ga':
                last_char = words.pop()
                label = ''.join((last_char[0], 'g', last_char[1:]))
            elif label == 'gantungan-ba':
                last_char = words.pop()
                label = ''.join((last_char[0], 'b', last_char[1:]))
            elif label == 'gantungan-nga':
                last_char = words.pop()
                label = ''.join((last_char[0], 'ng', last_char[1:]))
            elif label == 'gantungan-pa':
                last_char = words.pop()
                label = ''.join((last_char[0], 'p', last_char[1:]))
            elif label == 'gantungan-ja':
                last_char = words.pop()
                label = ''.join((last_char[0], 'j', last_char[1:]))
            elif label == 'gantungan-ya':
                last_char = words.pop()
                label = ''.join((last_char[0], 'y', last_char[1:]))
            elif label == 'gantungan-nya':
                last_char = words.pop()
                label = ''.join((last_char[0], 'ny', last_char[1:]))        
            elif label == 'end':
                label ='\n'
                
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
        char = transliterate(results)

        after.image(cv2.cvtColor(results[0].plot(), cv2.COLOR_BGR2RGB),
                 caption='Detected Objects.', use_container_width='auto')

        st.title(char)
    

if __name__ == '__main__':
    app()
