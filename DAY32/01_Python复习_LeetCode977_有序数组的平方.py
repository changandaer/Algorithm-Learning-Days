# DAY32：修正977的循环推进并闭卷复写，自己写三步和测试；要求见同目录课程。
# 1.[-4,-1,0,3,10] -> [0,1,9,16,100]
#   [-12,-7,-3,2,3,11] -> [4,9,9,49,121,144]
# 2.由于数据有序，因此当前的平方最大值只能来自当前数组的端值
#   一个first下标保存最左端数值下标，一个last下标保存最右端数值下标

class Solution:
    def sortedSquares(self, nums):

        result = [0] * len(nums)
        write = len(nums) - 1

        left = 0
        right = len(nums) - 1

        while left<=right:
            if abs(nums[left]) > abs(nums[right]):
                result[write] = (abs(nums[left]))**2
                left += 1
            else:
                result[write] = (abs(nums[right]))**2
                right -= 1
            write -= 1
        
        return result

solution = Solution()
for original,expected in [
    ([-4, -1, 0, 3, 10], [0, 1, 9, 16, 100]),
    ([-2, -1, -1], [1, 1, 4]),
    ([-2, -1, 1, 2], [1, 1, 4, 4]),
    ([-2, 2], [4, 4]),
    ([-3, -2, -1], [1, 4, 9]),
    ([0], [0]),
]:
    value = original.copy()
    print(value)
    result = solution.sortedSquares(value)
    assert result == expected