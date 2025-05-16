import base64
import re
from typing import Optional
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from LLM.api_list_manager import APIKeyManager
import os
from dotenv import load_dotenv


class CheckImageDescriber:

    def __init__(self, api_key: APIKeyManager, model_gemini: str):
        self.api_key = api_key.get_next_key()
        self.model_gemini = model_gemini

    def _load_image_as_base64(self, image_path: str) -> str:
        """Load image and encode it to base64 for Gemini."""
        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"

    def build_image_description_prompt_for_clothes(self) -> list:
        instruction = {
            "type": "text",
            "text": (
                """
            Hãy mô tả hình ảnh này một cách ngắn gọn và chính xác, chỉ tập trung vào các đặc điểm liên quan đến **quần áo** xuất hiện trong ảnh, ngoài màu sắc chủ yếu của quần áo, không nói thêm màu sắc nào khác như màu logo, màu sắc của hình in,....

            Yêu cầu mô tả:
            - Loại quần áo (áo thun, áo khoác, váy, quần jean, v.v.).
            - Chất liệu (cotton, denim, vải nỉ, vải len, v.v.).
            - Màu sắc chính(tuyệt đối không miêu tả mơ hồ mà phải **chi tiết** )
            - Họa tiết hoặc hoa văn nổi bật (kẻ sọc, chấm bi, in hình, v.v.).
            - Có logo hoặc chữ không? Ghi rõ nội dung nếu thấy rõ.
            - Sau khi một đồ vật trong ảnh được miêu tả xong, đến đồ vật khác ***phải chia cách*** bằng kí tự ---

            Chỉ mô tả các yếu tố liên quan đến quần áo. Bỏ qua khung cảnh, người mẫu, hành động hoặc các vật thể không liên quan.
            Ví dụ: Áo thun tay ngắn, có màu đỏ và xanh lam, chia đôi theo chiều dọc. Có logo Nike ở ngực trái, có logo FC Barcelona --- quần bò đỏ sẫm, bằng da trơn
                   Áo khoác dày có hình 2 con chim cánh cụt sau lưng, màu chủ đạo là màu xanh lam, mũ có gắn lông, trước áo có logo teelab nhỏ  --- quần đùi màu xám, bằng vải, có logo chữ xbeo
            """
                    )
            }
        return [instruction]

    def describe_image(self, image_path: str) -> str:
        """Use Gemini to describe the image."""
        encoded_image = self._load_image_as_base64(image_path)
        messages = self.build_image_description_prompt_for_clothes()

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
