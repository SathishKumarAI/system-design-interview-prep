# 📘  [[Two Sum](https://leetcode.com/problems/two-sum/description/)](https://leetcode.com/problems/two-sum/description/) - Complete Technical Documentation

---

# 1️⃣ Overview

The **[Two Sum](https://leetcode.com/problems/two-sum/description/)** problem is a foundational algorithmic problem that evaluates:

* Search space reduction
* Hash-based lookup design
* Time–space tradeoff reasoning
* Optimization thinking

Although simple in appearance, it teaches a core engineering principle:

> Convert repeated search into indexed lookup.

---

# 2️⃣ Problem Statement

Given:

* An integer array `nums`
* An integer `target`

Return two **distinct indices** `[i, j]` such that:

$$
nums[i] + nums[j] = target
$$

---

## 📌 Constraints

* ( 2 \leq nums.length \leq 10^4 )
* ( -10^9 \leq nums[i] \leq 10^9 )
* ( -10^9 \leq target \leq 10^9 )
* Exactly one valid solution exists (LeetCode version)
* You may not reuse the same element twice

---

# 3️⃣ Mathematical Formulation

Let:

$$
A = {a_0, a_1, a_2, \dots, a_{n-1}}
$$

We must determine:

$$
\exists ; i \neq j \quad \text{such that} \quad a_i + a_j = T
$$

Rewriting:

$$
a_j = T - a_i
$$

Define the **complement**:

$$
\text{complement} = T - a_i
$$

The problem becomes:

> Does the complement exist in the dataset?

This transformation reduces a pair-search problem into a lookup problem.

---

# 4️⃣ Solution Approaches

We implemented three progressively optimized approaches.

---

# 🔹 4.1 Brute Force Approach (`twoSum1`)

## 💡 Idea

Examine all possible unordered pairs.

## 🔍 Algorithm

For all:

$$
(i, j) \quad \text{where} \quad 0 \le i < j < n
$$

Check:

```python
if nums[i] + nums[j] == target
```

Return indices if match found.

---

## ⏱ Complexity

Time:

$$
O(n^2)
$$

Space:

$$
O(1)
$$

---

## ✅ Advantages

* Very simple
* Good for understanding problem space
* No extra memory

## ❌ Disadvantages

* Poor scalability
* Quadratic growth
* Inefficient for large inputs

---

# 🔹 4.2 Two-Pass HashMap Approach (`twoSum2`)

## 💡 Idea

Use a dictionary (hash map) to reduce search time.

---

## 🔍 How It Works

### Pass 1 - Build Index

Store:

$$
\text{value} \rightarrow \text{index}
$$

```python
hashmap[nums[i]] = i
```

---

### Pass 2 - Lookup Complement

For each element:

$$
\text{complement} = target - nums[j]
$$

Check:

* If complement exists in hashmap
* Ensure index is not reused

```python
if complement in hashmap and hashmap[complement] != j:
    return [j, hashmap[complement]]
```

---

## ⏱ Complexity

Time:

$$
O(n)
$$

Space:

$$
O(n)
$$

---

## ⚠️ Important Detail

If duplicates exist:

* First pass stores the **last index**
* Still valid because exactly one solution exists

However, this requires careful index comparison.

---

# 🔹 4.3 One-Pass HashMap Approach (`twoSum`) - Optimal

## 💡 Idea

Merge lookup and insertion into a single traversal.

---

## 🔍 How It Works

For each element:

1. Compute complement:

$$
\text{complement} = target - nums[i]
$$

2. Check if complement already exists
3. If yes → return indices
4. Otherwise → store current value

---

### Implementation Logic

```python
for i in range(len(nums)):
    complement = target - nums[i]

    if complement in hashmap:
        return [i, hashmap[complement]]

    hashmap[nums[i]] = i
```

---

## ⏱ Complexity

Time:

$$
O(n)
$$

Space:

$$
O(n)
$$

---

## 🧠 Why This Is the Best Approach

* Single traversal
* No redundant scanning
* Handles duplicates naturally
* Clean and readable
* Interview standard solution
* Streaming-friendly logic

---

# 5️⃣ Edge Cases

### 1️⃣ Duplicates

```python
nums = [3, 3], target = 6
```

One-pass solution:

* First 3 stored
* Second 3 finds complement immediately

---

### 2️⃣ Negative Numbers

```python
nums = [-1, -2, -3, -4], target = -5
```

Complement logic works universally.

---

### 3️⃣ No Solution (General Usage)

```python
nums = [1,2,3], target = 100
```

Return `[]`.

---

### 4️⃣ Multiple Solutions

Current implementation returns first valid pair.

---

# 6️⃣ Comparison Summary

| Approach         | Time Complexity | Space Complexity | Performance |
| ---------------- | --------------- | ---------------- | ----------- |
| Brute Force      | O(n²)           | O(1)             | Slow        |
| Two-Pass HashMap | O(n)            | O(n)             | Fast        |
| One-Pass HashMap | O(n)            | O(n)             | Fastest     |

---

# 7️⃣ Core Engineering Insight

[Two Sum](https://leetcode.com/problems/two-sum/description/) teaches:

$$
\textbf{Search → Transform → Index → Lookup}
$$

Instead of repeatedly searching the array:

* Pre-index values
* Convert pair problem into lookup problem
* Trade memory for speed

---

# 8️⃣ Real-World Applications

### 🔹 Fraud Detection

$$
txn_i + txn_j = suspicious_amount
$$

Hash-based matching enables fast detection.

---

### 🔹 Database Join Equivalent

```sql
SELECT A.id, B.id
FROM table A
JOIN table B
ON A.value + B.value = target;
```

Hash map simulates an indexed join.

---

### 🔹 Streaming Systems

Maintain dynamic hash structure:

* Insert as data arrives
* Check complement instantly

Used in:

* Event correlation
* Log monitoring
* Real-time anomaly detection

---

# 9️⃣ Key Learning Points

* Optimization often involves trading **space for time**
* Hashing provides constant-time lookup
* Complement transformation simplifies equations
* Start brute force → optimize progressively
* Clean naming (`complement`) improves clarity

---

# 🔟 Final Recommendation

For interviews and production:

> Always use the **One-Pass HashMap approach**

It is:

* Efficient
* Clean
* Scalable
* Industry-standard

---

# 🎯 Final Takeaway

[Two Sum](https://leetcode.com/problems/two-sum/description/) is not about addition.

It is about:

* Efficient lookup design
* Hash-based indexing
* Search space reduction
* Engineering-level optimization thinking

It forms the foundation for:

* 3Sum
* Subarray Sum problems
* Prefix sums
* Frequency maps
* Data indexing strategies

## Referenced by

- [Repo index](../../INDEX.md)
