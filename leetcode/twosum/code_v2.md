Good 👌 - now we move from “standard interview solution” to **alternative thinking**.

Here are **completely different implementations** of [Two Sum](https://leetcode.com/problems/two-sum/description/) that do NOT use the typical one-pass hashmap pattern.

---

# 🔹 1️⃣ Two Pointer (Sorted + Preserve Index)

This version:

* Sorts while preserving original indices
* Uses two pointers
* No hash map

### Idea

1. Pair each number with its index.
2. Sort by value.
3. Use left + right pointers.

---

```python
from typing import List

class SolutionTwoPointer:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Pair values with original indices
        indexed_nums = list(enumerate(nums))

        # Sort by value
        indexed_nums.sort(key=lambda x: x[1])

        left = 0
        right = len(nums) - 1

        while left < right:
            current_sum = indexed_nums[left][1] + indexed_nums[right][1]

            if current_sum == target:
                return [indexed_nums[left][0], indexed_nums[right][0]]
            elif current_sum < target:
                left += 1
            else:
                right -= 1

        return []
```

### Complexity

Time:
[
O(n \log n)
]

Space:
[
O(n)
]

---

# 🔹 2️⃣ Using Binary Search (After Sorting)

Instead of two pointers:

* Sort with indices
* For each element, binary search for complement

---

```python
import bisect
from typing import List

class SolutionBinarySearch:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        indexed_nums = list(enumerate(nums))
        indexed_nums.sort(key=lambda x: x[1])

        values = [num for _, num in indexed_nums]

        for i in range(len(values)):
            complement = target - values[i]

            j = bisect.bisect_left(values, complement, i + 1)

            if j < len(values) and values[j] == complement:
                return [indexed_nums[i][0], indexed_nums[j][0]]

        return []
```

### Complexity

Time:
[
O(n \log n)
]

---

# 🔹 3️⃣ Using Combinations (Functional Style)

Very different style.

Uses Python’s itertools.

---

```python
from typing import List
from itertools import combinations

class SolutionCombinations:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for (i, a), (j, b) in combinations(enumerate(nums), 2):
            if a + b == target:
                return [i, j]
        return []
```

This is brute force but written differently.

---

# 🔹 4️⃣ Using DefaultDict of Lists (Handles Duplicates Differently)

Instead of storing one index per value,
store ALL indices.

---

```python
from typing import List
from collections import defaultdict

class SolutionMultiIndex:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        value_map = defaultdict(list)

        for i, num in enumerate(nums):
            value_map[num].append(i)

        for i, num in enumerate(nums):
            complement = target - num

            if complement in value_map:
                for idx in value_map[complement]:
                    if idx != i:
                        return [i, idx]

        return []
```

---

# 🔹 5️⃣ Using Set Tracking (Less Conventional)

Track seen values but compute indices later.

---

```python
from typing import List

class SolutionSetBased:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = set()

        for num in nums:
            complement = target - num
            if complement in seen:
                # retrieve indices
                return [nums.index(complement), nums.index(num, nums.index(complement)+1)]
            seen.add(num)

        return []
```

⚠️ Not ideal (index lookup is O(n)), but conceptually different.

---

# 🧠 Why This Is Important

When interviewers say:

> “Can you solve it another way?”

They are testing:

* Flexibility
* Pattern recognition
* Understanding constraints

Not memorization.

---

# 🚀 Engineering Insight

There are multiple dimensions to this problem:

| Approach      | Time       | Space | Uses Sorting? | Uses Hashing? |
| ------------- | ---------- | ----- | ------------- | ------------- |
| Brute Force   | O(n²)      | O(1)  | ❌             | ❌             |
| HashMap       | O(n)       | O(n)  | ❌             | ✅             |
| Two Pointer   | O(n log n) | O(n)  | ✅             | ❌             |
| Binary Search | O(n log n) | O(n)  | ✅             | ❌             |

Each exists for a reason.

## Referenced by

- [Repo index](../../INDEX.md)
