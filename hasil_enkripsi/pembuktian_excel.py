import xlsxwriter

# ==============================================================================
# KONFIGURASI
# ==============================================================================
FILENAME_EXCEL = 'Pembuktian_Super_Enkripsi.xlsx'
MAX_CHARS = 15
TEXT_DEFAULT = "ALBI"
A_VAL = 3.9
X0_VAL = 0.5
SEED_PRNG = 123   # HARUS sama dengan Python

workbook = xlsxwriter.Workbook(FILENAME_EXCEL)
worksheet = workbook.add_worksheet("Pembuktian")

# ==============================================================================
# FORMAT
# ==============================================================================
header = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1, 'align': 'center'})
label = workbook.add_format({'bold': True, 'bg_color': '#E0E0E0', 'border': 1})
inputv = workbook.add_format({'bold': True, 'bg_color': '#FFFF99', 'border': 1})
cell = workbook.add_format({'border': 1, 'align': 'center'})

worksheet.set_column('A:J', 16)

# ==============================================================================
# INPUT PARAMETER
# ==============================================================================
worksheet.merge_range('A1:B1', 'PARAMETER INPUT', header)
worksheet.write('A2', 'Nilai a', label)
worksheet.write('B2', A_VAL, inputv)
worksheet.write('A3', 'Nilai x0', label)
worksheet.write('B3', X0_VAL, inputv)
worksheet.write('A4', 'Seed PRNG', label)
worksheet.write('B4', SEED_PRNG, inputv)
worksheet.write('A5', 'Plaintext', label)
worksheet.write('B5', TEXT_DEFAULT, inputv)

# ==============================================================================
# HEADER TABEL
# ==============================================================================
headers = [
    "Index", "Chaos (x)", "Keystream Chaos", "Ranking",
    "Huruf Asli", "ASCII (P)",
    "XOR PRNG", "XOR Chaotic",
    "Char Substitusi", "Cipher Final"
]

row_header = 7
for col, h in enumerate(headers):
    worksheet.write(row_header, col, h, header)

# ==============================================================================
# RANGE DINAMIS
# ==============================================================================
data_start = row_header + 1
excel_start = data_start + 1

chaos_range = f"OFFSET($B${excel_start},0,0,LEN($B$5),1)"
subs_char_range = f"OFFSET($I${excel_start},0,0,LEN($B$5),1)"

# ==============================================================================
# ISI DATA
# ==============================================================================
for i in range(MAX_CHARS):
    row = data_start + i
    er = row + 1
    valid = f'IF(A{er}<LEN($B$5),'
    end = ',"")'

    # Index
    worksheet.write(row, 0, i, cell)

    # Logistic Map
    if i == 0:
        worksheet.write_formula(row, 1, f"=$B$2*$B$3*(1-$B$3)", cell)
    else:
        worksheet.write_formula(row, 1, f"=$B$2*B{er-1}*(1-B{er-1})", cell)

    # Keystream Chaos
    worksheet.write_formula(row, 2, f"=MOD(INT(B{er}*10^10),256)", cell)

    # Ranking Permutasi
    worksheet.write_formula(
        row, 3,
        f"{valid}MATCH(SMALL({chaos_range},A{er}+1),{chaos_range},0)-1{end}",
        cell
    )

    # Huruf Asli
    worksheet.write_formula(row, 4, f"{valid}MID($B$5,A{er}+1,1){end}", cell)

    # ASCII
    worksheet.write_formula(row, 5, f"{valid}CODE(E{er}){end}", cell)

    # XOR PRNG (LCG manual)
    worksheet.write_formula(
        row, 6,
        f"{valid}BITXOR(F{er},MOD(({SEED_PRNG}+A{er})*1103515245+12345,256)){end}",
        cell
    )

    # XOR Chaotic
    worksheet.write_formula(
        row, 7,
        f"{valid}BITXOR(G{er},C{er}){end}",
        cell
    )

    # Karakter Substitusi
    worksheet.write_formula(row, 8, f"{valid}CHAR(H{er}){end}", cell)

    # Cipher Final (Permutasi)
    worksheet.write_formula(
        row, 9,
        f"{valid}INDEX({subs_char_range},D{er}+1){end}",
        cell
    )

workbook.close()
print("[OK] File Pembuktian Super Enkripsi (3 Metode) berhasil dibuat.")
