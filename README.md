# 블로그 자동 생성 시스템

김포다조은병원 의료 블로그 콘텐츠를 자동으로 생성하는 멀티 에이전트 시스템입니다.

## 특징

- ✅ **Claude Code 기반**: 텍스트 생성은 Claude가 직접 수행
- ✅ **의료법 준수**: 허위과대 광고 자동 검토 및 수정
- ✅ **네이버 블로그 최적화**: 복붙만 하면 되는 완성된 본문
- ✅ **병원 홍보 강화**: 검사/치료 안내 자연스럽게 통합 (15-20%)
- ✅ **이미지 가이드 포함**: 디자이너가 바로 제작 가능한 상세 설명 (별도 파일)
- ✅ **표준화된 구조**: 총 6개 섹션, 3000-3500자 분량
- ✅ **5단계 프로세스**: 전문적인 의료법 검토 품질 보장
- ✅ **바이브코딩**: Claude와 대화하며 단계별 진행
- ✅ **한글 파일명**: 날짜와 주제로 알아보기 쉬운 파일 관리

## 시스템 구조

```
hospital_blog_team/
├── agents/                   # 에이전트 프롬프트 (Claude가 읽고 실행)
│   ├── planner.md           # 1. 키워드 → 아웃라인 (6개 섹션)
│   ├── researcher.md        # 2. 의료 정보 리서치
│   ├── writer.md            # 3. 본문 초안 작성 (이미지 placeholder)
│   ├── compliance_checker.md # 4. 의료법 검토 및 최종 본문 생성
│   └── image_layout_designer.md # 5. 이미지 가이드 (별도 파일)
│
├── temp/                   # 중간 결과물
│   ├── outline.json        # 1단계
│   ├── research.json       # 2단계
│   ├── draft.md            # 3단계 (초안)
│   └── compliance_report.json  # 4단계 (검토 보고서)
│
├── output/                 # 최종 결과물 ⭐
│   ├── [날짜]_[한글제목].md                # 4단계 (최종 본문)
│   └── [날짜]_[한글제목]_이미지가이드.md   # 5단계 (이미지 가이드)
│
└── blog_generator/         # ⚠️ 현재 미사용 (향후 자동 이미지 생성 기능용)
    ├── generate_images.py  # Imagen API 이미지 생성 스크립트
    └── imagen_client.py    # Google Imagen 클라이언트
```

**최종 결과물**:
- `output/[날짜]_[한글제목].md` → 네이버 블로그에 그대로 복사/붙여넣기
- `output/[날짜]_[한글제목]_이미지가이드.md` → 이미지 제작 참고
- 이미지는 두 가지 방법으로 제작 가능:
  - **AI 생성**: ImageFX 프롬프트 복사/붙여넣기
  - **직접 제작**: 디자이너 가이드 참고하여 Canva, 피그마 등으로 제작
- 메타데이터는 네이버 블로그에서 직접 설정

## 설치 및 설정

### 1. Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정 (선택사항)

이미지를 실제로 생성하려면 Google Cloud 설정이 필요합니다.
텍스트 콘텐츠만 사용할 경우 이 단계는 건너뛰어도 됩니다.

`.env` 파일 생성:

```env
HOSPITAL_NAME=김포다조은병원
OUTPUT_DIR=./output

# 이미지 생성을 원하는 경우만 설정
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

자세한 Google Cloud 설정은 `GOOGLE_CLOUD_SETUP.md` 참고

## 사용 방법

### 기본 사용 (Claude Code 대화형)

Claude Code에서 다음과 같이 요청하세요:

```
"무릎 통증 치료" 주제로 블로그 글 작성해줘
```

Claude가 자동으로 다음 단계를 수행합니다:

1. **기획** (planner.md)
   - 키워드 분석
   - 아웃라인 생성 (6개 섹션)
   - `temp/outline.json` 저장

2. **리서치** (researcher.md)
   - 의료 정보 수집
   - `temp/research.json` 저장

3. **작성** (writer.md)
   - 본문 초안 마크다운 생성 (3000-3500자)
   - 이미지 placeholder 삽입
   - **네이버 SEO 최적화** (키워드 배치, 구조화)
   - **병원 홍보 강화** (검사/치료 안내 15-20%)
   - `temp/draft.md` 저장

4. **의료법 검토 및 최종 본문** (compliance_checker.md)
   - 전문적인 의료법 위반 검토
   - 자동 수정
   - **`output/[날짜]_[한글제목].md` 생성 (최종 본문) ⭐**

5. **이미지 가이드** (image_layout_designer.md)
   - outline 기반 이미지 계획 수립
   - 디자이너 가이드 + AI 프롬프트 작성
   - **`output/[날짜]_[한글제목]_이미지가이드.md` 생성 ⭐**

📋 **사용 방법**:
- `output/[날짜]_[한글제목].md` → 네이버 블로그 본문에 복사/붙여넣기
- `output/[날짜]_[한글제목]_이미지가이드.md` → 이미지 제작 참고

### 특정 단계만 실행

#### 특정 단계부터 재개
```
temp/outline.json부터 이어서 작성해줘
```

#### 의료법 재검토만
```
temp/draft.md를 의료법 기준으로 다시 검토해줘
```

### 네이버 블로그 사용 가이드

#### 1. 본문 복사/붙여넣기
- `output/[날짜]_[한글제목].md` 파일 열기
- 전체 내용 복사 (Ctrl+A → Ctrl+C)
- 네이버 블로그 "글쓰기" 모드에서 붙여넣기

#### 2. 이미지 제작/삽입

`output/[날짜]_[한글제목]_이미지가이드.md` 파일을 열어서 이미지를 제작합니다.
이미지 가이드는 **두 가지 형태**로 제공됩니다:

**옵션 1: AI 이미지 생성 (빠르고 간편)**
- 이미지 가이드의 "🤖 AI 이미지 생성 프롬프트" 섹션 참고
- 영어 프롬프트를 구글 ImageFX(imagefx.google)에 복사/붙여넣기
- 생성된 이미지 다운로드 후 한글 텍스트 추가 (Canva 등)
- 네이버 블로그 본문의 해당 위치에 이미지 삽입

**옵션 2: 디자이너가 직접 제작 (맞춤형)**
- 이미지 가이드의 "레이아웃 구성", "포함될 텍스트", "색상 가이드" 참고
- 디자인 툴(Canva, 피그마 등)로 처음부터 제작
- 네이버 블로그 본문의 해당 위치에 이미지 삽입

> 💡 **팁**: 시간이 부족하면 옵션 1 (AI 생성), 브랜딩이 중요하면 옵션 2 (직접 제작)

#### 3. 네이버 블로그 설정
- **카테고리**: 건강/의학
- **태그**: 본문의 핵심 키워드 5-7개
- **공개 설정**: 전체 공개
- **댓글/공감**: 허용

## 에이전트 가이드

각 에이전트의 역할과 상세 지침은 `agents/` 디렉토리의 `.md` 파일을 참조하세요.

### agents/planner.md
- **역할**: 키워드 → 블로그 아웃라인
- **출력**: `temp/outline.json`
- **핵심**: 독자 타겟팅, 톤앤매너 설정

### agents/researcher.md
- **역할**: 각 섹션별 의료 정보 수집
- **출력**: `temp/research.json`
- **핵심**: 의학적 정확성, 용어 정리

### agents/writer.md
- **역할**: 실제 블로그 본문 작성
- **출력**: `temp/draft.md`
- **핵심**: 독자 친화적, 의료법 준수 표현

### agents/compliance_checker.md ⭐
- **역할**: 의료법 위반 사항 검토 및 최종 본문 생성
- **출력**: `output/[날짜]_[한글제목].md`, `temp/compliance_report.json`
- **핵심**: 전문적인 의료법 검토, 허위과대 광고 방지

### agents/image_layout_designer.md ⭐
- **역할**: 이미지 가이드만 별도 파일로 생성
- **출력**: `output/[날짜]_[한글제목]_이미지가이드.md`
- **핵심**: 디자이너 가이드 + AI 프롬프트, 본문 제외

## 의료법 준수 가이드

### 절대 금지 표현
- ❌ 완치, 100% 치료, 확실한 효과
- ❌ 최고, 최상, 1등, 명의
- ❌ 단번에, 즉시, 획기적인
- ❌ 타 병원보다 우수
- ❌ 할인, 이벤트, 사은품

### 권장 표현
- ✅ 증상 개선에 도움을 드립니다
- ✅ 개인차가 있을 수 있습니다
- ✅ 전문의와 상담이 필요합니다
- ✅ 적절한 치료를 통해 기대할 수 있습니다

자세한 내용은 `agents/compliance_checker.md` 참조

## Context7 MCP 활용

Context7 MCP가 설치되어 있다면, Claude가 자동으로 다음 정보를 활용합니다:

- 병원 전문 진료과
- 병원 톤앤매너
- 의료 용어 사전
- 피해야 할 표현
- 기존 블로그 스타일

## 트러블슈팅

### Imagen API 연결 실패

```
✗ Imagen API 연결 실패: Could not find application default credentials
```

**해결 방법**:
1. `.env` 파일 확인
2. `GOOGLE_APPLICATION_CREDENTIALS` 경로 확인
3. 서비스 계정 키 파일 존재 확인
4. 프로젝트에서 Vertex AI API 활성화 확인

### 이미지 생성 실패

```
✗ 실패: Safety filter triggered
```

**해결 방법**:
- 프롬프트에서 민감한 표현 제거
- `imagen_prompt`를 더 중립적으로 수정
- `safety_filter_level` 조정

### Context7 MCP 연결 실패

**해결 방법**:
- Claude가 자동으로 기본 병원 정보로 fallback
- Context7 없이도 시스템 작동 가능

## 파일 구조 상세

### temp/ (중간 결과물)
작업 중 생성되는 파일들. 디버깅 및 재개에 유용합니다.

- `outline.json`: 블로그 구조 (1단계)
- `research.json`: 수집된 의료 정보 (2단계)
- `draft.md`: 본문 초안 (3단계)
- `compliance_report.json`: 의료법 검토 보고서 (4단계)

### output/ (최종 결과물) ⭐
완성된 블로그 글. 네이버 블로그에 바로 사용 가능합니다.

- `[날짜]_[한글제목].md`: 최종 본문 (예: 20260121_고혈압겨울철관리.md)
- `[날짜]_[한글제목]_이미지가이드.md`: 이미지 제작 가이드

### blog_generator/ (현재 미사용)
⚠️ **향후 자동 이미지 생성 기능용**

- `generate_images.py`: Imagen API를 사용한 이미지 자동 생성 스크립트
- `imagen_client.py`: Google Imagen API 클라이언트
- 현재는 수동으로 이미지 가이드를 보고 제작하는 방식 사용

## 라이선스

This project is for internal use at 김포다조은병원.

## 문의

기술 문의: Claude Code를 통해 질문하세요
