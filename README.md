# MenuNori

제레미가 운영하는 한국 식당 주문 연습 서비스의 첫 버전입니다.

- 분식집 1곳, 메뉴 6개, 미션 5개
- 외국인 여행자를 위한 영어 UI와 한국어 메뉴·주문 표현, 포장·매장, 수량, 맵기, 치즈 추가
- 장바구니 수정, 총액 확인, 오답 피드백, 다음 미션
- 원본 여행 가이드 5편과 소개·개인정보·이용 안내
- 실제 결제, 계정, 음성 수집, 광고·분석 스크립트 없음

`dist/`가 바로 배포 가능한 정적 웹사이트입니다. 별도의 패키지 설치나 빌드는 필요 없습니다.

## 로컬 확인

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

브라우저에서 http://127.0.0.1:4173 를 엽니다.

## 수정 위치

게임 화면 `dist/index.html`, 주문 기능·안내 `dist/assets/app.js`, 디자인 `dist/assets/style.css`.
해설과 안내 페이지는 `generate-pages.py`에서 수정한 후 `python3 generate-pages.py`를 실행합니다.
메뉴 사진은 자체 AI 생성 자산이며 실제 식당 사진이 아닙니다. 소셜 미리보기 이미지와 혼용하지 않습니다.

현재 canonical과 sitemap 기준 주소는 `.openai/hosting.json`의 프로젝트에 연결된 Sites 주소입니다. 도메인 변경 시 생성기의 `origin`과 홈 canonical도 함께 갱신하세요.

애드센스 관련 남은 사항은 `LAUNCH.md`를 확인하세요.
