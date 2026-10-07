"""DAY26字典综合复习：字符统计与第一个唯一字符；自己分析、实现并检查字典操作，接口见课程。"""

def analyze_text(s):

    statitics = {}

    for element in s:

        statitics[element] = statitics.get(element,0) + 1
    

    for key,value in statitics.items():

        length = len(statitics)

        i = 0
        while i<length:
            if value == 1:
                for index in range(len(s)):
                    if key == s[index]:
                        return statitics,key,index
            else:
                i += 1
    return statitics,-1
        

statitics = analyze_text('')
print(statitics)