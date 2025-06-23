import RPi.GPIO as GPIO
import time

BROCHE_TRIG = 23
BROCHE_ECHO = 24
BROCHE_LED = 17

DISTANCE_DETECTION_CM = 9

def initialiser_gpio():
    print("[GPIO] Initialisation avec RPi.GPIO...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BROCHE_LED, GPIO.OUT)
    GPIO.setup(BROCHE_TRIG, GPIO.OUT)
    GPIO.setup(BROCHE_ECHO, GPIO.IN)
    eteindre_led()
    time.sleep(0.5)

def nettoyer_gpio():
    print("[GPIO] Nettoyage RPi.GPIO...")
    GPIO.cleanup()

def mesurer_distance():
    # S'assurer que TRIG est à l'état bas
    GPIO.output(BROCHE_TRIG, False)
    time.sleep(0.0002)  # petit délai pour éviter des erreurs

    # Déclenchement du capteur (10 µs)
    GPIO.output(BROCHE_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(BROCHE_TRIG, False)

    # Attente du signal de départ (timeout anti-boucle infinie)
    t_start = time.time()
    timeout_start = time.time()
    while GPIO.input(BROCHE_ECHO) == 0:
        t_start = time.time()
        if time.time() - timeout_start > 0.02:  # 20 ms timeout
            print("[ERREUR] Timeout attente départ signal")
            return -1

    # Attente du retour du signal (timeout anti-boucle infinie)
    timeout_end = time.time()
    while GPIO.input(BROCHE_ECHO) == 1:
        t_end = time.time()
        if time.time() - timeout_end > 0.02:
            print("[ERREUR] Timeout retour signal")
            return -1

    duration = t_end - t_start
    distance_cm = duration * 17150  # (34300 cm/s) / 2 aller-retour
    return round(distance_cm, 2)

def allumer_led():
    GPIO.output(BROCHE_LED, True)

def eteindre_led():
    GPIO.output(BROCHE_LED, False)

def personne_detectee():
    distance = mesurer_distance()
    if distance == -1:
        return False
    print(f"[CAPTEUR] Distance mesurée : {distance} cm")
    return distance < DISTANCE_DETECTION_CM
