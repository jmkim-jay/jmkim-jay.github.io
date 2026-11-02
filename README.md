# Jaemin Kim — personal website

홈페이지: https://jmkim-jay.github.io/

## 홈 화면을 가장 쉽게 수정하는 방법

홈 화면의 원본은 **`index.html`**입니다. 소개글이나 링크를 수정할 때 Python을 실행할 필요가 없습니다.

1. GitHub에서 [index.html](https://github.com/jmkim-jay/jmkim-jay.github.io/blob/main/index.html)을 엽니다.
2. 연필 아이콘(Edit this file)을 누릅니다.
3. `[수정]` 주석을 찾아 원하는 문장이나 링크 주소를 바꿉니다.
4. **Commit changes**로 `main` 브랜치에 저장하면 GitHub Pages가 자동 반영합니다.

예를 들어 소개 문장은 `<p>...</p>` 안의 글을 바꾸면 됩니다.

```html
<p>여기에 소개 문장을 작성합니다.</p>
```

링크는 `href` 안의 주소와 화면에 표시할 이름을 수정합니다.

```html
<a href="https://www.linkedin.com/in/jaemin-kim-77413a429/">LinkedIn</a>
```

태그와 `id`, `class`는 유지하고 글이나 주소만 바꾸는 것이 가장 간단합니다. HTML 주석은 실제 홈페이지에 표시되지 않습니다. `scripts/build.py`를 실행해도 `index.html`은 바뀌지 않습니다.

## 파일별 수정 위치

| 내용 | 파일 |
| --- | --- |
| 홈 소개, 소속, 링크, 연구 분야, 이력, 메인 저널 목록 | `index.html` |
| 전체 논문 목록 데이터 | `data/publications.json` |
| 전체 논문 페이지 생성 코드 | `scripts/build.py` |
| 색상, 글꼴, 간격, 모바일 레이아웃 | `assets/style.css` |
| 논문 검색 및 분류 필터 | `assets/site.js` |
| 프로필 사진 | `assets/portrait.jpeg` |

메인 저널 목록은 `index.html`에서 직접 관리하며, 출판일이 최근인 논문을 위에 놓습니다. 전체 논문 목록에는 출판 예정 논문도 포함됩니다.

## 전체 논문 목록을 갱신하는 방법

`data/publications.json`을 수정한 뒤 Python 3으로 아래 명령을 실행합니다.

```sh
python3 scripts/build.py
```

이 명령은 **`publications.html`만 생성**합니다. 데이터 파일과 생성된 `publications.html`을 함께 커밋합니다. 전체 논문 페이지의 머리말이나 하단 링크를 수정할 때는 `scripts/build.py`를 수정하고 같은 명령을 실행합니다.

별도 프레임워크나 패키지 설치는 필요 없습니다. JavaScript 없이도 논문 목록을 읽을 수 있으며, JavaScript를 켜면 검색과 분류 필터를 사용할 수 있습니다.

## GitHub Pages

`main` 브랜치의 루트(`/`)를 배포합니다. `.nojekyll` 파일을 통해 HTML과 에셋이 그대로 게시됩니다. 별도 사용자 정의 Actions 워크플로는 필요 없습니다.

## 자료 출처

사진, 학력, 초기 논문 63편은 [UCLab 개인 페이지](https://uclab.re.kr/jmkim.html)를 기준으로 작성했습니다(확인일: 2026-11-02). 논문 제목과 저자 순서는 해당 기록을 따릅니다.

논문 링크는 UCLab 또는 IEEE Xplore의 원본 주소를 사용하며 PDF를 이 저장소에 재업로드하지 않습니다. “PDF (lab access)”는 UCLab 인증이 필요할 수 있는 링크이고, 공개 PDF가 있으면 공개 링크를 우선 표시합니다.
