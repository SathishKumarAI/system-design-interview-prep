# 📘 [Two Sum](https://leetcode.com/problems/two-sum/description/) – Complete Technical Documentation (Student-Friendly Edition)

---

# 1️⃣ Overview

The **[Two Sum](https://leetcode.com/problems/two-sum/description/)** problem looks very simple:

> Find two numbers in an array that add up to a target.

But behind this simple question, it teaches very important ideas in programming:

* How to reduce unnecessary work
* How to think smarter instead of harder
* How to trade memory for speed
* How to optimize performance

Even though this is labeled as “Easy”, it builds the foundation for many advanced problems.

---

# 2️⃣ Problem Statement (Simple Explanation)

You are given:

* A list of numbers → `nums`
* A number → `target`

You need to find:

Two **different positions (indices)** in the list such that:

$$
nums[i] + nums[j] = target
$$

Important rules:

* You cannot use the same number twice.
* There is exactly one correct answer (in LeetCode version).

---

## 🧠 Simple Example

```
nums = [2, 7, 11, 15]
target = 9
```

We check:

2 + 7 = 9 ✅

So answer is:

```
[0, 1]
```

Because index 0 and 1 add up to 9.

---

# 3️⃣ Mathematical Understanding (But Simple)

Let’s say:

$$
A = {a_0, a_1, a_2, ..., a_{n-1}}
$$

We want to find:

$$
a_i + a_j = T
$$

Now here comes the smart thinking:

If we know one number:

$$
a_i
$$

Then the other number must be:

$$
a_j = T - a_i
$$

We call:

$$
\text{complement} = T - a_i
$$

So now the problem becomes:

> Instead of finding two numbers, can we find the complement of each number?

This makes the problem much easier.

---

# 4️⃣ Solution Approaches

We move from basic thinking to smarter thinking.

---

# 🔹 4.1 Brute Force Approach (`twoSum1`)

## 💡 Simple Thinking

Try every possible pair.

Like checking:

* First with second
* First with third
* First with fourth
* Second with third
* Second with fourth
* And so on...

---

## 🔍 Code Idea

```python
for i in range(n):
    for j in range(i+1, n):
        if nums[i] + nums[j] == target:
            return [i, j]
```

---

## ⏱ Complexity (In Simple Words)

If there are 10 numbers → small work
If there are 10,000 numbers → HUGE work

Time complexity:

$$
O(n^2)
$$

This means:

If n doubles → work becomes 4x.

---

## ❌ Why It’s Not Good for Large Data

Because:

* It checks too many combinations.
* It repeats work again and again.

It works.
But it’s not smart.

---

# 🔹 4.2 Two-Pass HashMap Approach (`twoSum2`)

Now we think smarter.

---

## 💡 Big Idea

Instead of searching the whole array every time:

Let’s store numbers in a dictionary.

Think of dictionary like:

📖 A phone book
You can instantly look up someone’s number.

---

## 🧠 What We Do

### Pass 1 – Store All Numbers

Store:

```
value → index
```

Example:

```
2 → 0
7 → 1
11 → 2
15 → 3
```

---

### Pass 2 – Look for Complement

For each number:

```
complement = target - nums[j]
```

Then check:

```
if complement exists in hashmap:
    return indices
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

This is MUCH better than O(n²).

---

## ⚠️ Important Concept

We use extra memory to make it faster.

This is called:

> Time-Space Tradeoff

We use more memory
→ To reduce time.

---

# 🔹 4.3 One-Pass HashMap Approach (`twoSum`) – BEST

Now we improve even more.

---

## 💡 Even Smarter Idea

Instead of:

* First storing everything
* Then searching

We do both at the same time.

---

## 🔍 How It Works (Step by Step)

For each number:

1. Calculate complement:

   ```
   complement = target - nums[i]
   ```

2. Check:

   ```
   if complement already seen:
       return answer
   ```

3. Otherwise store current number.

---

## 🧠 Example Walkthrough

```
nums = [2, 7, 11, 15]
target = 9
```

Step 1:

* i = 0 → number = 2
* complement = 7
* 7 not seen
* store 2

Step 2:

* i = 1 → number = 7
* complement = 2
* 2 already seen ✅
* return answer

We stop early. Very efficient.

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

## ✅ Why This Is Best

* Only one loop
* Stops early when answer found
* Clean logic
* Interview standard solution
* Works for duplicates

---

# 5️⃣ Edge Cases (Important for Students)

---

## 1️⃣ Duplicates

```
nums = [3,3]
target = 6
```

First 3 stored
Second 3 finds complement immediately.

---

## 2️⃣ Negative Numbers

```
nums = [-1, -2, -3, -4]
target = -5
```

Complement logic still works.

Math works the same for negatives.

---

## 3️⃣ No Solution

```
nums = [1,2,3]
target = 100
```

Return empty list `[]`.

---

# 6️⃣ Comparison Summary (Easy Table)

| Approach         | Time  | Space | Simple Meaning |
| ---------------- | ----- | ----- | -------------- |
| Brute Force      | O(n²) | O(1)  | Slow           |
| Two-Pass HashMap | O(n)  | O(n)  | Fast           |
| One-Pass HashMap | O(n)  | O(n)  | Fastest        |

---

# 7️⃣ Core Learning (Very Important)

This problem teaches:

### Instead of:

Search again and again.

### Do this:

Store once → lookup instantly.

This idea is used everywhere in programming:

* Databases
* Caching
* Search engines
* Fraud detection
* Log systems

---

# 8️⃣ Real-Life Analogy

Imagine:

You’re at a grocery store.
You need two items that cost $10 total.

### Brute force way:

Pick every pair and check total price.

### Smart way:

For each item:
Ask yourself:

> If this costs $3, I need $7 more.
> Is there an item costing $7?

That’s exactly what we’re doing.

---

# 9️⃣ Why Interviewers Love This Question

Because it tests:

* Can you start simple?
* Can you optimize?
* Do you understand hash maps?
* Do you know time complexity?
* Can you think logically?

It separates:

Basic coders
From
Algorithm thinkers

---

# 🔟 Final Recommendation

Always use:

> One-Pass HashMap approach

Because it is:

* Efficient
* Clean
* Scalable
* Industry-standard

---

# 🎯 Final Big Takeaway

[Two Sum](https://leetcode.com/problems/two-sum/description/) is NOT about addition.

It is about:

* Thinking smarter
* Reducing repeated work
* Using data structures effectively
* Designing efficient solutions

## Referenced by

- [Repo index](../../INDEX.md)
