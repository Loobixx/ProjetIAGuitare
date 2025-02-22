import os
import sys

import joblib
import tensorflow as tf
print("Version de TensorFlow :", tf.__version__)
from tensorflow.keras.models import load_model
from DetecterLaFrequenceJouer import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def creationTab(audio_path):
 # Remplacez par votre fichier audio
    y, sr = librosa.load(audio_path, sr=None)  # sr=None pour conserver le taux d'échantillonnage d'origine

    # Détecter les fréquences fondamentales
    onsets = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True, units='time')
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    Modele_dir = resource_path("Modele_IA")

    # Charger le modèle, le scaler et le label_encoder
    model = load_model(Modele_dir + "\modele_notes_guitare.h5")  # Charger le modèle Keras


    scaler = joblib.load(Modele_dir + "\scaler.pkl")  # Charger le scaler


    label_encoder = joblib.load(Modele_dir + "\encodeur_etiquettes.pkl")  # Charger le label encoder

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    # Charger le modèle, le scaler et le label_encoder
    def predict_note_from_frequency(frequency):
        # Normaliser la fréquence
        normalized_frequency = scaler.transform(np.array([[frequency]]))

        # Prédire la note
        prediction = model.predict(normalized_frequency, verbose=0)
        predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])

        return predicted_label[0]

    notes_positions = {
        'A2': (0,2),
        'A3': (2,4),
        'A4': (5,6),
        'A#2': (1,2),
        'A#3': (3,4),
        'A#4': (6,6),
        'B2': (2,2),
        'B3': (0,5),
        'B4': (7,6),
        'C3': (3,2),
        'C4': (1,5),
        'C5': (8,6),
        'C#3': (4,2),
        'C#4': (2,5),
        'C#5': (9,6),
        'D3': (0,3),
        'D4': (3,5),
        'D5': (10,6),
        'D#3': (1,3),
        'D#4': (4,5),
        'D#5': (11,6),
        'E2': (0,1),
        'E3': (2,3),
        'E4': (0,6),
        'E5': (12,6),
        'F2': (1,1),
        'F3': (3,3),
        'F4': (1,6),
        'F5': (13,6),
        'F#2': (2,1),
        'F#3': (4,3),
        'F#4': (2,6),
        'G2': (3,1),
        'G3': (0,4),
        'G4': (3,6),
        'G#2': (4,1),
        'G#3': (1,4),
        'G#4': (4,6)
    }

    tab = []
    notes_detected = detecter_frequences(audio_path)
    if notes_detected != None:
        for i in range(len(notes_detected)):
            predicted_note = predict_note_from_frequency(notes_detected[i])#La suite doit etre modifier en rajoutant les note de l'ia a celle ci afin que tous corresponde parfaitement
            if (notes_positions.get(predicted_note) != None):
                tab.append([notes_positions.get(predicted_note)])



    return tab
