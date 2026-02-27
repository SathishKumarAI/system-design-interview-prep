from typing import List, Dict, Tuple


class Solution:
    """
    Two Sum Implementations

    1) Brute Force        -> O(n^2) time, O(1) space
    2) Two-Pass HashMap   -> O(n) time,  O(n) space
    3) One-Pass HashMap   -> O(n) time,  O(n) space (Optimal)
    """

    # ------------------------------------------------------------
    # 1️⃣ Brute Force Approach
    # ------------------------------------------------------------
    def twoSum1(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)

        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]

        return []


    # ------------------------------------------------------------
    # 2️⃣ Two-Pass HashMap Approach
    # ------------------------------------------------------------
    def twoSum2(self, nums: List[int], target: int) -> List[int]:
        hashmap: Dict[int, int] = {}

        # First pass: Build value → index map
        for i in range(len(nums)):
            hashmap[nums[i]] = i

        # Second pass: Lookup complement
        for j in range(len(nums)):
            complement = target - nums[j]

            if complement in hashmap and hashmap[complement] != j:
                return [j, hashmap[complement]]

        return []


    # ------------------------------------------------------------
    # 3️⃣ One-Pass HashMap (Optimal)
    # ------------------------------------------------------------
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hashmap: Dict[int, int] = {}

        for i in range(len(nums)):
            complement = target - nums[i]

            if complement in hashmap:
                return [i, hashmap[complement]]

            hashmap[nums[i]] = i

        return []


# ------------------------------------------------------------
# 🔍 Simple Test Runner
# ------------------------------------------------------------
def run_tests() -> None:
    s = Solution()

    test_cases: List[Tuple[List[int], int]] = [
        ([2, 7, 11, 15], 9),
        ([3, 2, 4], 6),
        ([3, 3], 6),
        ([-1, -2, -3, -4, -5], -8),
        ([1, 2, 3], 100),  # No solution case
    ]

    for nums, target in test_cases:
        print("\n----------------------------------")
        print(f"Input: {nums}, Target: {target}")
        print("Brute Force:", s.twoSum1(nums, target))
        print("Two-Pass HashMap:", s.twoSum2(nums, target))
        print("One-Pass HashMap:", s.twoSum(nums, target))


if __name__ == "__main__":
    run_tests()