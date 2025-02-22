import numpy as np
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
import joblib

# Étape 1 : Préparer les données
# Dictionnaire contenant les notes et leurs fréquences respectives
notes_et_frequences = {
    'E2': 82.41,
    'F2': 87.31035360614952,
    'F#2': 92.50209740117543,
    'G2': 98.00255834737423,
    'G#2': 103.83009372183649,
    'A2': 110.00415238215253,
    'A#2': 116.54533967516677,
    'B2': 123.47548620540732,
    'C3': 130.8177206926993,
    'C#3': 138.59654716211722,
    'D3': 146.83792672389072,
    'D#3': 155.5693642161967,
    'E3': 164.82,
    'F3': 174.62070721229904,
    'F#3': 185.00419480235087,
    'G3': 196.00511669474847,
    'G#3': 207.66018744367298,
    'A3': 220.00830476430505,
    'A#3': 233.09067935033355,
    'B3': 246.95097241081464,
    'C4': 261.6354413853986,
    'C#4': 277.19309432423444,
    'D4': 293.67585344778144,
    'D#4': 311.13872843239346,
    'E4': 329.64,
    'F4': 349.2282314330039,
    'F#4': 369.9944227116344,
    'G4': 391.99543598174927,
    'G#4': 415.3046975799451,
    'A4': 440.0,
    'A#4': 466.15619292098154,
    'B4': 493.87528260681165,
    'C5': 523.2426351381841,
    'C#5': 554.3562613242123,
    'D5': 587.32,
    'D#5': 622.2612123715343,
    'E5': 659.2627895589121,
    'F5': 698.464595022026,
}

# Création des listes de fréquences et de labels
frequences = []
etiquettes = []

# Ajouter des variations aux fréquences de base pour simuler des données
for note, frequence in notes_et_frequences.items():
    for variation in np.linspace(-5, 5, 50):  # Ajouter des variations de +- 5 Hz
        frequences.append(frequence + variation)
        etiquettes.append(note)

# Conversion en tableaux numpy
frequences = np.array(frequences)
etiquettes = np.array(etiquettes)

# Encodage des étiquettes en entiers
# Étape 1 : Initialiser un encodeur d'étiquettes (LabelEncoder) pour convertir les noms des notes (ex. : 'A2', 'B3', etc.)
# en valeurs numériques entières.
encodeur_etiquettes = LabelEncoder()

# Étape 2 : Appliquer l'encodage sur la liste des étiquettes (les noms des notes).
# Cela transforme chaque note en un entier unique (ex. : 'A2' -> 0, 'B3' -> 1, etc.).
etiquettes_encodees = encodeur_etiquettes.fit_transform(etiquettes)

# Étape 3 : Convertir ces entiers en une représentation catégorielle (one-hot encoding).
# Le one-hot encoding est nécessaire pour la classification multiclasses dans un réseau de neurones.
# Par exemple : si nous avons 3 classes ('A2', 'B3', 'C4') et une étiquette encodée de 1 (correspondant à 'B3'),
# alors la sortie devient : [0, 1, 0].
etiquettes_categoriques = to_categorical(etiquettes_encodees)


# Normalisation des fréquences entre 0 et 1
scaler_frequences = MinMaxScaler()
frequences_normalisees = scaler_frequences.fit_transform(frequences.reshape(-1, 1))

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(
    frequences_normalisees, etiquettes_categoriques, test_size=0.2, random_state=42
)

# Étape 2 : Construire le modèle
# Création du modèle de réseau de neurones
modele = Sequential([
    Input(shape=(1,)),
    Dense(128, activation='relu'),
    Dropout(0.2),  # Régularisation pour éviter le surapprentissage
    Dense(256, activation='relu'),
    Dropout(0.2),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(len(notes_et_frequences), activation='softmax')  # Sortie avec autant de neurones que de notes
])

# Compilation du modèle
modele.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Ajout d'un callback pour arrêter l'entraînement si la validation ne s'améliore pas
arret_precoce = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)

# Entraînement du modèle
historique = modele.fit(
    X_train,
    y_train,
    epochs=500,
    validation_data=(X_test, y_test),
    batch_size=32,
    verbose=1,
    callbacks=[arret_precoce]
)

# Étape 3 : Prédire une note à partir d'une fréquence
def predire_note(frequence):
    """
    Prédit une note à partir d'une fréquence donnée.
    """
    prediction = modele.predict(np.array([frequence]))
    etiquette_predite = encodeur_etiquettes.inverse_transform([np.argmax(prediction)])
    return etiquette_predite[0]


# Enregistrement du modèle et des transformateurs
reponse = input("Voulez-vous enregistrer le modèle ? (oui/non) : ")
if reponse.lower() == "oui":
    modele.save("Modele_IA/modele_notes_guitare.h5")

# Fonction pour afficher les courbes d'entraînement
def tracer_historique(historique):
    """
    Trace les courbes de perte et de précision pour l'entraînement et la validation.
    """
    plt.figure(figsize=(12, 5))

    # Courbe de perte (loss)
    plt.subplot(1, 2, 1)
    plt.plot(historique.history['loss'], label='Perte entraînement')
    plt.plot(historique.history['val_loss'], label='Perte validation')
    plt.title('Courbe de perte')
    plt.xlabel('Époques')
    plt.ylabel('Perte')
    plt.legend()

    # Courbe de précision (accuracy)
    plt.subplot(1, 2, 2)
    plt.plot(historique.history['accuracy'], label='Précision entraînement')
    plt.plot(historique.history['val_accuracy'], label='Précision validation')
    plt.title('Courbe de précision')
    plt.xlabel('Époques')
    plt.ylabel('Précision')
    plt.legend()

    plt.tight_layout()
    plt.show()


# Affichage des courbes d'entraînement
tracer_historique(historique)

# Exemple de prédiction
frequence = 110.5  # Fréquence proche de A2
frequence_normalisee = scaler_frequences.transform(np.array([[frequence]]))
note_predite = predire_note(frequence_normalisee[0][0])
print(f"La note prédite pour {frequence} Hz est : {note_predite}")

# Sauvegarder le scaler
joblib.dump(scaler_frequences, 'Modele_IA/scaler.pkl')

# Sauvegarder l'encodeur des étiquettes
joblib.dump(encodeur_etiquettes, 'Modele_IA/encodeur_etiquettes.pkl')
