from __future__ import annotations

from typing import Any, Optional


class Node:
    """Represents a node to be used in a doubly linked list."""
    def __init__(
            self,
            value: Any,
            prev: Optional[Node] = None,
            nxt: Optional[Node] = None):
        self.value = value

        # NOTE: This means that if prev and nxt are None, self.prev and
        # self.next will be self.  You may find this useful.  This means
        # that self.prev and self.next aren't Optional Nodes, they are
        # always Nodes.
        self.prev: Node = prev or self
        self.next: Node = nxt or self

    def __repr__(self) -> str:
        return 'Value: %r %r %r' % (self.value, self.prev, self.next)


class OrderedList:
    """A circular, doubly linked list of items, from lowest to highest.

    The contents of the list *must* have a accurate notation of less
    than and of equality.  That is to say, the contents of the list must
    implement both __lt__ and __eq__.
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0


def insert(lst: OrderedList, value: Any) -> None:
    new_node = Node(value, None, None)

    if lst.size == 0:
        lst.tail = new_node
        lst.head = lst.tail
        lst.tail.next = lst.head
        lst.head.prev = lst.tail

    elif lst.head.value > new_node.value:
        lst.head.prev = new_node
        new_node.next = lst.head
        lst.head = new_node
        lst.tail.next = lst.head

    elif lst.tail.value < new_node.value:
        new_node.prev = lst.tail
        lst.tail.next = new_node
        lst.tail = new_node
        lst.tail.next = lst.head

    else:
        temp = lst.head.next
        while temp.value < new_node.value:
            temp = temp.next
        prev_node = temp.prev
        prev_node.next = new_node
        new_node.prev = prev_node
        temp.prev = new_node
        new_node.next = temp

    lst.size += 1


def remove(lst: OrderedList, value: Any) -> None:
    if not contains(lst, value):
        raise ValueError('Value not exist')
    if value == lst.head.value:
        lst.head = lst.head.next
        lst.head.prev = lst.tail

    elif lst.tail.value == value:
        pre_tail = lst.tail.prev
        pre_tail.next = lst.head
        lst.head.prev = pre_tail
        lst.tail = pre_tail

    temp = lst.head.next

    for i in range(1, lst.size - 1):
        if temp.value == value:
            prev_node = temp.prev
            next_node = temp.next
            prev_node.next = next_node
            next_node.prev = prev_node
        temp = temp.next

    lst.size -= 1


def contains(lst: OrderedList, value: Any) -> bool:
    temp = lst.head
    for i in range(lst.size):
        if temp.value == value:
            return True
        temp = temp.next
    return False


def index(lst: OrderedList, value: Any) -> int:
    temp = lst.head
    for i in range(lst.size):
        if temp.value == value:
            return i
        temp = temp.next
    raise ValueError('Value not exist')


def get(lst: OrderedList, index: int) -> Any:
    if index >= lst.size:
        raise IndexError('Invalid index')
    temp = lst.head
    for i in range(index):
        temp = temp.next
    return temp.value


def pop(lst: OrderedList, index: int) -> Any:
    if index >= lst.size:
        raise IndexError('Invalid index')
    temp = lst.head
    pop = 0
    if index == 0:
        pop = lst.head.value
        lst.head = lst.head.next
        lst.head.prev = lst.tail
    elif index == lst.size - 1:
        pop = lst.tail.value
        pre_tail = lst.tail.prev
        pre_tail.next = lst.head
        lst.head.prev = pre_tail
        lst.tail = pre_tail
    else:
        for i in range(index):
            temp = temp.next
        pop = temp.value
        prev_node = temp.prev
        next_node = temp.next
        prev_node.next = next_node
        next_node.prev = prev_node
    lst.size -= 1
    return pop


def is_empty(lst: OrderedList) -> bool:
    if lst.size == 0:
        return True
    return False


def size(lst: OrderedList) -> int:
    return lst.size
