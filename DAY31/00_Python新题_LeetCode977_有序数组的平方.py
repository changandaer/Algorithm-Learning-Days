# DAY31：独立完成977，自己写三步、实现和测试；要求见同目录课程。
# 1.[-4,-1,0,3,10] -> [0,1,9,16,100]
#   [-12,-7,-3,2,3,11] -> [4,9,9,49,121,144]
# 2.由于数据有序，因此当前的平方最大值只能来自当前数组的端值
#   一个first下标保存最左端数值下标，一个last下标保存最右端数值下标
class Solution:
    def sortedSquares(self, nums):

        square = [0]*len(nums)
        square_last = len(nums) - 1
        first = 0
        last = len(nums) - 1
        for i in range(len(nums)):
            if square_last != 0:
                if abs(nums[first]) > abs(nums[last]):
                    square[square_last] = (nums[first])**2
                    first += 1
                    square_last -= 1
                elif abs(nums[first]) < abs(nums[last]):
                    square[square_last] = (nums[last])**2
                    last -= 1
                    square_last -= 1
                else:
                    square[square_last] = (nums[first])**2
                    square_last -= 1
                    first += 1
                    square[square_last] = (nums[last])**2
                    square_last -= 1
                    last -= 1
                    
            else:
                square[square_last] = (nums[first])**2
                
        return square

solution = Solution()
nums = [-4,-1,0,3,10]
square = solution.sortedSquares(nums)
print(square)

assert solution.sortedSquares([-7,-3,2,3,11]) == [4,9,9,49,121]
assert solution.sortedSquares([-3,-2,-1]) == [1,4,9]
assert solution.sortedSquares([-2,2]) == [4,4]
assert solution.sortedSquares([0]) == [0]
