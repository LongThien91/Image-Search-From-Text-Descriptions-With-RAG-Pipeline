import os
import re
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
#from generate.gemini.reset_api import APIKeyManager
from langchain_core.output_parsers import StrOutputParser
from api_list_manager import APIKeyManager


class CheckQueryUserchat:
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

                - Truy vấn của người dùng có thể không đề cập đến toàn bộ mô tả sản phẩm (ví dụ chỉ nói về áo hoặc quần).
                - Hãy xác định **top {top_k}** mô tả phù hợp nhất với truy vấn, dựa trên mức độ tương đồng về **ý nghĩa** (loại quần áo, màu sắc, họa tiết, hình in, logo, v.v.).
                - Mỗi truy vấn chỉ cần khớp tốt với **một phần chính** trong mô tả (ví dụ: chỉ áo).
                - Không được chọn mô tả không liên quan hoặc sai loại đồ (ví dụ người dùng hỏi "áo" thì mô tả chỉ có "quần" là không phù hợp).
                - **Tuyệt đối chỉ trả về danh sách các `id`** như sau:  
                `["1", "3"]`  
                - **Không hỏi lại, không giải thích, không thêm nhận xét hoặc ký tự dư thừa.**

                ### Ví dụ:

                Truy vấn:  
                "áo màu đen có hình phi hành gia"  

                Danh sách mô tả:  
                (1) cái áo màu đen có hình phi hành gia in sau lưng, quần trắng bằng vải  
                (2) quần màu đen có hình gấu  
                (3) áo màu đen trước ngực có hình tàu vũ trụ  
                (4) mũ màu trắng, hình hải quân trong One Piece

                → Kết quả mong muốn (top_k = 2):  
                `["1", "3"]`
                    """
                ),
                (
                    "human",
                    f"""
                Truy vấn của người dùng: "{user_query}"  
                Danh sách mô tả sản phẩm:  
                {system_describe}

                Hãy xác định top {top_k} mô tả phù hợp nhất và **chỉ trả về danh sách id dưới dạng**:  
                `["id1", "id2", ...]`
                """
                            )
                        ]
                    )
        return prompt
    
    def isSimilar(self, user_query: str, system_describe: str,top_k:int):
        prompt = self.build_prompt_router(user_query, system_describe)
        model_gemini = ChatGoogleGenerativeAI(
            google_api_key=self.api_key.get_next_key(),
            model=self.model_gemini,
            max_tokens=1000,
            temperature=0
        )

        summary_chain = prompt | model_gemini | StrOutputParser()
        summary_result = summary_chain.invoke({"user_query": user_query, "system_describe": system_describe,"top_k":top_k})
        return summary_result.strip()