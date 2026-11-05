# App Store 출시 안내

## 현재 상태
- 앱 코드, iOS 프로젝트, 심사 제출 자료 준비 완료
- 남은 작업: Mac에서 빌드·실기기 확인·업로드, App Store Connect 입력·심사 제출
- Xcode 빌드와 실제 iPhone 실행은 미검증 (작업 환경이 Linux). 첫 빌드 오류 가능성 있음

## 반영 내용 (2026-11-05)

| 항목 | 내용 | 이유 |
|---|---|---|
| 데이터 저장 | 앱 전용 파일 `Library/mjg-todo.json`에 함께 저장, 실행 시 복구 | iOS가 웹뷰 저장소를 비우면 목록이 사라질 위험 차단 |
| 이미지 저장 | iOS 공유 시트로 사진 저장·공유 (`@capacitor/share`) | 웹 공유 기능은 앱 안에서 동작이 불안정함 |
| 외부 접속 | 앱 빌드에서 Google Fonts 요청 제거 | 개인정보 라벨을 "수집 안 함"으로 두기 위함, 오프라인 동작 |
| 개인정보 매니페스트 | `ios/App/App/PrivacyInfo.xcprivacy` 추가 (추적 없음, 파일 시간 API 사유 C617.1) | 매니페스트 누락 시 업로드 단계에서 경고·반려 |
| Info.plist | 필수 기기 조건 `armv7` → `arm64` | 64비트 전용 기기 기준으로 정리 |
| 공개 페이지 | 개인정보 처리방침, 지원 페이지 | App Store Connect 필수 URL |
| 스크린샷 | `screenshots/` 6.9형 1320×2868 4장 | 필수 제출 이미지 |
| 스토어 문구 | [`metadata.md`](metadata.md) | 이름·설명·키워드·심사 메모 초안 |

- 개인정보 처리방침 URL: `https://awevhnfio.github.io/mjg-todo/privacy.html`
- 지원 URL: `https://awevhnfio.github.io/mjg-todo/support.html`
- 두 URL은 `main`에 합친 뒤 GitHub Pages 배포가 끝나야 열림

## 요청 사항
- Apple Developer Program 가입 필요: 연 99 USD (원화 금액은 Apple 결제 화면 확인 필요). 개인 가입 시 판매자 이름에 실명 표시
- 앱 이름 확정 필요: `하고 싶은 일` 사용 가능 여부는 App Store Connect에서 앱 생성 시 확인
- 번들 ID 확정 필요: 현재 `app.mjgtodo.notebook`. 첫 업로드 뒤 변경 불가
- 폰트 라이선스 확인 필요: 온글잎 해원 폰트의 **앱 임베딩·배포** 허용 여부 (웹 임베딩 허용만 확인된 상태)
- 문의 창구 결정 필요: 현재 GitHub 이슈만 안내. 이메일 추가 시 `app/pages/support.html` 수정
- EU 배포 여부 결정 필요: EU 국가에 배포하려면 App Store Connect에서 디지털서비스법(DSA) 거래자 여부 선언 필요. 원치 않으면 배포 국가에서 EU 제외
- 가격: 무료 권장 (유료·인앱 결제는 계약·세금 정보 추가 입력 필요)

## 리스크와 대응
- 심사 지침 4.2(최소 기능) 반려 가능성: 웹 기반 앱이라 "웹사이트 포장"으로 볼 여지 있음
  - 대응: 오프라인 동작, 카메라·사진으로 스티커 만들기, 공유 시트 연동을 심사 메모에 명시
  - 반려 시: 홈 화면 위젯, 햅틱 등 기기 기능 추가 후 재제출
- 기기 간 동기화 없음: 앱 삭제 시 데이터 함께 삭제됨. 지원 페이지에 안내함
- 첫 빌드 오류 가능성: Swift Package 의존성(Capacitor 8.5.3, Filesystem 8.1.4, Share 8.0.3) 받는 중 오류 시 오류 문구 전달 필요

## Mac에서 할 일

### 1. 빌드 준비

```bash
git clone https://github.com/awevhnfio/mjg-todo.git
```

```bash
cd mjg-todo/app/capacitor && npm install && npx cap sync ios && npx cap open ios
```

- Xcode는 최신 버전 사용. App Store 업로드에 필요한 최소 SDK 버전은 Apple 공지 확인 필요
- `notebook.html`을 고친 경우 `python3 app/build_app.py` 실행 후 `npx cap sync ios` 다시 실행

### 2. 서명 설정
- Xcode 왼쪽 **App** → TARGETS **App** → **Signing & Capabilities**
- **Team**: 유료 개발자 계정 선택
- **Bundle Identifier**: 확정한 번들 ID 입력
- **General** 탭: Version `1.0`, Build `1` (업로드할 때마다 Build 숫자 증가 필요)

### 3. 실기기 확인 목록
- [ ] 할 일 추가·수정·삭제, 하위 항목, 수첩 추가
- [ ] 동그라미 눌러 스티커 붙이기, 길게 눌러 고르기
- [ ] 사진으로 내 스티커 만들기 (카메라·사진 권한 문구 확인)
- [ ] 랜덤: 내 스티커가 있을 때 내 스티커만 붙는지
- [ ] 이미지 내보내기 → `공유 · 사진에 저장` → 사진 앱에 저장되는지
- [ ] 앱 완전 종료 후 다시 열어 목록 유지
- [ ] 비행기 모드에서 실행·글씨체 정상
- [ ] 다크 모드, 테마(피치·소다) 전환
- [ ] 하단 문구 `이 아이폰에 저장돼요` 표시

### 4. App Store Connect 앱 생성
- [appstoreconnect.apple.com](https://appstoreconnect.apple.com) → 앱 → **+** → 신규 앱
- 플랫폼 iOS, 이름, 기본 언어 한국어, 번들 ID, SKU(예: `mjg-todo-ios`) 입력

### 5. 업로드
- Xcode 위쪽 기기를 **Any iOS Device (arm64)**로 변경
- **Product → Archive** → Organizer에서 **Distribute App** → **App Store Connect** → Upload
- 처리 완료까지 수십 분 걸릴 수 있음. 완료 시 이메일 수신
- 선택: TestFlight 내부 테스트로 본인 iPhone에서 먼저 확인

### 6. 스토어 정보 입력
- [`metadata.md`](metadata.md) 문구 붙여넣기
- 스크린샷: `screenshots/` 4장을 6.9형 디스플레이 칸에 업로드
- **앱 개인정보**: "데이터를 수집하지 않음" 선택
- **연령 등급**: 설문 항목 모두 "없음" 선택
- **수출 규정**: Info.plist에 `ITSAppUsesNonExemptEncryption = NO` 설정되어 있어 별도 질문 없음
- **가격 및 사용 가능 여부**: 무료, 배포 국가 선택

### 7. 심사 제출
- 빌드 선택 → 심사 메모 입력 → **심사에 추가** → 제출
- 반려 시 사유 문구 전달 필요. 대응 방안 정리 예정
