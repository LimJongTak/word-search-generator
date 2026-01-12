# 🔍 숨은 영어 낱말 찾기 생성기 (Word Search Generator)

[cite_start]아이들을 위한 교육용 영어 낱말 찾기 학습지를 자동으로 생성하고 PDF로 다운로드할 수 있는 웹 애플리케이션입니다. [cite: 1, 4]

## ✨ 주요 기능
- [cite_start]**24x24 대형 그리드**: 다양한 단어를 빽빽하게 배치할 수 있는 넉넉한 크기 제공 [cite: 1]
- [cite_start]**18개 단어 입력**: 직업 관련 기본 단어 18개를 포함하여 사용자 정의 단어 입력 가능 [cite: 4]
- **난이도 조절 (1~10단계)**: 난이도에 따라 가로, 세로, 대각선, 역방향 배치를 동적으로 조절
- [cite_start]**자동 PDF 생성**: A4 가로(Landscape) 모드에 최적화된 문제지와 정답지(2페이지) 자동 생성 [cite: 5, 6]
- **한글 지원**: `NanumGothic-Bold` 폰트를 사용하여 제목과 리스트가 깨지지 않고 선명하게 출력

## 🛠 기술 스택
- **Language**: Python 3.10
- **Framework**: Flask
- **Library**: ReportLab (PDF Generation)
- **Deployment**: Render

## 🚀 로컬 실행 방법
1. 저장소를 클론합니다.
   ```bash
   git clone [https://github.com/사용자이름/저장소이름.git](https://github.com/사용자이름/저장소이름.git)