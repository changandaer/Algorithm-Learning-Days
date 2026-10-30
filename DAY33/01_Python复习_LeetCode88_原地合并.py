# DAY33：修正88的耗尽判断与原地接口，自己写三步与测试；要求见同目录课程。
class Solution:
    def merge(self, nums1, m, nums2, n):
        first = m - 1
        second = n - 1
        write = m + n - 1

        while first >= 0:
            if second >= 0 and nums1[second] > nums2[first]:
                nums1[write] = nums1[second]
                second -= 1
            else:
                nums1[write] = nums2[first]
                first -= 1
            write -= 1

solver = Solution()
for initial, m, other, expected in [
    ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], [1, 2, 2, 3, 5, 6]),
    ([1], 1, [], [1]),
    ([0], 0, [1], [1]),
    ([2, 4, 0, 0], 2, [1, 3], [1, 2, 3, 4]),
    ([0, 0], 1, [-1], [-1, 0]),
    ([2, 2, 0, 0], 2, [2, 2], [2, 2, 2, 2]),
]:
    values = initial.copy()
    saved_other = other.copy()
    returned = solver.merge(values, m, other, len(other))
    assert returned is None
    assert values == expected
    assert other == saved_other