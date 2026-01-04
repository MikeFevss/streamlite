import streamlit as st

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

# ---------------- PRE-GENERATED BOARDS ----------------
# Each board is a 5x5 list of strings from lista_acontecimentos
pre_generated_boards = [
    [
        ['Gustavo entra na ordem', 'Gustavo compra consola', 'Elzo chega depois da Núria ao casamento', 'Catarina escolhe tema pra tese', 'Catarina compra uma câmera'],
        ['Miguel muda de emprego', 'Rita dá mais do que 5 faltas disciplinares', 'Núria suja o vestido de casamento', 'Elzo aparece + do que 2 vezes', 'Bia manda algo pra trás no casamento'],
        ['Miguel conhece alguém', 'Miguel compra porta talheres', 'Daniela arranja trabalho remunerado', 'As raparigas vão de férias (pelo menos uma noite)', 'Fábio tem um incidente com a polícia'],
        ['Alguém aparece na televisão', '>= 5 pessoas do grupo nas cegonhas(excl Rita)', 'Grupo junta se todo num dia', 'Gustavo com barba completa', 'Daniela corre a meia maratona'],
        ['Núria acaba mestrado', 'Elzo é pai', 'Rita vai à fisioterapia', 'Fábio perde um voo', 'Bia aperta mão ao Trump'],
    ],
    [
        ['Daniela corre a meia maratona', 'Daniela arranja trabalho remunerado', 'Bia manda algo pra trás no casamento', '>= 5 pessoas do grupo nas cegonhas(excl Rita)', 'Fábio tem um incidente com a polícia'],
        ['Gustavo compra consola', 'Miguel muda de emprego', 'Rita vai à fisioterapia', 'Miguel conhece alguém', 'Elzo chega depois da Núria ao casamento'],
        ['Alguém aparece na televisão', 'Catarina escolhe tema pra tese', 'Gustavo com barba completa', 'Fábio perde um voo', 'As raparigas vão de férias (pelo menos uma noite)'],
        ['Elzo é pai', 'Núria acaba mestrado', 'Grupo junta se todo num dia', 'Catarina compra uma câmera', 'Bia aperta mão ao Trump'],
        ['Núria suja o vestido de casamento', 'Gustavo entra na ordem', 'Miguel compra porta talheres', 'Elzo aparece + do que 2 vezes', 'Rita dá mais do que 5 faltas disciplinares'],
    ],
    [
        ['Núria acaba mestrado', 'Miguel conhece alguém', 'Gustavo com barba completa', 'Rita dá mais do que 5 faltas disciplinares', 'Gustavo compra consola'],
        ['Daniela corre a meia maratona', 'Miguel compra porta talheres', 'Elzo chega depois da Núria ao casamento', 'Bia manda algo pra trás no casamento', 'Catarina compra uma câmera'],
        ['>= 5 pessoas do grupo nas cegonhas(excl Rita)', 'Grupo junta se todo num dia', 'Elzo é pai', 'Fábio perde um voo', 'Bia aperta mão ao Trump'],
        ['Gustavo entra na ordem', 'Alguém aparece na televisão', 'Daniela arranja trabalho remunerado', 'Fábio tem um incidente com a polícia', 'Elzo aparece + do que 2 vezes'],
        ['Rita vai à fisioterapia', 'Núria suja o vestido de casamento', 'As raparigas vão de férias (pelo menos uma noite)', 'Miguel muda de emprego', 'Catarina escolhe tema pra tese'],
    ],
    [
        ['Núria acaba mestrado', 'Alguém aparece na televisão', '>= 5 pessoas do grupo nas cegonhas(excl Rita)', 'Núria suja o vestido de casamento', 'Grupo junta se todo num dia'],
        ['Rita vai à fisioterapia', 'Catarina compra uma câmera', 'Fábio perde um voo', 'Daniela corre a meia maratona', 'Miguel muda de emprego'],
        ['Rita dá mais do que 5 faltas disciplinares', 'Bia manda algo pra trás no casamento', 'Gustavo compra consola', 'Elzo é pai', 'Daniela arranja trabalho remunerado'],
        ['As raparigas vão de férias (pelo menos uma noite)', 'Gustavo entra na ordem', 'Miguel compra porta talheres', 'Bia aperta mão ao Trump', 'Catarina escolhe tema pra tese'],
        ['Elzo aparece + do que 2 vezes', 'Elzo chega depois da Núria ao casamento', 'Miguel conhece alguém', 'Gustavo com barba completa', 'Fábio tem um incidente com a polícia'],
    ],
    [
        ['Daniela corre a meia maratona', 'Grupo junta se todo num dia', 'Núria acaba mestrado', 'Bia manda algo pra trás no casamento', 'Miguel conhece alguém'],
        ['Miguel compra porta talheres', 'Rita vai à fisioterapia', 'Alguém aparece na televisão', 'Catarina escolhe tema pra tese', 'Bia aperta mão ao Trump'],
        ['Rita dá mais do que 5 faltas disciplinares', 'Catarina compra uma câmera', 'As raparigas vão de férias (pelo menos uma noite)', 'Elzo é pai', 'Gustavo compra consola'],
        ['Elzo chega depois da Núria ao casamento', 'Fábio tem um incidente com a polícia', 'Gustavo entra na ordem', 'Daniela arranja trabalho remunerado', '>= 5 pessoas do grupo nas cegonhas(excl Rita)'],
        ['Miguel muda de emprego', 'Elzo aparece + do que 2 vezes', 'Fábio perde um voo', 'Gustavo com barba completa', 'Núria suja o vestido de casamento'],
    ],
    [
        ['As raparigas vão de férias (pelo menos uma noite)', 'Daniela corre a meia maratona', 'Bia manda algo pra trás no casamento', 'Núria acaba mestrado', 'Gustavo compra consola'],
        ['Gustavo com barba completa', 'Alguém aparece na televisão', 'Elzo é pai', 'Catarina escolhe tema pra tese', 'Fábio tem um incidente com a polícia'],
        ['Elzo aparece + do que 2 vezes', 'Fábio perde um voo', 'Daniela arranja trabalho remunerado', '>= 5 pessoas do grupo nas cegonhas(excl Rita)', 'Miguel muda de emprego'],
        ['Gustavo entra na ordem', 'Catarina compra uma câmera', 'Núria suja o vestido de casamento', 'Rita dá mais do que 5 faltas disciplinares', 'Rita vai à fisioterapia'],
        ['Miguel conhece alguém', 'Elzo chega depois da Núria ao casamento', 'Miguel compra porta talheres', 'Grupo junta se todo num dia', 'Bia aperta mão ao Trump'],
    ],
    [
        ['Bia manda algo pra trás no casamento', 'Miguel conhece alguém', 'Fábio perde um voo', 'Elzo é pai', 'Bia aperta mão ao Trump'],
        ['Elzo aparece + do que 2 vezes', '>= 5 pessoas do grupo nas cegonhas(excl Rita)', 'Gustavo compra consola', 'Catarina compra uma câmera', 'Gustavo com barba completa'],
        ['Daniela corre a meia maratona', 'Fábio tem um incidente com a polícia', 'Gustavo entra na ordem', 'As raparigas vão de férias (pelo menos uma noite)', 'Núria acaba mestrado'],
        ['Rita dá mais do que 5 faltas disciplinares', 'Rita vai à fisioterapia', 'Miguel muda de emprego', 'Daniela arranja trabalho remunerado', 'Catarina escolhe tema pra tese'],
        ['Miguel compra porta talheres', 'Grupo junta se todo num dia', 'Elzo chega depois da Núria ao casamento', 'Núria suja o vestido de casamento', 'Alguém aparece na televisão'],
    ],
    [
        ['As raparigas vão de férias (pelo menos uma noite)', 'Miguel conhece alguém', 'Gustavo compra consola', 'Grupo junta se todo num dia', 'Alguém aparece na televisão'],
        ['Núria acaba mestrado', 'Rita dá mais do que 5 faltas disciplinares', 'Elzo é pai', 'Rita vai à fisioterapia', 'Bia manda algo pra trás no casamento'],
        ['Miguel compra porta talheres', 'Daniela corre a meia maratona', 'Catarina escolhe tema pra tese', 'Bia aperta mão ao Trump', 'Daniela arranja trabalho remunerado'],
        ['Fábio perde um voo', 'Elzo aparece + do que 2 vezes', 'Miguel muda de emprego', 'Catarina compra uma câmera', 'Gustavo entra na ordem'],
        ['>= 5 pessoas do grupo nas cegonhas(excl Rita)', 'Fábio tem um incidente com a polícia', 'Elzo chega depois da Núria ao casamento', 'Gustavo com barba completa', 'Núria suja o vestido de casamento'],
    ],
    [
        ['Núria suja o vestido de casamento', 'Alguém aparece na televisão', 'Catarina compra uma câmera', 'Fábio tem um incidente com a polícia', 'Catarina escolhe tema pra tese'],
        ['Bia manda algo pra trás no casamento', '>= 5 pessoas do grupo nas cegonhas(excl Rita)', 'Gustavo compra consola', 'Elzo é pai', 'Miguel muda de emprego'],
        ['Gustavo com barba completa', 'Fábio perde um voo', 'Rita vai à fisioterapia', 'Daniela arranja trabalho remunerado', 'Miguel compra porta talheres'],
        ['Bia aperta mão ao Trump', 'Rita dá mais do que 5 faltas disciplinares', 'Daniela corre a meia maratona', 'Elzo chega depois da Núria ao casamento', 'Elzo aparece + do que 2 vezes'],
        ['Gustavo entra na ordem', 'Núria acaba mestrado', 'Grupo junta se todo num dia', 'Miguel conhece alguém', 'As raparigas vão de férias (pelo menos uma noite)'],
    ],
    [
        ['Alguém aparece na televisão', 'Gustavo compra consola', 'As raparigas vão de férias (pelo menos uma noite)', 'Gustavo com barba completa', '>= 5 pessoas do grupo nas cegonhas(excl Rita)'],
        ['Rita dá mais do que 5 faltas disciplinares', 'Catarina escolhe tema pra tese', 'Elzo aparece + do que 2 vezes', 'Fábio tem um incidente com a polícia', 'Catarina compra uma câmera'],
        ['Gustavo entra na ordem', 'Grupo junta se todo num dia', 'Bia manda algo pra trás no casamento', 'Fábio perde um voo', 'Miguel muda de emprego'],
        ['Núria acaba mestrado', 'Miguel conhece alguém', 'Elzo chega depois da Núria ao casamento', 'Núria suja o vestido de casamento', 'Rita vai à fisioterapia'],
        ['Bia aperta mão ao Trump', 'Miguel compra porta talheres', 'Elzo é pai', 'Daniela corre a meia maratona', 'Daniela arranja trabalho remunerado'],
    ],
]



# ---------------- FUNCTIONS ----------------
def get_winning_lines(board):
    lines = []
    for r in range(GRID_SIZE):
        lines.append({(r, c) for c in range(GRID_SIZE)})
    for c in range(GRID_SIZE):
        lines.append({(r, c) for r in range(GRID_SIZE)})
    lines.append({(i, i) for i in range(GRID_SIZE)})
    lines.append({(i, GRID_SIZE-1-i) for i in range(GRID_SIZE)})
    return lines

# ---------------- STREAMLIT DASHBOARD ----------------
st.set_page_config(page_title="Bingo Dashboard", layout="wide")
st.title("🎉 Bingo Dashboard – Acontecimentos 🎉")

# Sidebar: happenings
st.sidebar.header("Marque os acontecimentos")
marked = {a: st.sidebar.checkbox(a, key=a) for a in lista_acontecimentos}
marked_set = {a for a, v in marked.items() if v}

# Display boards
winners = []
near_winners = []

num_boards = len(pre_generated_boards)
cols = st.columns(min(num_boards, 5))  # up to 5 per row

for idx, board in enumerate(pre_generated_boards):
    col = cols[idx % len(cols)]
    col.subheader(lista_pessoas[idx % len(lista_pessoas)])
    board_lines = get_winning_lines(board)
    winning_coords = []

    for line in board_lines:
        line_items = {board[r][c] for r, c in line}
        if line_items.issubset(marked_set):
            winners.append((idx, line))
            winning_coords.extend(list(line))
        elif len(line_items - marked_set) == 1:
            near_winners.append((idx, line, line_items - marked_set))

    # Render board
    for r in range(GRID_SIZE):
        row_html = ""
        for c in range(GRID_SIZE):
            cell = board[r][c]
            if (r, c) in winning_coords:
                color = "#ffd966"  # gold
            elif cell in marked_set:
                color = "#b6f2b6"  # green
            else:
                color = "#ffffff"  # white
            row_html += f'<div style="display:inline-block;width:140px;height:60px;border:1px solid #000;background-color:{color};text-align:center;vertical-align:middle;padding:5px;">{cell}</div>'
        col.markdown(row_html, unsafe_allow_html=True)

# Status
status_text = ""
if winners:
    status_text += "🎉 Vencedores: " + ", ".join(lista_pessoas[idx % len(lista_pessoas)] for idx, _ in winners) + "\n"
if near_winners:
    status_text += "⚠️ Quase bingo: " + ", ".join(
        f"{lista_pessoas[idx % len(lista_pessoas)]} ({list(missing)[0]})" for idx, _, missing in near_winners
    )
if not status_text:
    status_text = "❌ Ainda não há vencedores."

st.markdown(f"### {status_text}")

