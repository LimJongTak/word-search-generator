import random
import string
import io
import os
from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

app = Flask(__name__)

# --- 한글 폰트 설정 ---
FONT_NAME = 'NanumGothicBold'
try:
    font_path = os.path.join(os.path.dirname(__file__), 'NanumGothic-Bold.ttf')
    pdfmetrics.registerFont(TTFont(FONT_NAME, font_path))
except Exception as e:
    FONT_NAME = 'Helvetica-Bold'

class WordSearch:
    def __init__(self, size=24, difficulty=5):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.solution_mask = [[False for _ in range(size)] for _ in range(size)]
        
        self.directions = [(0, 1), (1, 0)] 
        if difficulty > 3:
            self.directions.extend([(1, 1), (1, -1)])
        if difficulty > 7:
            self.directions.extend([(0, -1), (-1, 0), (-1, -1), (-1, 1)])

    def place_word(self, word):
        word = word.upper().replace(" ", "")
        placed = False
        attempts = 0
        while not placed and attempts < 200:
            d = random.choice(self.directions)
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)
            
            if self.can_place(word, r, c, d):
                for i, char in enumerate(word):
                    self.grid[r + d[0]*i][c + d[1]*i] = char
                    self.solution_mask[r + d[0]*i][c + d[1]*i] = True
                placed = True
            attempts += 1

    def can_place(self, word, r, c, d):
        for i, char in enumerate(word):
            nr, nc = r + d[0]*i, c + d[1]*i
            if not (0 <= nr < self.size and 0 <= nc < self.size):
                return False
            if self.grid[nr][nc] != '' and self.grid[nr][nc] != char:
                return False
        return True

    def fill_random(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == '':
                    self.grid[r][c] = random.choice(string.ascii_uppercase)

def draw_puzzle(c, ws, words, is_answer=False):
    width, height = landscape(A4)
    cell_size = 17 
    
    # 1. 제목 [cite: 5]
    title = "숨은 영어 단어 찾기 (정답지)" if is_answer else "숨은 영어 단어 찾기"
    c.setFont(FONT_NAME, 22)
    c.drawCentredString(width/2, height - 40, title)

    # 2. 그리드 영역 [cite: 1]
    grid_total_width = ws.size * cell_size
    start_x = (width - grid_total_width) / 2 + 8
    start_y = height - 80 

    for r in range(ws.size):
        for col in range(ws.size):
            if is_answer and ws.solution_mask[r][col]:
                c.setFillColor(colors.red)
                c.setFont("Helvetica-Bold", 12)
            else:
                c.setFillColor(colors.black)
                c.setFont("Helvetica", 12)
            
            char = ws.grid[r][col]
            c.drawCentredString(start_x + col*cell_size, start_y - r*cell_size, char)

    # 3. 하단 구분선
    line_y = start_y - (ws.size * cell_size) - 15
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.2)
    c.line(50, line_y, width-50, line_y)

    # 4. 단어 리스트 (한 줄에 6개씩 3줄 배치로 수정)
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 14)
    c.drawString(60, line_y - 25, "찾아야 할 단어 목록:")
    
    c.setFont("Helvetica-Bold", 10)
    
    # 18개 단어를 가로 6개, 세로 3줄로 배치
    list_base_y = line_y - 45
    for i, word in enumerate(words):
        row_idx = i // 6   # 0, 1, 2행 (총 3줄)
        col_idx = i % 6    # 0, 1, 2, 3, 4, 5열 (한 줄에 6개)
        
        # 가로 간격(width 분할) 조정
        x_pos = 70 + (col_idx * 130) # 열 간격을 130으로 좁혀서 6개가 들어가게 함
        # 세로 간격 조정
        y_pos = list_base_y - (row_idx * 18) 
        
        c.drawString(x_pos, y_pos, f"■ {word.upper()}")

@app.route('/')
def index():
    # 제시어 목록 [cite: 4, 7]
    default_words = [
        "DOCTOR", "JUDGE", "CHEF", "TEACHER", "SPORTSMAN", "SINGER",
        "ACTOR", "FIREFIGHTER", "POLICE", "PROFESSOR", "EMPLOYEE", "SOLDIER",
        "SCIENTIST", "PRESIDENT", "ANNOUNCER", "ANCHOR", "REPORTER", "ARTIST"
    ]
    return render_template('index.html', default_words=default_words)

@app.route('/generate', methods=['POST'])
def generate():
    words = []
    for i in range(1, 19):
        w = request.form.get(f'word_{i}', '').strip()
        if w: words.append(w)
    
    difficulty = int(request.form.get('difficulty', 5))
    ws = WordSearch(size=24, difficulty=difficulty) # 24x24 사이즈 [cite: 1, 5]
    for w in words:
        ws.place_word(w)
    ws.fill_random()

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    
    draw_puzzle(p, ws, words, is_answer=False)
    p.showPage()
    draw_puzzle(p, ws, words, is_answer=True)
    p.showPage()
    
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="word_search_jobs.pdf")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)