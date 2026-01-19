# 블로그 자동 생성 시스템

김포다조은병원 의료 블로그 콘텐츠를 자동으로 생성하는 멀티 에이전트 시스템입니다.

## 특징

- ✅ **Claude Code 기반**: 텍스트 생성은 Claude가 직접 수행
- ✅ **의료법 준수**: 허위과대 광고 자동 검토 및 수정
- ✅ **이미지 자동 생성**: Imagen API로 관련 이미지 생성
- ✅ **Context7 통합**: 병원 정보와 의료 용어 일관성 유지
- ✅ **바이브코딩**: Claude와 대화하며 단계별 진행

## 시스템 구조

```
hospital_blog_team/
├── agents/                   # 에이전트 프롬프트 (Claude가 읽고 실행)
│   ├── planner.md           # 1. 키워드 → 아웃라인
│   ├── researcher.md        # 2. 의료 정보 리서치
│   ├── writer.md            # 3. 본문 작성
│   ├── compliance_checker.md # 4. 의료법 검토
│   ├── image_director.md    # 5. 이미지 계획
│   └── integrator.md        # 7. 최종 통합
│
├── blog_generator/          # Python 모듈 (이미지 생성만)
│   ├── imagen_client.py     # Imagen API 클라이언트
│   └── generate_images.py   # 6. 이미지 생성 스크립트
│
├── output/                  # 최종 결과물
│   ├── images/             # 생성된 이미지
│   └── *.md                # 블로그 마크다운 파일
│
└── temp/                   # 중간 결과물
    ├── outline.json        # 1단계 결과
    ├── research.json       # 2단계 결과
    ├── draft.md            # 3단계 결과
    ├── compliance_report.json  # 4단계 결과
    ├── draft_revised.md    # 4단계 수정본
    └── image_plan.json     # 5단계 결과
```

## 설치 및 설정

### 1. Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. Google Cloud 설정

#### 서비스 계정 생성
1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 프로젝트 선택 또는 생성
3. IAM > 서비스 계정 > 서비스 계정 만들기
4. 역할: `Vertex AI User` 권한 부여
5. 키 생성 (JSON 다운로드)

#### 환경변수 설정
`.env` 파일 생성:

```bash
cp .env.example .env
```

`.env` 파일 편집:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
HOSPITAL_NAME=김포다조은병원
OUTPUT_DIR=./output
```

### 3. Imagen API 활성화

```bash
# Google Cloud CLI 설치 후
gcloud services enable aiplatform.googleapis.com
```

### 4. 연결 테스트

```bash
python blog_generator/imagen_client.py
```

정상 출력:
```
✓ Imagen API 연결 성공
  프로젝트: your-project-id
  리전: us-central1
```

## 사용 방법

### 기본 사용 (Claude Code 대화형)

Claude Code에서 다음과 같이 요청하세요:

```
"무릎 통증 치료" 주제로 블로그 글 작성해줘
```

Claude가 자동으로 다음 단계를 수행합니다:

1. **기획** (planner.md)
   - 키워드 분석
   - 아웃라인 생성
   - `temp/outline.json` 저장

2. **리서치** (researcher.md)
   - 의료 정보 수집
   - Context7에서 용어 확인
   - `temp/research.json` 저장

3. **작성** (writer.md)
   - 본문 마크다운 생성
   - `temp/draft.md` 저장

4. **의료법 검토** (compliance_checker.md)
   - 허위과대 광고 검사
   - 자동 수정
   - `temp/compliance_report.json` + `temp/draft_revised.md` 저장

5. **이미지 기획** (image_director.md)
   - 필요한 이미지 목록 생성
   - Imagen 프롬프트 작성
   - `temp/image_plan.json` 저장

6. **이미지 생성** (Python 스크립트)
   ```bash
   python blog_generator/generate_images.py
   ```
   - `output/images/*.png` 생성

7. **최종 통합** (integrator.md)
   - 본문 + 이미지 통합
   - `output/김포다조은병원_무릎통증치료_YYYYMMDD.md` 생성

### 특정 단계만 실행

#### 이미지 없이 텍스트만
```
"허리 디스크" 주제로 블로그 글 작성해줘 (이미지 제외)
```

#### 특정 단계부터 재개
```
temp/outline.json부터 이어서 작성해줘
```

#### 의료법 재검토만
```
temp/draft.md를 의료법 기준으로 다시 검토해줘
```

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
- **역할**: 의료법 위반 사항 검토 및 수정
- **출력**: `temp/compliance_report.json`, `temp/draft_revised.md`
- **핵심**: 허위과대 광고 방지

### agents/image_director.md
- **역할**: 이미지 계획 및 Imagen 프롬프트 생성
- **출력**: `temp/image_plan.json`
- **핵심**: 의료법 준수 이미지, 교육적 스타일

### agents/integrator.md
- **역할**: 본문 + 이미지 최종 통합
- **출력**: `output/*.md`
- **핵심**: 메타데이터, 이미지 경로, 최종 검토

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

- `outline.json`: 블로그 구조
- `research.json`: 수집된 의료 정보
- `draft.md`: 초안
- `compliance_report.json`: 의료법 검토 보고서
- `draft_revised.md`: 수정된 초안
- `image_plan.json`: 이미지 생성 계획
- `image_generation.log`: 이미지 생성 로그

### output/ (최종 결과물)
완성된 블로그 글과 이미지

- `images/*.png`: 생성된 이미지
- `*.md`: 최종 블로그 마크다운 파일

## 라이선스

This project is for internal use at 김포다조은병원.

## 문의

기술 문의: Claude Code를 통해 질문하세요
