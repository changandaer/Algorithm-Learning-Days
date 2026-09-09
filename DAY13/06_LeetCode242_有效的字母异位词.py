"""DAY13任务6：LeetCode 242。要求见课程文档；请从空白完成三步分析、实现和测试。"""

# 1.输入输出："anagram" 与 "nagaram" → True

# 2.阶段：先判断字符串长度

class Solution:

    def is_anagram(self,s, t):

        word_s = {}
        word_t = {}
        len_letter = 0

        if len(s) == len(t):

            for letter_s in s:
                word_s[letter_s] = word_s.get(letter_s,0) + 1
            for letter_t in t:
                word_t[letter_t] = word_t.get(letter_t,0) + 1
            
            if word_s == word_t:
                return True
            
            # 在 Python 中，当使用 == 来比较两个字典时，Python 底层会自动做以下三步检查：

            # 1.查键的数量：两个字典的键（Key）的数量是不是一样多？
            # 2.查键的种类：字典 A 里的所有键，是不是都在字典 B 里？
            # 3.查键对应的值：对于每一个相同的键，它们对应的值（Value）是不是一模一样？

            # 只要这三点全部满足，Python 就会认为这两个字典完全相等，返回 True。字典里的键值对是按什么顺序塞进去的，完全不影响对比结果。

            # 为什么会这样设计？因为在数据结构的概念里，字典（哈希表）是没有“顺序”这个概念的，它就像一个有很多抽屉的储物柜。
            # 把苹果放在左边的抽屉，香蕉放在右边；和先把香蕉放在左边，苹果放在右边，对于“你拥有什么水果”这个本质结果来说是一样的。

            # 列表（List）看重顺序：[1, 2, 3] == [3, 2, 1] 结果是 False。
            # 字典（Dict）只看重映射关系：{'a': 1, 'b': 2} == {'b': 2, 'a': 1} 结果是 True。

                    
        return False

solution = Solution()

word = solution.is_anagram("anagram","nagaram")

print(word)

assert solution.is_anagram("rat","car") == False
assert solution.is_anagram("aab","abb") == False
assert solution.is_anagram('','') == True