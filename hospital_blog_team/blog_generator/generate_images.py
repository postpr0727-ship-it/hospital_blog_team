#!/usr/bin/env python3
"""
Image Generation Script

temp/image_plan.json 파일을 읽어서 Imagen API로 이미지를 생성합니다.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from dotenv import load_dotenv
from imagen_client import ImagenClient


# 환경변수 로드
load_dotenv()


def load_image_plan(plan_path: str = "temp/image_plan.json") -> Dict[str, Any]:
    """이미지 계획 파일 로드"""
    try:
        with open(plan_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"✗ 오류: {plan_path} 파일을 찾을 수 없습니다.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ 오류: JSON 파싱 실패 - {e}")
        sys.exit(1)


def generate_images_from_plan(
    plan: Dict[str, Any],
    output_dir: str = "output/images",
    max_retries: int = 3
) -> List[Dict[str, Any]]:
    """
    이미지 계획에 따라 이미지 생성

    Args:
        plan: image_plan.json 내용
        output_dir: 이미지 저장 디렉토리
        max_retries: 최대 재시도 횟수

    Returns:
        생성 결과 목록
    """
    # 출력 디렉토리 생성
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Imagen 클라이언트 초기화
    try:
        client = ImagenClient()
    except Exception as e:
        print(f"✗ Imagen 클라이언트 초기화 실패: {e}")
        print("\n설정을 확인하세요:")
        print("  1. .env 파일에 GOOGLE_CLOUD_PROJECT 설정")
        print("  2. GOOGLE_APPLICATION_CREDENTIALS 환경변수 설정")
        print("  3. Google Cloud 서비스 계정 키 파일 경로 확인")
        sys.exit(1)

    images = plan.get("images", [])
    total = len(images)
    results = []

    print(f"\n{'='*60}")
    print(f"이미지 생성 시작: 총 {total}개")
    print(f"{'='*60}\n")

    for idx, image_info in enumerate(images, 1):
        image_id = image_info.get("id", idx)
        filename = image_info.get("filename", f"image_{idx}.png")
        prompt = image_info.get("imagen_prompt", "")
        description = image_info.get("description", "")
        priority = image_info.get("priority", "medium")

        print(f"[{idx}/{total}] {description}")
        print(f"  파일명: {filename}")
        print(f"  우선순위: {priority}")

        if not prompt:
            print(f"  ⚠️  프롬프트가 없어 건너뜁니다.")
            results.append({
                "id": image_id,
                "filename": filename,
                "success": False,
                "error": "프롬프트 없음"
            })
            continue

        output_path = os.path.join(output_dir, filename)

        # 이미지 생성 (재시도 로직 포함)
        result = client.generate_image_with_retry(
            prompt=prompt,
            output_path=output_path,
            max_retries=max_retries,
            aspect_ratio="16:9" if image_info.get("position") == "hero" else "4:3"
        )

        results.append({
            "id": image_id,
            "filename": filename,
            "description": description,
            "success": result["success"],
            "output_path": output_path if result["success"] else None,
            "error": result.get("error")
        })

        print()

    return results


def save_generation_log(
    results: List[Dict[str, Any]],
    plan: Dict[str, Any],
    log_path: str = "temp/image_generation.log"
):
    """생성 로그 저장"""
    success_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - success_count

    log_data = {
        "generated_at": datetime.now().isoformat(),
        "keyword": plan.get("keyword", ""),
        "total_images": len(results),
        "success_count": success_count,
        "fail_count": fail_count,
        "results": results
    }

    # 로그 파일 저장
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"이미지 생성 완료")
    print(f"{'='*60}")
    print(f"성공: {success_count}/{len(results)}")
    print(f"실패: {fail_count}/{len(results)}")

    if fail_count > 0:
        print(f"\n실패한 이미지:")
        for result in results:
            if not result["success"]:
                print(f"  - {result['filename']}: {result.get('error', 'Unknown error')}")

    print(f"\n로그 저장: {log_path}")


def main():
    """메인 함수"""
    # 명령줄 인자 처리
    plan_path = sys.argv[1] if len(sys.argv) > 1 else "temp/image_plan.json"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output/images"

    # 이미지 계획 로드
    plan = load_image_plan(plan_path)

    # 이미지 생성
    results = generate_images_from_plan(plan, output_dir)

    # 로그 저장
    save_generation_log(results, plan)

    # 실패가 있으면 종료 코드 1
    fail_count = sum(1 for r in results if not r["success"])
    sys.exit(1 if fail_count > 0 else 0)


if __name__ == "__main__":
    main()
