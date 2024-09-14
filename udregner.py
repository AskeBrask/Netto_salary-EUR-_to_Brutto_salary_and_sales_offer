import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # For logo display
from fpdf import FPDF  # For PDF generation

# Funktion til at beregne bruttoløn, salgspris og profit
def beregn(*args):
    try:
        # Inputværdier
        nettoløn_eur = float(nettoløn_entry.get())
        trækprocent = float(trækprocent_entry.get()) / 100
        profit_margin = float(profit_entry.get()) / 100
        antal_timer = float(timer_entry.get())
        antal_medarbejdere = int(medarbejdere_entry.get())
        valutakurs = 7.44  # Fast valutakurs for EUR til DKK

        # Beregn brutto løn i DKK
        bruttoløn_eur = nettoløn_eur / (1 - trækprocent)
        bruttoløn_dkk = bruttoløn_eur * valutakurs
        
        feriepenge = feriepenge_var.get()
        pension = pension_var.get()
        fritvalg_sh = fritvalg_var.get()

        # Beregn brutto løn inkl. feriepenge
        if feriepenge:
            bruttoløn_ferie = bruttoløn_dkk * 1.125  # 12.5% feriepenge
        else:
            bruttoløn_ferie = bruttoløn_dkk

        # Beregn brutto løn inkl. pension
        if pension:
            bruttoløn_pension = bruttoløn_ferie * 1.08  # 8% pension
        else:
            bruttoløn_pension = bruttoløn_ferie

        # Beregn brutto løn inkl. fritvalg og SH
        if fritvalg_sh:
            bruttoløn_fritvalg = bruttoløn_pension * 1.13  # 4% SH og 9% Fritvalg
        else:
            bruttoløn_fritvalg = bruttoløn_pension

        # Beregn salgspris (SP) baseret på brutto lønnen
        salgspris = bruttoløn_fritvalg / (1 - profit_margin)
        profit_amount = salgspris - bruttoløn_fritvalg

        # Beregn total salgspris og profit for antal medarbejdere og timer
        total_salgspris = salgspris * antal_timer * antal_medarbejdere
        total_profit = profit_amount * antal_timer * antal_medarbejdere

        # Opdater resultatfelterne
        bruttoløn_label.config(text=f"{bruttoløn_dkk:.2f} kr.")
        salgspris_label.config(text=f"{salgspris:.2f} kr.")
        profit_label.config(text=f"{profit_amount:.2f} kr.")
        total_salgspris_label.config(text=f"{total_salgspris:.2f} kr.")
        total_profit_label.config(text=f"{total_profit:.2f} kr.")

    except ValueError:
        result_label.config(text="Ugyldig indtastning. Prøv igen.")

# Funktion til at generere tilbud som PDF
def generer_pdf():
    try:
        pdf = FPDF()
        pdf.add_page()

        # Tilføj titel
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Tilbudsberegning", ln=True, align="C")

        # Tilføj oplysninger
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Nettoløn: {nettoløn_entry.get()} EUR", ln=True)
        pdf.cell(200, 10, f"Trækprocent: {trækprocent_entry.get()} %", ln=True)
        pdf.cell(200, 10, f"Ønsket profitmargin: {profit_entry.get()} %", ln=True)
        pdf.cell(200, 10, f"Antal timer: {timer_entry.get()}", ln=True)
        pdf.cell(200, 10, f"Antal medarbejdere: {medarbejdere_entry.get()}", ln=True)
        pdf.cell(200, 10, f"Bruttoløn: {bruttoløn_label.cget('text')}", ln=True)
        pdf.cell(200, 10, f"Salgspris: {salgspris_label.cget('text')}", ln=True)
        pdf.cell(200, 10, f"Profit: {profit_label.cget('text')}", ln=True)
        pdf.cell(200, 10, f"Total salgspris: {total_salgspris_label.cget('text')}", ln=True)
        pdf.cell(200, 10, f"Total profit: {total_profit_label.cget('text')}", ln=True)

        # Gem PDF
        pdf.output("tilbud.pdf")
        result_label.config(text="PDF tilbud gemt som 'tilbud.pdf'")

    except Exception as e:
        result_label.config(text=f"Fejl: {str(e)}")

# Opsætning af GUI
window = tk.Tk()
window.title("Løn Beregner")

# Tilføj logo (skal have en logo-fil, fx logo.png)
try:
    logo_image = Image.open("logo.png")
    logo_image = logo_image.resize((200, 100), Image.ANTIALIAS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(window, image=logo_photo)
    logo_label.grid(row=0, column=0, columnspan=2, pady=10)
except FileNotFoundError:
    pass  # Hvis logo-filen ikke findes, ignoreres det

# Copywriting/introduktion
intro_label = tk.Label(window, text="Velkommen til Løn Beregneren. Indtast venligst dine værdier nedenfor for at få præcise tilbudsberegninger.")
intro_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Forudindstillede værdier
nettoløn_default = 13.00
trækprocent_default = 38.00
profit_default = 30.00
timer_default = 40
medarbejdere_default = 1

# Nettoløn input (i EUR)
tk.Label(window, text="Nettoløn (EUR):").grid(row=2, column=0)
nettoløn_entry = tk.Entry(window)
nettoløn_entry.insert(0, nettoløn_default)
nettoløn_entry.grid(row=2, column=1)
nettoløn_entry.bind("<KeyRelease>", beregn)

# Trækprocent input
tk.Label(window, text="Trækprocent (%):").grid(row=3, column=0)
trækprocent_entry = tk.Entry(window)
trækprocent_entry.insert(0, trækprocent_default)
trækprocent_entry.grid(row=3, column=1)
trækprocent_entry.bind("<KeyRelease>", beregn)

# Profitmargin input
tk.Label(window, text="Ønsket profitmargin (%):").grid(row=4, column=0)
profit_entry = tk.Entry(window)
profit_entry.insert(0, profit_default)
profit_entry.grid(row=4, column=1)
profit_entry.bind("<KeyRelease>", beregn)

# Antal timer input
tk.Label(window, text="Antal timer:").grid(row=5, column=0)
timer_entry = tk.Entry(window)
timer_entry.insert(0, timer_default)
timer_entry.grid(row=5, column=1)
timer_entry.bind("<KeyRelease>", beregn)

# Antal medarbejdere input
tk.Label(window, text="Antal medarbejdere:").grid(row=6, column=0)
medarbejdere_entry = tk.Entry(window)
medarbejdere_entry.insert(0, medarbejdere_default)
medarbejdere_entry.grid(row=6, column=1)
medarbejdere_entry.bind("<KeyRelease>", beregn)

# Feriepenge checkbox
feriepenge_var = tk.BooleanVar()
feriepenge_check = ttk.Checkbutton(window, text="Feriepenge (12,5%)", variable=feriepenge_var)
feriepenge_check.grid(row=7, column=0, columnspan=2)
feriepenge_check.bind("<ButtonRelease>", beregn)

# Pension checkbox
pension_var = tk.BooleanVar()
pension_check = ttk.Checkbutton(window, text="Pension (8%)", variable=pension_var)
pension_check.grid(row=8, column=0, columnspan=2)
pension_check.bind("<ButtonRelease>", beregn)

# Fritvalg og SH checkbox
fritvalg_var = tk.BooleanVar()
fritvalg_check = ttk.Checkbutton(window, text="Fritvalg og SH (13%)", variable=fritvalg_var)
fritvalg_check.grid(row=9, column=0, columnspan=2)
fritvalg_check.bind("<ButtonRelease>", beregn)

# Resultater for en medarbejder
tk.Label(window, text="Bruttoløn (DKK):").grid(row=10, column=0)
bruttoløn_label = tk.Label(window, text="0.00 kr.")
bruttoløn_label.grid(row=10, column=1)

tk.Label(window, text="Salgspris (SP):").grid(row=11, column=0)
salgspris_label = tk.Label(window, text="0.00 kr.")
salgspris_label.grid(row=11, column=1)

tk.Label(window, text="Profit:").grid(row=12, column=0)
profit_label = tk.Label(window, text="0.00 kr.")
profit_label.grid(row=12, column=1)

# Totaler for alle medarbejdere og timer
tk.Label(window, text="Total salgspris:").grid(row=13, column=0)
total_salgspris_label = tk.Label(window, text="0.00 kr.")
total_salgspris_label.grid(row=13, column=1)

tk.Label(window, text="Total profit:").grid(row=14, column=0)
total_profit_label = tk.Label(window, text="0.00 kr.")
total_profit_label.grid(row=14, column=1)

# Tilføj knap til at generere PDF
generate_pdf_button = tk.Button(window, text="Generer PDF Tilbud", command=generer_pdf)
generate_pdf_button.grid(row=15, column=0, columnspan=2, pady=10)

# Resultatbesked
result_label = tk.Label(window, text="")
result_label.grid(row=16, column=0, columnspan=2)

# Kør GUI'en
window.mainloop()

