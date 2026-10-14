"""DAY28：先不看昨日示范，闭卷完成121并解释自己的正确性与复杂度。"""
# [8, 2, 6, 1, 5] -> 4

class Solution:
    
    def maxProfit(self, prices):
        low_price = prices[0]
        maxprofit = 0

        for i in range(1,len(prices)):
            if low_price > prices[i-1]:
                low_price = prices[i-1]
            profit = prices[i] - low_price
            if profit > maxprofit:
                maxprofit = profit
        if maxprofit>0:
            return maxprofit
        else:
            return 0

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
assert solution.maxProfit([3,2,6,5,0,3]) == 4
            