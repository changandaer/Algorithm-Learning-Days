"""DAY27：独立完成LeetCode121，自己写三步分析、实现与测试；要求见当天课程。"""

# 1.输入输出：[8, 2, 6, 1, 5] -> 4
# 2.按照大小顺序排成字典，键为价格，值为索引号，只有后面索引号比当前索引号大才能相减计算利润，保存截止当前为止的最大利润
# 但是如何把价格按照大小顺序排成字典恐怕时间复杂度就不只是O(n)了，所以需要另寻他路，枚举所有买卖日期可能检查约n²对组合
# 除了最大利润需要保存，最低价格也需要保存

class Solution:

    # def maxProfit(self, prices):

    #     max_profit = 0

    #     for i in range(len(prices)):
    #         for j in range(i+1,len(prices)):
    #             profit = prices[j] - prices[i]
    #             if profit > max_profit:
    #                 max_profit = profit

    #     return max_profit

    # def maxProfit(self, prices):

    #     max_profit = 0
    #     i = 0
    #     low_price = prices[0]

    #     for index in range(len(prices)):

    #         if i<= len(prices) - 2:

    #             if prices[i] >= prices[i+1]:
    #                 i += 1
    #             else:
    #                 if low_price >= prices[i]:
    #                     low_price = prices[i]
    #                 profit = prices[i+1] - low_price
    #                 i += 1
    #                 if profit > max_profit:
    #                     max_profit = profit
        
    #     return max_profit
    
    def maxProfit(self, prices):

        max_profit = 0
        low_price = prices[0]

        for index in range(0,len(prices)-1):

            if prices[index+1] > prices[index]:
                if prices[index] < low_price:
                    low_price = prices[index]
                profit = prices[index+1] - low_price
                if profit > max_profit:
                    max_profit = profit
        
        return max_profit



solution = Solution()
assert solution.maxProfit([8, 2, 6, 1, 5]) == 4
assert solution.maxProfit([8, 2, 6, 7, 100]) == 98
assert solution.maxProfit([9, 7, 4]) == 0
assert solution.maxProfit([3]) == 0
assert solution.maxProfit([2, 2]) == 0
assert solution.maxProfit([3, 6, 1, 2]) == 3
assert solution.maxProfit([9, 7, 4]) == 0
assert solution.maxProfit([0, 4]) == 4
assert solution.maxProfit([2, 4, 1]) == 2

