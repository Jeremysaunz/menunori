# MenuNori

제레미가 운영하는, 영어권 한국 여행자를 위한 메뉴 읽기·주문 연습 사이트입니다.

- 가상의 분식집: 메뉴 6개, 미션 5개, 매장·포장, 수량·맵기·추가 옵션, 주문표 확인
- 영어 해설 가이드 7편: 원본 메뉴 예제, 계산, 실수 찾기, 짧은 표현, 해당 미션 연결
- 소개, 문의·정정, 콘텐츠 제작 기준, 개인정보, 이용 안내
- 실제 결제·계정·음성 업로드·광고·분석 스크립트 없음

## 배포

GitHub `main`이 기존 Vercel `menunori` 프로젝트와 연결되어 있습니다.
공개 기준 주소: https://menunori.vercel.app

`vercel.json`은 정적 산출물 `dist/`를 배포합니다. 설치·빌드 단계가 필요 없습니다. 실제 없는 경로는 404여야 하므로 모든 경로를 홈으로 돌리는 SPA rewrite는 사용하지 않습니다.

`.openai/hosting.json`은 이전 Sites 확인본의 식별 정보입니다. Vercel 배포에 사용하지 않으며, 이전 비공개 확인본을 AdSense 신청 주소로 사용하지 않습니다.

## 수정과 생성

- 홈: `dist/index.html`
- 주문 게임: `dist/assets/app.js`
- 스타일: `dist/assets/style.css`
- 기존 가이드: `generate-pages.py`
- 보강 예제·추가 가이드: `guide_content.py`
- 공통 페이지·정책·메타데이터 생성: `site_pages.py`
- 공개 도메인·운영자·문의 이메일: `site-config.json`

운영자가 제공한 AdSense 계정은 `site-config.json`의 `adsenseAccount`에 저장합니다. 생성기는 소유권 확인 메타 태그만 HTML head에 넣으며, 광고 스크립트는 실행하지 않습니다.

```sh
python3 generate-pages.py
node --check dist/assets/app.js
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

`site-config.json`의 `contactEmail`은 운영자가 공개를 지정한 이메일만 넣습니다. 현재 null이며 작동하는 GitHub issue 경로를 제공하고 있습니다. 도메인을 변경하면 `origin`을 바꾸고 생성 후 홈 canonical 및 메타데이터도 확인합니다. 생성한 `dist/`도 함께 커밋해야 합니다.

음식 사진은 자체 AI 생성 자산이며 실제 식당의 메뉴·가격·레시피를 나타내지 않습니다. 독립 원어민 검수를 완료했다고 주장하지 않습니다.

AdSense 계정 연결과 심사 준비 상태는 `LAUNCH.md`를 확인하세요.
