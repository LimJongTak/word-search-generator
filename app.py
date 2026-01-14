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
    print(f"Font Load Error: {e}")
    FONT_NAME = 'Helvetica-Bold'

class WordSearch:
    def __init__(self, size=24, difficulty=50):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.solution_mask = [[False for _ in range(size)] for _ in range(size)]
        
        # 난이도 1~100 로직
        self.directions = [(0, 1), (1, 0)]  # 기본 가로, 세로
        if difficulty > 25: self.directions.extend([(1, 1), (1, -1)])  # 대각선
        if difficulty > 50: self.directions.extend([(0, -1), (-1, 0)])  # 역방향 가로/세로
        if difficulty > 75: self.directions.extend([(-1, -1), (-1, 1)]) # 역방향 대각선

    def place_word(self, word):
        word = word.upper().replace(" ", "")
        placed = False
        attempts = 0
        while not placed and attempts < 300:
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
            if not (0 <= nr < self.size and 0 <= nc < self.size): return False
            if self.grid[nr][nc] != '' and self.grid[nr][nc] != char: return False
        return True

    def fill_random(self, lang='en'):
        kr_pool = "가나다라마바사아자차카타파하각난닫랄맘밥삿앙잦챷캌탙팦핳"
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == '':
                    self.grid[r][c] = random.choice(kr_pool if lang == 'ko' else string.ascii_uppercase)

def draw_puzzle(c, ws, words, is_answer=False, lang='en'):
    width, height = landscape(A4)
    cell_size = 17
    title = f"숨은 단어 찾기 ({'정답지' if is_answer else '문제지'})"
    
    c.setFont(FONT_NAME, 22)
    c.drawCentredString(width/2, height - 40, title)

    start_x = (width - (ws.size * cell_size)) / 2 + 8
    start_y = height - 80 

    for r in range(ws.size):
        for col in range(ws.size):
            char = ws.grid[r][col]
            if is_answer and ws.solution_mask[r][col]:
                c.setFillColor(colors.red)
                c.setFont(FONT_NAME if lang == 'ko' else "Helvetica-Bold", 12)
            else:
                c.setFillColor(colors.black)
                c.setFont(FONT_NAME if lang == 'ko' else "Helvetica", 12)
            c.drawCentredString(start_x + col*cell_size, start_y - r*cell_size, char)

    line_y = start_y - (ws.size * cell_size) - 15
    c.setStrokeColor(colors.black)
    c.line(50, line_y, width-50, line_y)
    
    c.setFont(FONT_NAME, 14)
    c.setFillColor(colors.black)
    c.drawString(60, line_y - 25, f"단어 목록 (총 {len(words)}개):")
    
    c.setFont(FONT_NAME, 10)
    for i, word in enumerate(words):
        row, col = i // 6, i % 6
        c.drawString(80 + (col * 130), line_y - 45 - (row * 18), f"■ {word.upper()}")

@app.route('/')
def index():
    en_list = ["DOCTOR", "JUDGE", "CHEF", "TEACHER", "SPORTSMAN", "SINGER", "ACTOR", "FIREFIGHTER", "POLICE", "PROFESSOR", "EMPLOYEE", "SOLDIER", "SCIENTIST", "PRESIDENT", "ANNOUNCER", "ANCHOR", "REPORTER", "ARTIST"]
    ko_list = ["의사", "판사", "요리사", "선생님", "운동선수", "가수", "배우", "소방관", "경찰관", "교수", "회사원", "군인", "과학자", "대통령", "아나운서", "앵커", "기자", "화가"]
    return render_template('index.html', en=en_list, ko=ko_list)

@app.route('/generate', methods=['POST'])
def generate():
    lang = request.form.get('lang', 'en')
    diff = int(request.form.get('difficulty', 50))
    words = [request.form.get(k).strip() for k in sorted(request.form.keys()) if k.startswith('word_') and request.form.get(k).strip()]
    
    ws = WordSearch(size=24, difficulty=diff)
    for w in words: ws.place_word(w)
    ws.fill_random(lang)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    draw_puzzle(p, ws, words, False, lang)
    p.showPage()
    draw_puzzle(p, ws, words, True, lang)
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"wordsearch_{lang}.pdf")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)