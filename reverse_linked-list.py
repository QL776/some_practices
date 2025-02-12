class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution(object):
    def reverseList(self, head):
        pre = None
        cur = head

        while cur is not None:
            next = cur.next
            cur.next = pre
            pre = cur
            cur = next
        
        return pre

def bulid_linked_list(values):
    head = ListNode(values[0])
    cur = head
    for val in values[1:]:
        cur.next = ListNode(val)
        cur = cur.next
    return head

def print_linked_list(head):
    cur = head
    while cur:
        print(cur.val, end=' ')
        cur = cur.next
    print()

if __name__ == "__main__":
    
    values = [1, 2, 3, 4, 5, 6, 7]

    head = bulid_linked_list(values)
    solution = Solution()
    reversed_head = solution.reverseList(head)

    print_linked_list(reversed_head)




