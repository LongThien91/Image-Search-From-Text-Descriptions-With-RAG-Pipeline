import os
import re
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from LLM.api_list_manager import APIKeyManager
from langchain_core.output_parsers import StrOutputParser


class CheckQuerySimilar:
    def __init__(self, api_key: APIKeyManager, model_gemini: str):
        self.api_key = api_key.get_next_key()
        self.model_gemini = model_gemini

    
    def build_prompt_router(self, user_query: str, system_describe: str, top_k: int) -> ChatPromptTemplate:
        prompt = ChatPromptTemplate.from_messages(
            [
            (
                "system",
                f"""
                Bạn là một trợ lý thông minh có nhiệm vụ **so khớp truy vấn người dùng với mô tả sản phẩm** trong cơ sở dữ liệu.  

                Các mô tả sản phẩm có định dạng:  
                (id) mô tả chi tiết từng bộ quần áo – ví dụ:  
                (1) áo màu đen in hình phi hành gia, quần màu trắng có logo teelab.  
                (2) áo khoác xanh dương có hình ngọn núi.  

                ### Yêu cầu:
                - Hãy xác định **top {top_k}** mô tả phù hợp nhất với truy vấn, dựa trên mức độ tương đồng về **ý nghĩa** (loại quần áo, màu sắc, họa tiết, hình in, logo, v.v.) .
                - Không nhất thiết phải trả về tất top {top_k} kết quả, nếu mô tả sản phẩm không phù hợp có thể trả về số lượng ít hơn.
                - Không được chọn mô tả không liên quan hoặc sai loại đồ (ví dụ người dùng hỏi "áo" thì mô tả chỉ có "quần" là không phù hợp).
                - **Tuyệt đối chỉ trả về danh sách các `id`** như sau:["0", "2"]
                -Sắp xếp theo thứ tự các số trả về phải có mức độ tương đồng giảm dần, chọn mô tả phù hợp nhất trước.
                - **Không hỏi lại, không giải thích, không thêm nhận xét hoặc thêm ký tự dư thừa.**

                ### Ví dụ:

                Truy vấn:  
                "áo màu đen có hình phi hành gia"  

                Danh sách mô tả:  
                (0) cái áo màu đen có hình phi hành gia in sau lưng
                (1) quần màu đen có hình gấu  
                (2) áo màu đen trước ngực có hình tàu vũ trụ  
                (3) Áo thun tay ngắn, chất liệu cotton, màu trắng. In hình gấu Lotso và chữ "LOTSO STORY" ở mặt trước. Có logo hình vương miện ở góc dưới bên phải.

                → Kết quả mong muốn (top_k = 2):  
                ["0", "2"]
                **Không được bao quanh bằng dấu ``` hay bất kỳ định dạng markdown/code block nào.**  
                **Chỉ in ra 1 dòng duy nhất là danh sách id.**
                    """
                ),
                (
                    "human",
                    f"""
                Truy vấn của người dùng: "{user_query}"  
                Danh sách mô tả sản phẩm:  
                {system_describe}

                Hãy xác định top {top_k} mô tả phù hợp nhất và **chỉ trả về danh sách id dưới dạng**:  
                ["id1", "id2", ...]
                """
                            )
                        ]
                    )
        return prompt
    
    def isSimilar(self, user_query: str, system_describe: str,top_k:int):
        prompt = self.build_prompt_router(user_query, system_describe,top_k)
        model_gemini = ChatGoogleGenerativeAI(
            google_api_key=self.api_key,
            model=self.model_gemini,
            max_tokens=1000,
            temperature=0
        )

        summary_chain = prompt | model_gemini | StrOutputParser()
        summary_result = summary_chain.invoke({"user_query": user_query, "system_describe": system_describe,"top_k":top_k})
        return summary_result.strip()