import math

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Liste des notes détectées
listeNote = []


def detecter_frequences(fichier_audio):
    """
    Détecte les fréquences d'un fichier audio et affiche le domaine fréquentiel toutes les 5 ms,
    avec identification des pics d'amplitude.

    Args:
        fichier_audio (str): Le chemin vers le fichier audio.

    Returns:
        None
    """
    try:
        # Charger le fichier audio avec une fréquence d'échantillonnage de 22050 Hz
        y, sr = librosa.load(fichier_audio, sr=11025)  # sr fixé à 22050 Hz

        # Paramètres pour la transformée de Fourier à court terme (STFT)
        n_fft = 2048  # Taille de la fenêtre FFT
        hop_length = 441  # Espacement entre les fenêtres (20 ms)

        # Calcul de la STFT pour obtenir le spectrogramme
        stft = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))

        # Affichage du spectrogramme sur une échelle logarithmique
        plt.figure(figsize=(12, 6))
        librosa.display.specshow(librosa.amplitude_to_db(stft, ref=np.max),
                                 sr=sr, hop_length=hop_length, y_axis='log', x_axis='time')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Spectrogramme complet')
        plt.xlabel('Temps (s)')
        plt.ylabel('Fréquence (Hz)')
        plt.tight_layout()
        plt.show()

        # Calcul des fréquences correspondant à chaque bin FFT
        frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

        # Calcul de la durée d'une frame
        frame_duration = hop_length / sr  # Correspond à 0.02 secondes (20 ms)

        # Détermination du nombre de frames pour une durée de 5 ms
        frames_per_5ms = max(1, int(0.002 / frame_duration))  # Frames nécessaires (au moins 1)

        # Nombre total de frames dans le spectrogramme
        num_frames = stft.shape[1]

        # Initialisation des variables pour le traitement
        i = 0
        listeNote = []
        MoyenneAmp = 0  # Moyenne des amplitudes détectées
        NBamp = 0  # Nombre total d'amplitudes utilisées pour la moyenne

        # Boucle sur chaque segment de 5 ms
        for start_frame in range(0, num_frames, frames_per_5ms):
            end_frame = start_frame + frames_per_5ms

            # Moyenne des amplitudes pour le segment
            amplitudes_moyennes = np.mean(stft[:, start_frame:end_frame], axis=1)

            # Détection des pics d'amplitude dans le spectre fréquentiel
            peaks, _ = find_peaks(amplitudes_moyennes, height=0.05)  # Ajuster la hauteur si nécessaire

            # Récupération des fréquences correspondantes aux pics détectés
            frequences_pics = frequencies[peaks]

            i += 1



            afficher = False  # Indicateur pour afficher le spectre d'un segment particulier

            # Parcourir les pics détectés pour extraire les notes
            for freq, amp in zip(frequences_pics, amplitudes_moyennes[peaks]):
                MoyenneAmp += amp  # Mise à jour de la somme des amplitudes
                NBamp += 1  # Compteur d'amplitudes
                if amp > 1:  # Seuil pour considérer une note significative
                    listeNote.append((round(amp, 2), round(freq, 2), round(start_frame * frame_duration, 2)))

        # Vérification d'affichage du domaine fréquentiel pour un segment
            if afficher:
                plt.figure(figsize=(10, 4))
                plt.plot(frequencies, amplitudes_moyennes, label='Amplitudes moyennes')
                plt.scatter(frequences_pics, amplitudes_moyennes[peaks], color='red', label='Pics détectés')
                plt.xlabel('Fréquence (Hz)')
                plt.ylabel('Amplitude')
                plt.title(f'Domaine fréquentiel ({start_frame * frame_duration:.2f}s - {end_frame * frame_duration:.2f}s)')
                plt.legend()
                plt.grid()
                plt.tight_layout()
                plt.show()

    except Exception as e:
        # Gestion des erreurs lors du traitement du fichier audio
        print(f"Erreur lors du traitement du fichier audio : {e}")

    # Sauvegarde des notes détectées dans un fichier texte
    with open("notes_detectees.txt", "w") as f:
        temps = -2
        for note in listeNote:
            if temps != note[2]:
                f.write(f"\n{note}\n")
                temps = note[2]
            else:
                f.write(f"{note}\n")

    TabTestPourUneNote = [[]] #En considérant qu'une personne ne va pas jouer 2 note en moin de 10 miliseconde
    temps = -2
    nbCase = -1
    for note in listeNote:
        if temps != note[2]:
            nbCase += 1
            temps = note[2]
            TabTestPourUneNote.append([])
            TabTestPourUneNote[nbCase].append(note)
        else:
            TabTestPourUneNote[nbCase].append(note)

    TabTestPourUneNote3 = []
    for i in range(len(TabTestPourUneNote)):
        if TabTestPourUneNote[i]:  # Vérifie si la liste n'est pas vide
            TabTestPourUneNote3.append(list(zip(*TabTestPourUneNote[i])))

    for i in range(len(TabTestPourUneNote3)):
        print(TabTestPourUneNote3[i])

    Liste = []
    Actuel = ()
    for i in range(len(TabTestPourUneNote3)-2):
        if Actuel == TabTestPourUneNote3[i][1]:
            Liste.append(TabTestPourUneNote3[i])
        else:   
            if TabTestPourUneNote3[i][1] == TabTestPourUneNote3[i+1][1] == TabTestPourUneNote3[i+2][1]:
                Actuel = TabTestPourUneNote3[i][1]
                Note = []
                print(TabTestPourUneNote3[i-1][1])
                found_notes = NombreDeNote(TabTestPourUneNote3[i][1])
                print(TabTestPourUneNote3[i][1])
                print(f"Nombre de notes jouées : {len(found_notes)}")
                print("Notes et harmoniques détectées :", found_notes, "\n")

                Liste.append((TabTestPourUneNote3[i], len(Note)))
    print()
    print("Liste :")
    for i in Liste:
        print(i)
    print()

    Dictionnaire = {}
    for i in range(len(Liste)):
        if len(Liste[i]) == 3:
            result = TrouverLaPrincipal(Liste[i][1])
        else:
            result = TrouverLaPrincipal(Liste[i][0][1])
        if result != None:
            print(result)
            Dictionnaire[Liste[i][1]] = result





    TabTestPourUneNote2 = []
    for i in range(len(TabTestPourUneNote3)-3):
        DejaPresent = False
        if TabTestPourUneNote3[i][1] == TabTestPourUneNote3[i+1][1] == TabTestPourUneNote3[i+2][1]:
            for j in range(len(TabTestPourUneNote2)):
                if TabTestPourUneNote2[j][1] == TabTestPourUneNote3[i][1]:
                    DejaPresent = True
                    break
                else:
                    if len(TabTestPourUneNote2[j][1]) > len(TabTestPourUneNote3[i][1]):
                        DejaPresent = all(x in TabTestPourUneNote2[j][1] for x in TabTestPourUneNote3[i][1])
            if DejaPresent == False:
                TabTestPourUneNote2.append(TabTestPourUneNote3[i])

    print()
    for i in range(len(TabTestPourUneNote2)):
        print(TabTestPourUneNote2[i])



    Tuple = []
    Dictionnaire = {}
    TabTestPourUneNote2 = TabTestPourUneNote3
    for i in range(len(TabTestPourUneNote2)-2):
        tuple = []
        if TabTestPourUneNote2[i][1] == TabTestPourUneNote2[i+1][1] == TabTestPourUneNote2[i+2][1]:
            for j in range(len(TabTestPourUneNote2[i][1])):
                if Dictionnaire.get(TabTestPourUneNote2[i][1][j]) is None:
                    tuple.append(TabTestPourUneNote2[i][1][j])
                    Dictionnaire[TabTestPourUneNote2[i][1][j]] = TabTestPourUneNote2[i][0][j]

                else:
                    if TabTestPourUneNote2[i][0][j] > Dictionnaire[TabTestPourUneNote2[i][1][j]]:
                        if not math.isclose(TabTestPourUneNote2[i][0][j], Dictionnaire[TabTestPourUneNote2[i][1][j]], abs_tol = 2):
                            tuple.append(TabTestPourUneNote2[i][1][j])
                            Dictionnaire[TabTestPourUneNote2[i][1][j]] = TabTestPourUneNote2[i][0][j]
                    else:
                        Dictionnaire[TabTestPourUneNote2[i][1][j]] = TabTestPourUneNote2[i][0][j]
            if tuple:
                Tuple.append((tuple, TabTestPourUneNote2[i][2][0]))

    print(Dictionnaire)
    print()
    note = []
    print("Tuple : ")
    print(Tuple)
    for tuple, temps in Tuple:
        multiple = 0
        print(tuple)
        Principal = tuple[0]
        for j in range(len(tuple)):
            if math.isclose(tuple[j]%Principal, 0, abs_tol = 15) or math.isclose(tuple[j]%Principal, Principal, abs_tol = 15):
                if tuple[j] != Principal:
                    multiple += 1
        if multiple > 0:
            note.append((Principal, temps))

    print(note)

    noteFinal = []
    for i in range(len(note)):
        if 70 < note[i][0] < 710: # Plage des fréquences d'intérêt (notes musicales)
            noteFinal.append(note[i][0])

    return noteFinal




def TrouverLaPrincipal(tuple, m = 0):
    multiple = 0
    Principal = tuple[m]
    for j in range(len(tuple)):
        if math.isclose(tuple[j] % Principal, 0, abs_tol=15) or math.isclose(tuple[j] % Principal, Principal,
                                                                             abs_tol=15):
            if tuple[j] != Principal:
                multiple += 1
    if multiple > 0:
        return Principal

    return


def NombreDeNote(Frequences, tolerance=15):
    note_groups = []

    for i in range(len(Frequences)):
        current_freq = Frequences[i]
        added = False

        for group in note_groups:
            fundamental = group[0]
            if any(math.isclose(current_freq, fundamental * n, abs_tol=tolerance) for n in range(1, 6)):
                group.append(current_freq)
                added = True
                break

        if not added:
            note_groups.append([current_freq])

    # Supprimer les sons parasites (notes isolées)
    note_groups = [group for group in note_groups if len(group) > 1]

    return note_groups



