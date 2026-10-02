# MenuNori 영어 검색 운영

기준일: 2026-10-02 · 기준 주소: https://menunori.com

## 검색어와 페이지 역할

아래는 사이트가 실제로 답할 수 있는 검색 의도에 따른 후보입니다. 검색량·경쟁도·순위는 측정하지 않았습니다. Search Console에 쌓이는 실제 검색어와 페이지별 노출·클릭을 보고 조정합니다.

| 페이지 | 주 검색어 후보 | 답하는 문제 |
| --- | --- | --- |
| `/` | Korean kiosk practice, practice ordering food in Korea | 여행 전 직접 메뉴·옵션을 선택하는 무료 연습 |
| `/guides/` | how to order food in Korea, ordering food in Korea without speaking Korean | 식당 주문을 처음부터 이해하는 영어 안내와 세부 가이드 연결 |
| `/guides/korean-kiosk/` | how to use a Korean restaurant kiosk, Korean kiosk buttons in English | 주문 화면의 순서·한글 버튼·옵션·확인 |
| `/guides/read-korean-menu/` | how to read a Korean menu, Korean menu in English | 분식 메뉴 이름·가격·수량 읽기 |
| `/guides/dine-in-takeaway/` | to go in Korean, takeaway in Korean, 포장 meaning | 포장·매장 버튼과 실제 요청 문장 |
| `/guides/spice-and-extras/` | Korean menu spice levels, mild in Korean | 순한맛·보통맛·맵기·추가 옵션 구분 |
| `/guides/check-your-order/` | Korean kiosk order confirmation, Korean kiosk basket | 결제 전에 잘못된 메뉴·수량·옵션 찾기 |
| `/guides/quantity-and-prices/` | Korean menu prices, Korean servings 인분 | 원화·개·인분·합계 계산 |
| `/guides/restaurant-ordering-phrases/` | how to order food in Korean, Korean restaurant ordering phrases | 음식 이름·수량·주세요를 이용한 짧은 요청 |

`order food in Korea`는 배달·실제 주문 의도도 포함할 수 있습니다. 홈은 반드시 **practice**를 명시하고, 가이드는 식당 방문·메뉴·키오스크라는 범위를 설명합니다. 배달 앱 안내나 실제 식당 주문 서비스처럼 소개하지 않습니다.

## 사이트 적용

- 영어 제목·검색 설명·본문 첫 문장을 페이지의 구체적인 질문에 맞췄습니다.
- 가이드 첫 설명은 목차보다 먼저 보이며, JavaScript 없이도 본문과 관련 링크가 HTML에 있습니다.
- 홈 가이드 링크는 목적을 설명하는 문구를 사용합니다. 영어 UI와 한국어 학습 예시를 유지합니다.
- canonical, 사이트맵, robots.txt와 구조화 데이터의 주소는 `menunori.com`을 사용합니다.
- 가이드는 Article, 탐색 경로는 BreadcrumbList, 홈은 WebSite 데이터를 제공합니다. 구조화 데이터가 검색 표시나 순위를 보장하지는 않습니다.
- 실제 번역 페이지가 없으므로 언어별 URL·hreflang을 만들지 않습니다. 의미 없는 meta keywords나 검색어 반복 문단을 넣지 않습니다.
- Search Console과 AdSense 소유권 확인 태그를 보존합니다. 이 태그가 색인이나 승인을 완료해 주는 것은 아닙니다.

## Search Console에서 운영자가 할 일

1. `menunori.com`에 해당하는 속성의 소유권 확인을 완료합니다. URL 접두어 속성이면 `https://menunori.com/`을 선택합니다.
2. **Sitemaps**에서 `https://menunori.com/sitemap.xml`을 제출하고 읽기 성공 여부를 확인합니다.
3. **URL inspection**에서 홈, `/guides/`, `/guides/korean-kiosk/`를 하나씩 검사합니다. 새 페이지가 아직 색인되지 않았다면 실시간 URL 테스트 후 **Request indexing**을 사용할 수 있습니다.
4. **Page indexing**에서 색인 여부와 제외 사유를 확인합니다. 검색 결과 노출·순위와 HTTP 200 응답은 별도입니다.
5. **Performance → Search results**에서 검색어·페이지·국가별 노출수, 클릭수, CTR, 평균 게재순위를 확인합니다. 초기에는 데이터가 충분히 쌓이지 않을 수 있습니다.

2~4주 뒤의 첫 점검은 운영 일정이며 Google 처리 시간의 보장이 아닙니다. 노출은 있지만 클릭이 적으면 실제 검색어와 제목의 약속이 맞는지 확인합니다. 색인되지 않았다면 색인 보고서부터 확인합니다. 유입된 사람이 찾던 답을 얻을 수 있도록 본문을 수정합니다. 영어를 사용하는 여행자는 여러 국가에 있으므로 국가 필터만으로 대상 여부를 단정하지 않습니다.

기존 URL은 유지합니다. 새 글은 실제로 빠진 주문 상황이 발견되거나 이용자가 질문한 경우에 추가하며, 비슷한 검색어만 바꾼 중복 페이지를 만들지 않습니다.

## 공식 참고

- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Google 검색 제목 안내](https://developers.google.com/search/docs/appearance/title-link)
- [Google 재크롤링·색인 요청 안내](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl)
