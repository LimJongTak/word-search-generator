# 🔍 숨은 단어 찾기 생성기 (Word Search Generator)

[cite_start]아이들을 위한 교육용 단어 찾기 학습지를 자동으로 생성하고 PDF로 다운로드할 수 있는 웹 애플리케이션입니다. [cite: 1, 4] [cite_start]사용자가 입력한 단어 목록을 바탕으로 매번 새로운 퍼즐을 생성하며, 정답지까지 함께 제공합니다. [cite: 5, 6]

## ✨ 주요 기능

- [cite_start]**24x24 대형 그리드**: 다양한 단어를 빽빽하게 배치할 수 있는 넉넉한 크기의 격자를 제공합니다. [cite: 1]
- [cite_start]**동적 단어 목록 관리**: 기본 제공되는 18개 단어 외에도 사용자가 직접 입력창을 추가하거나 삭제하여 단어 개수를 자유롭게 조절할 수 있습니다. [cite: 4]
- **다국어 모드 지원**: 
  - **영어 모드**: 알파벳 대문자로 구성된 퍼즐을 생성합니다.
  - **한국어 모드**: 한글 음절로 구성된 퍼즐을 생성하며, 빈칸 역시 무작위 한글로 채워집니다.
- **세분화된 난이도 (1~100)**: 1부터 100까지의 수치에 따라 가로, 세로, 대각선, 역방향 배치를 동적으로 조절하여 난이도를 설정할 수 있습니다.
- [cite_start]**자동 PDF 생성**: A4 가로(Landscape) 모드에 최적화된 문제지와 정답지(2페이지)를 자동으로 생성하여 다운로드합니다. [cite: 5, 6]
- **한글 폰트 완벽 지원**: `NanumGothic-Bold` 폰트를 사용하여 PDF 출력 시 한글 제목과 리스트가 깨지지 않고 선명하게 출력됩니다.
- **UI 편의 기능**: 모든 입력창을 즉시 비울 수 있는 '전체 초기화' 버튼과 언어별 기본 단어 자동 셋팅 기능을 제공합니다.



## 🛠 기술 스택

- **Language**: Python 3.10+
- **Framework**: Flask
- **Library**: ReportLab (PDF Generation)
- **Deployment**: Render
- **Frontend**: HTML5, CSS3, JavaScript (Jinja2 Template)

## 🚀 로컬 실행 방법

1. 저장소를 클론합니다.
   ```bash
   git clone [https://github.com/LimJongTak/word-search-generator.git](https://github.com/LimJongTak/word-search-generator.git)