"""DAY14任务4：可选。学完异常处理后，再独立实现读取成功与文件缺失的不同结果。"""

def try_read_text(file_path):

    try:
        with open(file_path,"r",encoding='utf-8') as file:
            
            content = file.read()

            return {"ok": True, "text": content}

    except FileNotFoundError:

        return {"ok": False, "error": "找不到文件"}

read_text_A = try_read_text("DAY14/岗位样例A_三条岗位.txt")
read_text_C = try_read_text("DAY14/岗位样例C_仅空白行.txt")
read_text_D = try_read_text("DAY14/岗位样例D_不存在.txt")

print(read_text_A)
print(read_text_C)
print(read_text_D)