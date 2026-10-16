# 하고 싶은 일 목록 — 아이폰 앱 패키지

아이폰에 설치하는 방법은 두 가지입니다.

| | A. 홈 화면 앱 (PWA) | B. 정식 iOS 앱 (Xcode) |
|---|---|---|
| 필요한 것 | 무료 웹 호스팅 1곳 | Mac + Xcode + Apple ID |
| 설치 | Safari → 공유 → 홈 화면에 추가 | Xcode에서 아이폰으로 실행 |
| 앱 아이콘·전체 화면 | ✅ | ✅ |
| 오프라인 | ✅ (서비스 워커 캐시) | ✅ (앱 안에 파일 포함) |
| 유효 기간 | 제한 없음 | 무료 Apple ID: **7일마다 다시 설치**, 유료 개발자($99/년): 1년, TestFlight/App Store 배포 가능 |
| 파일 | `mjg-todo-pwa.zip` (`pwa/`) | `mjg-todo-ios-project.zip` (`capacitor/`) |

> 둘 다 데이터는 **그 아이폰 안에만** 저장됩니다(localStorage). Claude 앱에서 쓰던 목록과는 이어지지 않고, 기기 간 동기화도 안 됩니다.

---

## A. 홈 화면 앱 (PWA) — 추천

1. `mjg-todo-pwa.zip`을 풀어 나온 파일들을 HTTPS 호스팅에 올립니다. 예:
   - **Netlify Drop**: https://app.netlify.com/drop 에 `pwa` 폴더를 끌어다 놓기 (가입 후 무료)
   - **GitHub Pages**: 저장소에 `pwa` 폴더 내용을 올리고 Settings → Pages 켜기
2. 아이폰 **Safari**로 받은 주소를 엽니다. (Chrome 등 다른 브라우저는 안 됩니다.)
3. 공유 버튼(□↑) → **홈 화면에 추가** → 이름 `하고 싶은 일` 확인 → 추가.
4. 홈 화면 아이콘으로 열면 주소창 없이 앱처럼 열립니다. 한 번 연 뒤에는 인터넷이 없어도 열립니다.

- 업데이트: 호스팅 파일을 바꾸면, 앱을 인터넷 연결 상태로 다시 열 때 새 버전이 들어옵니다.
- 이미지 내보내기: `공유 · 사진에 저장` 버튼(공유 시트)이나 이미지를 길게 눌러 저장합니다.
- 주의: 홈 화면 앱의 데이터는 Safari와 따로 저장됩니다. 홈 화면 아이콘을 지우면 데이터도 지워집니다.

## B. 정식 iOS 앱 (Capacitor + Xcode)

준비: Mac, Xcode 16 이상, Node.js 20 이상, Apple ID(Xcode → Settings → Accounts에 로그인)

```bash
unzip mjg-todo-ios-project.zip -d mjg-todo-ios
cd mjg-todo-ios/capacitor
npm install
npx cap sync ios        # 웹 파일과 플러그인을 iOS 프로젝트에 반영
npx cap open ios        # Xcode가 열림
```

Xcode에서:
1. 왼쪽에서 **App** 프로젝트 → TARGETS **App** → **Signing & Capabilities**
2. **Team**에 내 Apple ID 선택. 번들 ID(`app.mjgtodo.notebook`)가 이미 쓰이고 있다고 나오면 `app.<내이름>.notebook`처럼 바꿉니다.
3. 아이폰을 USB로 연결 → 위쪽 기기 목록에서 내 아이폰 선택 → ▶ 실행
4. 아이폰에서 처음 실행할 때: **설정 → 일반 → VPN 및 기기 관리 → 내 Apple ID → 신뢰**
   (iOS 16 이상은 **설정 → 개인정보 보호 및 보안 → 개발자 모드** 켜기도 필요)

설정해 둔 것:
- 앱 이름 `하고 싶은 일`, 아이콘·실행 화면(분홍 수첩), 아이폰 전용·세로 화면 고정
- 카메라/사진 보관함 권한 문구(스티커 만들기, 이미지 저장용)
- Capacitor 8.5.3, iOS 15 이상, Swift Package Manager 사용(CocoaPods 불필요)

## 앱을 고친 뒤 다시 만들기

`notebook.html`(앱 원본)을 고친 다음, 원본이 있는 폴더 구조(`mjg-todo/notebook.html`, `mjg-todo/app/build_app.py`)에서:

```bash
cd mjg-todo/app
python3 build_app.py              # pwa/, capacitor/www/, mjg-todo-pwa.zip 다시 생성
cd capacitor && npx cap sync ios  # 정식 앱에 반영 (Mac에서)
```

## 확인한 것 / 못 한 것

- ✅ PWA: 로컬 서버에서 서비스 워커 등록, manifest, **오프라인 상태로 다시 열기**(데이터 유지)를 Chromium으로 확인
- ✅ iOS 프로젝트: `npx cap add ios`로 Xcode 프로젝트 생성, 아이콘·실행 화면·Info.plist 설정
- ❌ 이 작업 환경은 Linux라 **Xcode 빌드와 실제 아이폰 실행은 하지 못했습니다.** 처음 빌드할 때 오류가 나면 메시지를 알려 주세요.
- ⚠️ 정식 앱 안에서 `공유 · 사진에 저장` 버튼이 안 보이면, 미리보기 이미지를 길게 눌러 저장하세요.
- 앱 안에 넣은 **온글잎 해원 폰트**는 웹·앱 배포 시 라이선스(임베딩 허용 범위)를 꼭 확인하세요. App Store에 올릴 때는 특히 필요합니다.
