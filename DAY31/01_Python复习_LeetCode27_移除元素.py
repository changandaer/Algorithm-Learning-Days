# DAY31：闭卷复习27，使用整数返回接口；自己写三步与测试，要求见同目录课程。
# 1.[3,2,2,3]排除3→k2,[2,2,3,3]
#   [3,2,4,2,3]排除3→k2,[2,2,3,3]
# 2.auxiliary下标负责保留目标val的下标，query负责查询不同于val的值的下标

class Solution:
    def removeElement(self, nums, val):
        auxiliary = 0
        for query in range(len(nums)):
            if nums[query] == val:
                pass
            else:
                nums[auxiliary],nums[query] = nums[query],nums[auxiliary] 
                # 注意数组交换与赋值的区别
                auxiliary += 1
        return auxiliary,nums

solution = Solution()
nums = [3,2,4,2,3]
print(solution.removeElement(nums,3))
            
