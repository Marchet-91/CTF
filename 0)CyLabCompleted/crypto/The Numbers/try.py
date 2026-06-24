import cv2
import pytesseract

# ---- SOLO PER UTENTI WINDOWS ----
# Se Tesseract non è nel PATH di sistema, scommenta la riga sotto e inserisci il tuo percorso:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 1. Carica l'immagine
image_path = 'the_numbers.png'
img = cv2.imread(image_path)

# 2. Pre-processing: Converti in scala di grigi
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 3. Pulizia del rumore: Applica un thresholding (soglia)
# I pixel più scuri del valore '100' diventano nero puro (0), gli altri bianco (255)
_, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

# (Opzionale) Salva l'immagine pulita per verificare il risultato visivamente
cv2.imwrite('immagine_pulita.png', thresh)

# 4. Configurazione Tesseract
# --psm 6 assume che l'immagine sia un singolo blocco di testo uniforme
custom_config = r'--oem 3 --psm 6'

# 5. Estrazione del testo
testo_estratto = pytesseract.image_to_string(thresh, config=custom_config)

print("--- TESTO ESTRATTO ---")
print(testo_estratto)