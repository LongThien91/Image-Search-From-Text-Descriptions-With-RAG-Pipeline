import base64
import re
from typing import Optional
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

class CheckImageDescriber:

    def __init__(self, api_key: str, model_gemini: str):
        self.api_key = api_key
        self.model_gemini = model_gemini

    def _load_image_as_base64(self, image_path: str) -> str:
        """Load image and encode it to base64 for Gemini."""
        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"

    def build_image_description_prompt(self) -> list:
        instruction = {
            "type": "text",
            "text": ("""
         Mô tả lại một cách chi tiết, rõ ràng và chính xác mọi yếu tố có trong ảnh.
            - Các vật thể chính và phụ trong ảnh (người, đồ vật, cảnh vật,...).
            - Hành động hoặc trạng thái của các đối tượng.
            - Bối cảnh không gian (trong nhà, ngoài trời, địa điểm, môi trường xung quanh, ...).
            - Màu sắc nổi bật, ánh sáng, và cảm xúc chung của ảnh.
            - Nếu có người: giới tính, độ tuổi ước lượng, trang phục, biểu cảm khuôn mặt, tư thế,...
            - Nếu có vật thể: ví dụ: quần áo, hãy miêu tả lại tên quần áo, loại quần áo, chất liệu, kiểu dáng, màu sắc, hoa văn, họa tiết, cách trưng bày, logo...
        ...
                """
            )
        }

        return [instruction]

    def describe_image(self, image_path: str) -> str:
        """Use Gemini to describe the image."""
        encoded_image = self._load_image_as_base64(image_path)
        messages = self.build_image_description_prompt()

        messages.append({
            "type": "image_url",
            "image_url": {
                "url": encoded_image
            }
        })

        model = ChatGoogleGenerativeAI(
            google_api_key=self.api_key,
            model=self.model_gemini,
            temperature=0.1,
            max_tokens=300,
        )

        response = model.invoke(
            [HumanMessage(content=messages)]
        )
        return response.content.strip()
