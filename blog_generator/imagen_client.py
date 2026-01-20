"""
Imagen API Client

Google Vertex AI Imagen API를 사용하여 이미지를 생성하는 클라이언트입니다.
"""

import os
import time
from typing import Optional, Dict, Any
from pathlib import Path

try:
    from google.cloud import aiplatform
    from vertexai.preview.vision_models import ImageGenerationModel
except ImportError:
    print("경고: google-cloud-aiplatform 패키지가 설치되지 않았습니다.")
    print("pip install google-cloud-aiplatform 를 실행하세요.")


class ImagenClient:
    """Imagen API 클라이언트"""

    def __init__(
        self,
        project_id: Optional[str] = None,
        location: str = "us-central1"
    ):
        """
        Imagen 클라이언트 초기화

        Args:
            project_id: Google Cloud 프로젝트 ID
            location: Imagen API 리전
        """
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = location

        if not self.project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT 환경변수를 설정하거나 "
                "project_id 파라미터를 제공해야 합니다."
            )

        # Vertex AI 초기화
        aiplatform.init(project=self.project_id, location=self.location)

        # Imagen 모델 로드
        self.model = ImageGenerationModel.from_pretrained("imagegeneration@005")

    def generate_image(
        self,
        prompt: str,
        output_path: str,
        number_of_images: int = 1,
        negative_prompt: Optional[str] = None,
        aspect_ratio: str = "1:1",
        safety_filter_level: str = "block_some",
        person_generation: str = "allow_adult"
    ) -> Dict[str, Any]:
        """
        이미지 생성

        Args:
            prompt: 이미지 생성 프롬프트
            output_path: 저장할 파일 경로
            number_of_images: 생성할 이미지 개수
            negative_prompt: 제외할 요소 (선택적)
            aspect_ratio: 종횡비 ("1:1", "9:16", "16:9", "4:3", "3:4")
            safety_filter_level: 안전 필터 레벨
            person_generation: 인물 생성 설정

        Returns:
            생성 결과 정보
        """
        try:
            print(f"이미지 생성 중: {prompt[:50]}...")

            # 이미지 생성
            images = self.model.generate_images(
                prompt=prompt,
                number_of_images=number_of_images,
                negative_prompt=negative_prompt,
                aspect_ratio=aspect_ratio,
                safety_filter_level=safety_filter_level,
                person_generation=person_generation
            )

            # 첫 번째 이미지 저장
            if images and len(images.images) > 0:
                output_dir = Path(output_path).parent
                output_dir.mkdir(parents=True, exist_ok=True)

                images.images[0].save(location=output_path)

                print(f"✓ 저장 완료: {output_path}")

                return {
                    "success": True,
                    "output_path": output_path,
                    "prompt": prompt
                }
            else:
                return {
                    "success": False,
                    "error": "이미지가 생성되지 않았습니다.",
                    "prompt": prompt
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "prompt": prompt
            }

    def generate_image_with_retry(
        self,
        prompt: str,
        output_path: str,
        max_retries: int = 3,
        retry_delay: int = 2,
        **kwargs
    ) -> Dict[str, Any]:
        """
        재시도 로직이 있는 이미지 생성

        Args:
            prompt: 이미지 생성 프롬프트
            output_path: 저장할 파일 경로
            max_retries: 최대 재시도 횟수
            retry_delay: 재시도 간격 (초)
            **kwargs: generate_image()의 추가 파라미터

        Returns:
            생성 결과 정보
        """
        for attempt in range(max_retries):
            result = self.generate_image(prompt, output_path, **kwargs)

            if result["success"]:
                return result

            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f"재시도 {attempt + 1}/{max_retries} - {wait_time}초 후 재시도...")
                time.sleep(wait_time)
            else:
                print(f"✗ 실패: {result.get('error', 'Unknown error')}")

        return result


def test_connection():
    """Imagen API 연결 테스트"""
    try:
        client = ImagenClient()
        print(f"✓ Imagen API 연결 성공")
        print(f"  프로젝트: {client.project_id}")
        print(f"  리전: {client.location}")
        return True
    except Exception as e:
        print(f"✗ Imagen API 연결 실패: {e}")
        return False


if __name__ == "__main__":
    # 연결 테스트
    test_connection()
