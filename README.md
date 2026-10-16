# 하고 싶은 일 목록

손글씨 수첩 느낌의 아이폰용 투두 앱입니다. 끝낸 일에 스티커를 붙이고, 내 사진으로 누끼 스티커를 만들고, 수첩을 여러 권 쓸 수 있습니다.

| 경로 | 내용 |
|---|---|
| `notebook.html` | 앱 원본 (한 파일짜리 웹앱, Claude Artifact로도 게시됨) |
| `DESIGN.md` | 설계 문서 |
| `app/` | 아이폰 앱 패키지 — 설치 방법은 [`app/README.md`](app/README.md) |
| `app/pwa/` | 홈 화면 앱(PWA). HTTPS로 호스팅 후 Safari → 홈 화면에 추가 |
| `app/capacitor/` | Xcode용 iOS 앱 프로젝트 (Capacitor 8) |
| `app/build_app.py` | `notebook.html`에서 `pwa/`·`capacitor/www/`를 다시 만드는 스크립트 |
| `Ownglyph_haewonny-Rg.ttf` | 온글잎 해원 폰트 원본 (© VoyagerX, inc. & Haewon Lee) |

> 폰트 라이선스: 온글잎 해원 폰트는 저작권자(VoyagerX)에게 권리가 있습니다. 공개 저장소나 배포에 쓰기 전에 라이선스를 확인하세요.
