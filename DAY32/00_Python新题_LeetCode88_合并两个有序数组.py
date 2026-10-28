# DAY32：独立完成88的原地合并，自己写三步、实现与测试；要求见同目录课程。

class Solution:
    def merge(self, nums1, m, nums2, n):
        result = [0] * (m+n)
        write = 0

        left_1 = 0
        left_2 = 0


        while write<(m+n):
            if left_1<m:
                if nums1[left_1] > nums2[left_2]:
                    result[write] = nums2[left_2]
                    left_2 += 1
                else:
                    result[write] = nums1[left_1]
                    left_1 += 1
                
                write += 1
            else:
                result[write] = nums2[left_2]
                left_2 += 1
                write += 1

        return result

solution = Solution()
nums1 = [1,2,3,0,0,0]
m = 3
nums2 = [2,5,6]
n = 3
print(solution.merge(nums1, m, nums2, n))

nums1 = [1]
m = 1
nums2 = []
n = 0
print(solution.merge(nums1, m, nums2, n))

nums1 = [0]
m = 0
nums2 = [1]
n = 1
print(solution.merge(nums1, m, nums2, n))


nums1 = [2,4,0,0]
m = 2
nums2 = [1,3]
n = 2
print(solution.merge(nums1, m, nums2, n))

