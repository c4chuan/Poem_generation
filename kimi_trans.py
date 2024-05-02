from pathlib import Path
from openai import OpenAI
import time
import os


def get_break_point(save_path):
    paths = os.listdir(save_path)
    if not len(paths)==0:
        num = []
        for p in paths:
            num.append(int(p[:-4]))
        num = sorted(num)
        return num[-1]
    else:
        return 0



def get_response(file_path):
    client = OpenAI(
        api_key="sk-WM6vHdxlfnK4sqYZhhIIL28a1YYpFMXAMCg46CKY9TFOKfB4",
        base_url="https://api.moonshot.cn/v1",
    )


    # xlnet.pdf 是一个示例文件, 我们支持 pdf, doc 以及图片等格式, 对于图片和 pdf 文件，提供 ocr 相关能力
    file_object = client.files.create(file=Path(f"./诗词同义类聚词典/{pdf_id}.pdf"), purpose="file-extract")

    # 获取结果
    # file_content = client.files.retrieve_content(file_id=file_object.id)
    # 注意，之前 retrieve_content api 在最新版本标记了 warning, 可以用下面这行代替
    # 如果是旧版本，可以用 retrieve_content
    file_content = client.files.content(file_id=file_object.id).text

    # 把它放进请求中
    messages = [
        {
            "role": "system",
            "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
        },
        {
            "role": "system",
            "content": file_content,
        },
        {"role": "user", "content": '''请你提取出pdf中括号内的名词和对应的解释，并严格按照以下格式输出
        1.【<名词>】: <解释>
        2.【<名词>】: <解释>
        3.【<名词>】: <解释>
        4.【<名词>】: <解释>
        5.【<名词>】: <解释>
        ...以此类推'''},
    ]

    # 然后调用 chat-completion, 获取 Kimi 的回答
    completion = client.chat.completions.create(
        model="moonshot-v1-32k",
        messages=messages,
        temperature=0.3,
    )
    print(completion.choices[0].message)
    return completion.choices[0].message.content

save_path = './result'
if not os.path.isdir(save_path):
    os.mkdir(save_path)
paths = os.listdir('./诗词同义类聚词典')

st_point = get_break_point(save_path)
print(st_point)
for i in range(st_point,len(paths)):
    pdf_id = i+1
    path = f'./诗词同义类聚词典/{pdf_id}.pdf'
    sp_save_path = save_path+f'/{pdf_id}.txt'
    res = get_response(path)
    time.sleep(21)
    with open(sp_save_path,'w') as file:
        file.write(res)
        file.close()