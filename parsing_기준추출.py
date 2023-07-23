import re
import pprint

# 기준 정보 파일을 읽습니다.
with open("st.md", "r", encoding="utf-8") as f:
    standard_lines = f.readlines()

# 통신 순서와 키워드를 저장할 리스트를 생성합니다.
communication_order = []
keywords = []

# 각 행을 파싱합니다.
for line in standard_lines:
    # 통신 코드, 참여자, 메세지 타입, CEID를 찾습니다.
    match = re.search(r"(cv|mc) ->> (cv|mc) : (S\d+F\d+)", line)
    if match:
        sender, receiver, code = match.groups()
        communication_order.append((sender, receiver, code))
        keywords.append(code)

        # S6F11 코드에 대해 CEID를 찾습니다.
        if code == "S6F11":
            ceid_match = re.search(r"CEID = (\d+)", line)
            if ceid_match:
                ceid = ceid_match.group(1)
                keywords.append("CEID = " + ceid)

# 통신 순서와 키워드를 출력합니다.
pprint.pprint("[communication_order]")
pprint.pprint(communication_order)
pprint.pprint("[Keywords]")
pprint.pprint(keywords)
