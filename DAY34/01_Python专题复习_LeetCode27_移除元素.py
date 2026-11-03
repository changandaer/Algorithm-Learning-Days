# DAY34：独立复习27，用读写双指针组织三步、实现与测试；要求见同目录课程。
# 双指针：
#       读位置：当前检索的元素的位置
#       写位置：下一个符合条件的结果要放的位置
#       每检查一个元素，读位置向前推，只有确实保留了一个满足条件的元素，写位置才向前推

# [4,1,4,2,1]排除4→k3，读位置一直向前推，等于4交换之后写位置才向前推

class Solution:
    def removeElement(self, nums, val):
        write = 0
        for read in range(len(nums)):
            if nums[read] != val:
                nums[write],nums[read] = nums[read],nums[write]
                write += 1
        return write

solution = Solution()
for nums,val,expected in [
                            ([4,1,4,2,1],4,3),
                            ([2,2],2,0),
                            ([],0,0),
                            ([1,1,3],2,3)
]:
    nums_copy = nums.copy()
    assert nums == nums_copy
    result = solution.removeElement(nums_copy,val)
    print(nums_copy,val,result)
    assert result == expected
