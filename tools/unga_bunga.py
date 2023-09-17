def find_comps(arr, ind, tar):
    if tar == 0:
        return [[ind]]
    comps = []
    for i in range(ind+1, len(arr)):
        if arr[i] <= tar:
            print(arr, i, arr[i])
            temp = find_comps(arr, i, tar - arr[i])
            for t in temp:
                comps.append(t + [ind])
    return comps

#print(find_comps([4,3,2,3,5,2,1], 0, 1))

def canPartitionKSubsets(nums, k):
    total_sum = 0
    for num in nums:
        total_sum += num
    target_sum = 0
    if total_sum % k == 0:
        target_sum = total_sum // k
    else:
        return False
    # print(target_sum)
    visited = [False] * len(nums)

    def helper(cur_idx, cur_sum):
        if cur_sum == target_sum:
            return True
        if cur_sum > target_sum:
            return False
        if cur_idx < 0:
            return cur_sum == target_sum
        found = False
        temp = 0
        if not visited[cur_idx]:
            found = found or helper(cur_idx - 1, cur_sum + nums[cur_idx])
        if found:
            visited[cur_idx] = True
            print(nums[cur_idx])
            return True
        if not found:
            found = found or helper(cur_idx - 1, cur_sum)
        return found

    for _ in range(k):
        helper(len(nums) - 1, 0)
        print("break")
        print(visited.copy())

print(canPartitionKSubsets(nums = [4,3,2,3,5,2,1], k = 4))