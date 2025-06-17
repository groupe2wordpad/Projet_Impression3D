import time
import informatique  # module pour gérer interface 
import electronique  #  module GPIO, détection, LED

def main():
    try:
        # Initialisation GPIO
        electronique.initialiser_gpio()
        print("[MAIN] GPIO initialisé.")

        detection_effectuee = False  # Pour éviter de relancer la séquence plusieurs fois

        while True:
            if electronique.personne_detectee():
                if not detection_effectuee:
                    print("[MAIN] Personne détectée !")
                    electronique.allumer_led()
                    time.sleep(3)  # Attente avant de lancer message

                    # Lancer message vocal d'intro
                    informatique.lancer_message_introduction()

                    # Changer page de repos vers interaction
                    informatique.changer_page("interaction")

                    detection_effectuee = True  # Séquence lancée

                else:
                    # Personne toujours présente, LED reste allumée, on attend
                    pass

            else:
                # Personne non détectée, on éteint la LED
                if detection_effectuee:
                    print("[MAIN] Personne partie, retour au repos.")
                    electronique.eteindre_led()
                    informatique.changer_page("repos")
                    detection_effectuee = False

            time.sleep(0.5)  # Petite pause entre détections

    except KeyboardInterrupt:
        print("\n[MAIN] Interruption clavier reçue. Nettoyage GPIO et sortie.")
    finally:
        electronique.eteindre_led()
        electronique.nettoyer_gpio()
        print("[MAIN] GPIO nettoyé. Fin du programme.")

if __name__ == "__main__":
    main()
