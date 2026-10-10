import sqlite3
import os
from database import DB_PATH

def expand_dsa():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    additional_problems = [
        # Stack & Queue
        (
            "Stack & Queue",
            "Valid Parentheses",
            "Easy",
            "https://leetcode.com/problems/valid-parentheses/",
            "https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/",
            "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
            "Use a stack. Push opening brackets. When a closing bracket arrives, verify it matches the bracket popped from the top of the stack.",
            "O(N)",
            "O(N)",
            """def isValid(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    return not stack""",
            """#include <string>
#include <stack>
#include <unordered_map>
using namespace std;

bool isValid(string s) {
    stack<char> st;
    unordered_map<char, char> mp = {{')', '('}, {'}', '{'}, {']', '['}};
    for (char c : s) {
        if (mp.count(c)) {
            if (st.empty() || st.top() != mp[c]) return false;
            st.pop();
        } else {
            st.push(c);
        }
    }
    return st.empty();
}""",
            15
        ),
        (
            "Stack & Queue",
            "Daily Temperatures",
            "Medium",
            "https://leetcode.com/problems/daily-temperatures/",
            "https://www.geeksforgeeks.org/find-number-days-warmer-temperature-given-array/",
            "Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature.",
            "Monotonic Decreasing Stack: Maintain indices in a stack where temperatures are in descending order. When current temperature is higher than stack top, pop and calculate distance.",
            "O(N)",
            "O(N)",
            """def dailyTemperatures(temperatures: list[int]) -> list[int]:
    res = [0] * len(temperatures)
    stack = []  # stores index
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            prev_i = stack.pop()
            res[prev_i] = i - prev_i
        stack.append(i)
    return res""",
            """#include <vector>
#include <stack>
using namespace std;

vector<int> dailyTemperatures(vector<int>& temperatures) {
    int n = temperatures.size();
    vector<int> res(n, 0);
    stack<int> st;
    for (int i = 0; i < n; i++) {
        while (!st.empty() && temperatures[st.top()] < temperatures[i]) {
            int prev = st.top();
            st.pop();
            res[prev] = i - prev;
        }
        st.push(i);
    }
    return res;
}""",
            16
        ),
        (
            "Stack & Queue",
            "Min Stack",
            "Medium",
            "https://leetcode.com/problems/min-stack/",
            "https://www.geeksforgeeks.org/design-and-implement-special-stack-data-structure/",
            "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time O(1).",
            "Store pairs in stack: (value, current_min) or maintain a parallel min_stack that tracks running minimums.",
            "O(1) all operations",
            "O(N)",
            """class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]""",
            """#include <stack>
#include <algorithm>
using namespace std;

class MinStack {
    stack<int> st;
    stack<int> minSt;
public:
    MinStack() {}
    void push(int val) {
        st.push(val);
        if (minSt.empty() || val <= minSt.top()) minSt.push(val);
    }
    void pop() {
        if (st.top() == minSt.top()) minSt.pop();
        st.pop();
    }
    int top() { return st.top(); }
    int getMin() { return minSt.top(); }
};""",
            17
        ),

        # Binary Search
        (
            "Binary Search",
            "Koko Eating Bananas",
            "Medium",
            "https://leetcode.com/problems/koko-eating-bananas/",
            "https://www.geeksforgeeks.org/koko-eating-bananas/",
            "Koko loves to eat bananas. Given piles and h hours, return the minimum integer eating speed k such that she can eat all bananas within h hours.",
            "Binary Search on Answer: Search space for speed k is [1, max(piles)]. For each mid speed, check if total ceil(pile/k) hours <= h. If yes, try smaller speed (r = mid); else increase speed (l = mid + 1).",
            "O(N * log(max(piles)))",
            "O(1)",
            """import math

def minEatingSpeed(piles: list[int], h: int) -> int:
    l, r = 1, max(piles)
    while l < r:
        mid = (l + r) // 2
        hours = sum(math.ceil(p / mid) for p in piles)
        if hours <= h:
            r = mid
        else:
            l = mid + 1
    return l""",
            """#include <vector>
#include <algorithm>
#include <cmath>
using namespace std;

int minEatingSpeed(vector<int>& piles, int h) {
    int l = 1, r = *max_element(piles.begin(), piles.end());
    while (l < r) {
        int mid = l + (r - l) / 2;
        long long hours = 0;
        for (int p : piles) hours += (p + mid - 1) / mid;
        if (hours <= h) r = mid;
        else l = mid + 1;
    }
    return l;
}""",
            18
        ),

        # Trees & BST
        (
            "Trees & Graphs",
            "Binary Tree Level Order Traversal",
            "Medium",
            "https://leetcode.com/problems/binary-tree-level-order-traversal/",
            "https://www.geeksforgeeks.org/level-order-tree-traversal/",
            "Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).",
            "BFS with Queue: Use a double-ended queue. At each level, determine queue size, pop all nodes belonging to that level, add their values to a level list, and push child nodes.",
            "O(N)",
            "O(N)",
            """from collections import deque

def levelOrder(root) -> list[list[int]]:
    if not root: return []
    res = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level)
    return res""",
            """#include <vector>
#include <queue>
using namespace std;

vector<vector<int>> levelOrder(TreeNode* root) {
    if (!root) return {};
    vector<vector<int>> res;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        int sz = q.size();
        vector<int> level;
        for (int i = 0; i < sz; i++) {
            TreeNode* cur = q.front(); q.pop();
            level.push_back(cur->val);
            if (cur->left) q.push(cur->left);
            if (cur->right) q.push(cur->right);
        }
        res.push_back(level);
    }
    return res;
}""",
            19
        ),
        (
            "Trees & Graphs",
            "Validate Binary Search Tree",
            "Medium",
            "https://leetcode.com/problems/validate-binary-search-tree/",
            "https://www.geeksforgeeks.org/a-program-to-check-if-a-binary-tree-is-bst-or-not/",
            "Given the root of a binary tree, determine if it is a valid binary search tree (BST).",
            "Recursive Range Checking: Pass valid range (min_val, max_val) down recursion. Every node's value must strictly satisfy min_val < node.val < max_val. Update ranges for left and right children.",
            "O(N)",
            "O(Height of Tree)",
            """def isValidBST(root) -> bool:
    def validate(node, low=float('-inf'), high=float('inf')):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)
    return validate(root)""",
            """#include <climits>
using namespace std;

bool validate(TreeNode* node, long long low, long long high) {
    if (!node) return true;
    if (node->val <= low || node->val >= high) return false;
    return validate(node->left, low, node->val) && validate(node->right, node->val, high);
}

bool isValidBST(TreeNode* root) {
    return validate(root, LLONG_MIN, LLONG_MAX);
}""",
            20
        ),

        # Heaps & Priority Queues
        (
            "Heaps & Priority Queues",
            "Top K Frequent Elements",
            "Medium",
            "https://leetcode.com/problems/top-k-frequent-elements/",
            "https://www.geeksforgeeks.org/find-k-numbers-which-occur-most-times-in-an-array/",
            "Given an integer array nums and an integer k, return the k most frequent elements in O(N log K) or O(N).",
            "Bucket Sort Approach (O(N)): Count frequencies with hash map. Group numbers by frequency into an array of buckets (index = frequency). Traverse buckets from right to left to collect top k numbers.",
            "O(N)",
            "O(N)",
            """from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for n, c in count.items():
        buckets[c].append(n)
    res = []
    for i in range(len(buckets) - 1, 0, -1):
        for n in buckets[i]:
            res.append(n)
            if len(res) == k:
                return res
    return res""",
            """#include <vector>
#include <unordered_map>
using namespace std;

vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int, int> count;
    for (int n : nums) count[n]++;
    vector<vector<int>> buckets(nums.size() + 1);
    for (auto& p : count) buckets[p.second].push_back(p.first);
    vector<int> res;
    for (int i = buckets.size() - 1; i >= 0 && res.size() < k; i--) {
        for (int num : buckets[i]) {
            res.push_back(num);
            if (res.size() == k) return res;
        }
    }
    return res;
}""",
            21
        ),
        (
            "Heaps & Priority Queues",
            "Find Median from Data Stream",
            "Hard",
            "https://leetcode.com/problems/find-median-from-data-stream/",
            "https://www.geeksforgeeks.org/median-of-stream-of-running-integers-using-stl/",
            "The median is the middle value in an ordered integer list. Implement MedianFinder that supports addNum and findMedian in O(log N) and O(1).",
            "Two Heaps: A max-heap for the smaller half of numbers, and a min-heap for the larger half. Keep heaps balanced such that lengths differ by at most 1.",
            "O(log N) add, O(1) find",
            "O(N)",
            """import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # max-heap (invert values)
        self.large = []  # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0""",
            """#include <queue>
using namespace std;

class MedianFinder {
    priority_queue<int> small; // max-heap
    priority_queue<int, vector<int>, greater<int>> large; // min-heap
public:
    void addNum(int num) {
        small.push(num);
        large.push(small.top());
        small.pop();
        if (small.size() < large.size()) {
            small.push(large.top());
            large.pop();
        }
    }
    double findMedian() {
        return small.size() > large.size() ? small.top() : (small.top() + large.top()) / 2.0;
    }
};""",
            22
        ),

        # Backtracking
        (
            "Backtracking",
            "Subsets (Power Set)",
            "Medium",
            "https://leetcode.com/problems/subsets/",
            "https://www.geeksforgeeks.org/backtracking-to-find-all-subsets/",
            "Given an integer array nums of unique elements, return all possible subsets (the power set).",
            "Backtracking: At each index, decide whether to include nums[i] in the current subset. Recurse, then backtrack by popping nums[i] and explore without it.",
            "O(N * 2^N)",
            "O(N)",
            """def subsets(nums: list[int]) -> list[list[int]]:
    res = []
    subset = []
    def dfs(i):
        if i >= len(nums):
            res.append(subset.copy())
            return
        # Include nums[i]
        subset.append(nums[i])
        dfs(i + 1)
        # Exclude nums[i]
        subset.pop()
        dfs(i + 1)
    dfs(0)
    return res""",
            """#include <vector>
using namespace std;

void dfs(int i, vector<int>& nums, vector<int>& cur, vector<vector<int>>& res) {
    if (i >= nums.size()) {
        res.push_back(cur);
        return;
    }
    cur.push_back(nums[i]);
    dfs(i + 1, nums, cur, res);
    cur.pop_back();
    dfs(i + 1, nums, cur, res);
}

vector<vector<int>> subsets(vector<int>& nums) {
    vector<vector<int>> res;
    vector<int> cur;
    dfs(0, nums, cur, res);
    return res;
}""",
            23
        ),

        # Graphs
        (
            "Trees & Graphs",
            "Course Schedule (Cycle Detection / Topological Sort)",
            "Medium",
            "https://leetcode.com/problems/course-schedule/",
            "https://www.geeksforgeeks.org/topological-sorting-indegree-based-solution/",
            "There are numCourses courses labeled from 0 to numCourses - 1. You are given an array prerequisites. Return true if you can finish all courses, else false.",
            "Kahn's Algorithm (BFS with In-Degrees): Compute in-degrees of all courses. Add all 0 in-degree courses to a queue. Process queue, decrementing neighbors' in-degrees. If processed count equals numCourses, no cycle exists!",
            "O(V + E)",
            "O(V + E)",
            """from collections import deque

def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    adj = [[] for _ in range(numCourses)]
    in_degree = [0] * numCourses
    for crs, pre in prerequisites:
        adj[pre].append(crs)
        in_degree[crs] += 1
    q = deque([i for i in range(numCourses) if in_degree[i] == 0])
    count = 0
    while q:
        node = q.popleft()
        count += 1
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                q.append(neighbor)
    return count == numCourses""",
            """#include <vector>
#include <queue>
using namespace std;

bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
    vector<vector<int>> adj(numCourses);
    vector<int> inDegree(numCourses, 0);
    for (auto& pre : prerequisites) {
        adj[pre[1]].push_back(pre[0]);
        inDegree[pre[0]]++;
    }
    queue<int> q;
    for (int i = 0; i < numCourses; i++) {
        if (inDegree[i] == 0) q.push(i);
    }
    int visited = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        visited++;
        for (int v : adj[u]) {
            if (--inDegree[v] == 0) q.push(v);
        }
    }
    return visited == numCourses;
}""",
            24
        ),

        # Bit Manipulation & Math
        (
            "Bit Manipulation & Math",
            "Single Number",
            "Easy",
            "https://leetcode.com/problems/single-number/",
            "https://www.geeksforgeeks.org/find-element-appears-once-array-every-element-appears-twice/",
            "Given a non-empty array of integers nums, every element appears twice except for one. Find that single one in linear runtime and O(1) space.",
            "XOR properties: a ^ a = 0 and a ^ 0 = a. Since XOR is commutative and associative, XORing all elements together cancels out all pairs, leaving only the unique number.",
            "O(N)",
            "O(1)",
            """def singleNumber(nums: list[int]) -> int:
    res = 0
    for num in nums:
        res ^= num
    return res""",
            """#include <vector>
using namespace std;

int singleNumber(vector<int>& nums) {
    int res = 0;
    for (int n : nums) res ^= n;
    return res;
}""",
            25
        )
    ]

    for p in additional_problems:
        cursor.execute("""
        INSERT INTO dsa_problems (topic, title, difficulty, leetcode_url, gfg_url, description, approach_notes, time_complexity, space_complexity, code_python, code_cpp, order_idx)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    conn.commit()
    conn.close()
    print(f"Added {len(additional_problems)} additional problems to DSA sheet.")

if __name__ == "__main__":
    expand_dsa()
