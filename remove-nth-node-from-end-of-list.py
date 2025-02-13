class ListNode(object):
    def __init__(self, val=0,next=None):
        self.val = val
        self.next = next

def bulid_linked_list(values):
    head = ListNode(values[0])
    cur = head
    for value in values[1:]:
        cur.next = ListNode(value)
        cur = cur.next
    return head

def print_linked_list(head):
    cur = head
    while cur:
        print(cur.val,end="->")
        cur = cur.next
    print("None")

class Solution(object):
  def removerNthFromend(self,head,n):    
    dummy = ListNode(0,head)
    slow = dummy
    fast = dummy

    for _ in range(n):
      fast = fast.next

    if fast is None:
        return dummy.next.next
    
    while fast and fast.next is not None:
        slow = slow.next
        fast = fast.next
    
    slow.next = slow.next.next

    return dummy.next

if __name__ == "__main__":
    values = [1, 2, 3, 4, 5, 6, 7]
    head = bulid_linked_list(values)
    solution = Solution()
    result = solution.removerNthFromend(head,3)
    print_linked_list(result)