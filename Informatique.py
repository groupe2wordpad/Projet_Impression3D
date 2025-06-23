import os

def lancer_message_introduction():
    fichier_intro = "message_intro.wav"
    if os.path.exists(fichier_intro):
        print("[INFO] Lecture du message d’introduction local.")
        os.system(f"aplay {fichier_intro}")
    else:
        print(f"[WARNING] Fichier {fichier_intro} introuvable.")

def changer_page(page_name):
    chemin_fichier = os.path.join("static", "page_state.txt")
    with open(chemin_fichier, "w") as f:
        f.write(page_name)
    print(f"[INFO] Page changée : {page_name}")
