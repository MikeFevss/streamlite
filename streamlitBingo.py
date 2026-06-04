import streamlit as st
import json
import os

from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)
GRID_SIZE = 5

# ---------------- DATA ----------------
lista_acontecimentos = [
    "Fábio perde um voo",
    "Daniela corre a meia maratona",
    "Bia aperta mão ao Trump",
    "Miguel muda de emprego",
    "Gustavo com barba completa",
    "Núria suja o vestido de casamento",
    "Rita vai à fisioterapia",
    "As raparigas vão de férias (pelo menos uma noite)",
    "Catarina escolhe tema pra tese",
    "Elzo aparece + do que 2 vezes",
    "Elzo é pai",
    "Bia manda algo pra trás no casamento",
    "Gustavo compra consola",
    "Miguel compra porta talheres",
    "Rita dá mais do que 5 faltas disciplinares",
    "Alguém aparece na televisão",
    "Fábio tem um incidente com a polícia",
    "Núria acaba mestrado",
    "Gustavo entra na ordem",
    "Elzo chega depois da Núria ao casamento",
    "Daniela arranja trabalho remunerado",
    "Miguel conhece alguém",
    "Catarina compra uma câmera",
    ">= 5 pessoas do grupo nas cegonhas(excl Rita)",
    "Grupo junta se todo num dia"
]

lista_pessoas = [
    'Miguel', 'Rita', 'Catarina', 'Bia', 'Daniela',
    'Duarte', 'Elzo', 'Fábio', 'Gustavo', 'Núria'
]

BOARDS_FILE = "pre_generated_boards.json"

# ---------------- LOAD STATE ----------------
try:
    rows = (
        supabase.table("check")
        .select("*")
        .execute()
    )

    marked_state = {
        row["acontecimento"]: row["check"]
        for row in rows.data
    }

except Exception as e:
    st.error(f"Supabase error: {e}")
    st.stop()


marked_state = {
    row["acontecimento"]: row["check"]
    for row in rows.data
}

if os.path.exists(BOARDS_FILE):
    with open(BOARDS_FILE, "r", encoding="utf-8") as f:
        pre_generated_boards = json.load(f)
else:
    st.error("pre_generated_boards.json not found")
    st.stop()

# ---------------- FUNCTIONS ----------------
def get_winning_lines():
    lines = []
    for r in range(GRID_SIZE):
        lines.append({(r, c) for c in range(GRID_SIZE)})
    for c in range(GRID_SIZE):
        lines.append({(r, c) for r in range(GRID_SIZE)})
    lines.append({(i, i) for i in range(GRID_SIZE)})
    lines.append({(i, GRID_SIZE - 1 - i) for i in range(GRID_SIZE)})
    return lines

WINNING_LINES = get_winning_lines()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Bingo Dashboard", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.bingo-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 4px;
}
.bingo-cell {
    border: 1px solid #333;
    border-radius: 6px;
    padding: 6px;
    font-size: 12px;
    text-align: center;
    color: black;
    min-height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.status-box {
    padding: 14px;
    border-radius: 10px;
    margin-bottom: 24px;
    background: #f8f9fa;
    font-size: 16px;
    color: #111;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🎉 Bingo Dashboard – Acontecimentos 2026 🎉")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Marque os acontecimentos")
marked_set = set()

for a in lista_acontecimentos:
    checked = st.sidebar.checkbox(a, value=marked_state.get(a, False), key=a)
    marked_state[a] = checked
    if checked:
        marked_set.add(a)

for event, checked in marked_state.items():
    (
        supabase.table("bingo_state")
        .update({"checked": checked})
        .eq("event", event)
        .execute()
    )

# ---------------- STATUS ----------------
winners = []
near_winners = []

for idx, board in enumerate(pre_generated_boards):
    for line in WINNING_LINES:
        items = {board[r][c] for r, c in line}
        if items.issubset(marked_set):
            winners.append(idx)
        elif len(items - marked_set) == 1:
            near_winners.append((idx, list(items - marked_set)[0]))

if winners:
    text = "🎉 Vencedores: " + ", ".join(lista_pessoas[i] for i in set(winners))
    border = "#4CAF50"
elif near_winners:
    text = "⚠️ Quase bingo: " + ", ".join(
        f"{lista_pessoas[i]} ({missing})" for i, missing in near_winners
    )
    border = "#FF9800"
else:
    text = "❌ Ainda não há vencedores."
    border = "#999"

st.markdown(
    f"<div class='status-box' style='border-left:6px solid {border}'>{text}</div>",
    unsafe_allow_html=True
)

# ---------------- DISPLAY BOARDS ----------------
boards_per_row = 2

for row_start in range(0, len(pre_generated_boards), boards_per_row):
    cols = st.columns(boards_per_row)

    for col, idx in zip(cols, range(row_start, min(row_start + boards_per_row, len(pre_generated_boards)))):
        board = pre_generated_boards[idx]

        col.markdown(f"### 🎯 {lista_pessoas[idx]}")

        winning_coords = set()
        for line in WINNING_LINES:
            if {board[r][c] for r, c in line}.issubset(marked_set):
                winning_coords |= line

        html = "<div class='bingo-grid'>"
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = board[r][c]
                if (r, c) in winning_coords:
                    bg = "#FFD966"
                elif cell in marked_set:
                    bg = "#B6F2B6"
                else:
                    bg = "#FFFFFF"

                html += f"<div class='bingo-cell' style='background:{bg}'>{cell}</div>"
        html += "</div>"

        col.markdown(html, unsafe_allow_html=True)


