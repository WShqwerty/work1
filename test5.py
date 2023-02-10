from typing import List


def rotate(nums: List[int], k: int):
    if len(nums) < k:
        k = k % len(nums) 
    nums[0:len(nums)-k:], nums[len(nums)-k::] = nums[len(nums)-k::], nums[0:len(nums)-k:]


def rotate_c(nums: List[int], k: int):
    for i in range(k):
        nums[0:len(nums)-1:], nums[len(nums)-1::] = nums[len(nums)-1::], nums[0:len(nums)-1:]
    

if __name__ == "__main__":
    l = [1, 2, 3, 4, 5, 6, 3]
    n = 21
    rotate(l, n)
    print(l)
    l = [1, 2, 3, 4, 5, 6, 3]
    rotate_c(l, n)
    print(l)