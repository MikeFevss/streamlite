import streamlit as st
import json
import os

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

# ---------------- FILES ----------------
STATE_FILE = "check.json"
BOARDS_FILE = "pre_generated_boards.json"

# ---------------- LOAD STATE ----------------
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        marked_state = json.load(f)
else:
    marked_state = {a: False for a in lista_acontecimentos}

if os.path.exists(BOARDS_FILE):
    with open(BOARDS_FILE, "r", encoding="utf-8") as f:
        pre_generated_boards = json.load(f)
else:
    st.error(f"{BOARDS_FILE} not found.")
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
st.set_page_config(
    page_title="Bingo Dashboard",
    layout="wide"
)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
}

.bingo-cell {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 95px;
    height: 48px;
    border: 1px solid #333;
    border-radius: 6px;
    margin: 2px;
    padding: 4px;
    font-size: 12px;
    font-weight: 500;
    text-align: center;
    color: black;
    line-height: 1.2;
}

.status-box {
    padding: 12px 16px;
    border-radius: 10px;
    background: #f4f6f8;
    margin-bottom: 20px;
    font-size: 16px;
}

section[data-testid="stSidebar"] {
    background-color: #fafafa;
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

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(marked_state, f, ensure_ascii=False, indent=2)

# ---------------- DETECT STATUS ----------------
winners = []
near_winners = []

for idx, board in enumerate(pre_generated_boards):
    for line in WINNING_LINES:
        line_items = {board[r][c] for r, c in line}
        if line_items.issubset(marked_set):
            winners.append((idx, line))
        elif len(line_items - marked_set) == 1:
            near_winners.append((idx, line, line_items - marked_set))

# ---------------- STATUS BAR (TOP) ----------------
if winners:
    status_text = "🎉 <b>Vencedores:</b> " + ", ".join(
        lista_pessoas[idx % len(lista_pessoas)] for idx, _ in winners
    )
    border_color = "#4CAF50"
elif near_winners:
    status_text = "⚠️ <b>Quase bingo:</b> " + ", ".join(
        f"{lista_pessoas[idx % len(lista_pessoas)]} ({list(missing)[0]})"
        for idx, _, missing in near_winners
    )
    border_color = "#FF9800"
else:
    status_text = "❌ <b>Ainda não há vencedores.</b>"
    border_color = "#999"

st.markdown(
    f"""
    <div class="status-box" style="border-left:6px solid {border_color}">
        {status_text}
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- DISPLAY BOARDS ----------------
boards_per_row = 2

for row_start in range(0, len(pre_generated_boards), boards_per_row):
    cols = st.columns(boards_per_row)

    for i, idx in enumerate(range(row_start, min(row_start + boards_per_row, len(pre_generated_boards)))):
        board = pre_generated_boards[idx]
        col = cols[i]

        col.markdown(
            f"<h4 style='text-align:center;'>🎯 {lista_pessoas[idx % len(lista_pessoas)]}</h4>",
            unsafe_allow_html=True
        )

        winning_coords = set()
        for w_idx, line in winners:
            if w_idx == idx:
                winning_coords.update(line)

        for r in range(GRID_SIZE):
            row_html = "<div>"
            for c in range(GRID_SIZE):
                cell = board[r][c]

                if (r, c) in winning_coords:
                    color = "#FFD966"
                elif cell in marked_set:
                    color = "#B6F2B6"
                else:
                    color = "#FFFFFF"

                row_html += f"""
                <div class="bingo-cell" style="background-color:{color}">
                    {cell}
                </div>
                """
            row_html += "</div>"
            col.markdown(row_html, unsafe_allow_html=True)
