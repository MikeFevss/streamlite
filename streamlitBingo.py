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

lista_pessoas = ['Miguel', 'Rita', 'Catarina', 'Bia', 'Daniela', 'Duarte', 'Elzo', 'Fábio', 'Gustavo', 'Núria']

# ---------------- FILES ----------------
STATE_FILE = "check.json"
BOARDS_FILE = "pre_generated_boards.json"

# Load existing checkbox state
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        marked_state = json.load(f)
else:
    marked_state = {a: False for a in lista_acontecimentos}

# Load pre-generated boards from file
if os.path.exists(BOARDS_FILE):
    with open(BOARDS_FILE, "r", encoding="utf-8") as f:
        pre_generated_boards = json.load(f)
else:
    st.error(f"{BOARDS_FILE} not found! Please create the JSON file with pre-generated boards.")
    st.stop()

# ---------------- FUNCTIONS ----------------
def get_winning_lines(board):
    lines = []
    # Rows
    for r in range(GRID_SIZE):
        lines.append({(r, c) for c in range(GRID_SIZE)})
    # Columns
    for c in range(GRID_SIZE):
        lines.append({(r, c) for r in range(GRID_SIZE)})
    # Diagonals
    lines.append({(i, i) for i in range(GRID_SIZE)})
    lines.append({(i, GRID_SIZE-1-i) for i in range(GRID_SIZE)})
    return lines

# ---------------- STREAMLIT DASHBOARD ----------------
st.set_page_config(page_title="Bingo Dashboard", layout="wide")
st.title("🎉 Bingo Dashboard – Acontecimentos 2026 🎉")

# ---------------- SIDEBAR CHECKBOXES ----------------
st.sidebar.header("Marque os acontecimentos")
marked_set = set()
for a in lista_acontecimentos:
    checked = st.sidebar.checkbox(a, value=marked_state.get(a, False), key=a)
    marked_state[a] = checked
    if checked:
        marked_set.add(a)

# Save updated state
with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(marked_state, f, ensure_ascii=False, indent=2)

# ---------------- COMPUTE STATUS ----------------
winners = []
near_winners = []

for idx, board in enumerate(pre_generated_boards):
    board_lines = get_winning_lines(board)
    for line in board_lines:
        line_items = {board[r][c] for r, c in line}
        if line_items.issubset(marked_set):
            winners.append((idx, line))
        elif len(line_items - marked_set) == 1:
            near_winners.append((idx, line, line_items - marked_set))

status_text = ""
if winners:
    status_text += "🎉 Vencedores: " + ", ".join(lista_pessoas[idx % len(lista_pessoas)] for idx, _ in winners) + "\n"
if near_winners:
    status_text += "⚠️ Quase bingo: " + ", ".join(
        f"{lista_pessoas[idx % len(lista_pessoas)]} ({list(missing)[0]})" for idx, _, missing in near_winners
    )
if not status_text:
    status_text = "❌ Ainda não há vencedores."

# ---------------- SHOW STATUS AT THE TOP ----------------
st.markdown(f"### {status_text}")

# ---------------- DISPLAY BOARDS ----------------
num_boards = len(pre_generated_boards)
boards_per_row = 1  # max 2 boards per row

for row_start in range(0, num_boards, boards_per_row):
    row_cols = st.columns(boards_per_row)
    for i, idx in enumerate(range(row_start, min(row_start + boards_per_row, num_boards))):
        board = pre_generated_boards[idx]
        col = row_cols[i]
        col.subheader(lista_pessoas[idx % len(lista_pessoas)])
        board_lines = get_winning_lines(board)
        winning_coords = []

        # Detect winners again for coloring
        for line in board_lines:
            line_items = {board[r][c] for r, c in line}
            if line_items.issubset(marked_set):
                winning_coords.extend(list(line))

        # Render board as 5x5 grid (smaller boxes and text)
        for r in range(GRID_SIZE):
            row_html = ""
            for c in range(GRID_SIZE):
                cell = board[r][c]
                if (r, c) in winning_coords:
                    color = "#ffd966"  # gold for winners
                elif cell in marked_set:
                    color = "#b6f2b6"  # green for marked
                else:
                    color = "#ffffff"  # white
                row_html += f'''
                <div style="
                    display:inline-block;
                    width:65px; 
                    height:50px; 
                    border:1px solid #000;
                    background-color:{color};
                    color:black;
                    text-align:center;
                    vertical-align:middle;
                    padding:1px;
                    font-size:8px;
                    overflow:hidden;
                ">{cell}</div>
                '''
            col.markdown(row_html, unsafe_allow_html=True)






