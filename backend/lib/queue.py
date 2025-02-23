from collections import deque

from backend.lib.models import Payment



class PaymentQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, item: Payment):
        self.queue.append(item)

    def dequeue(self) -> Payment:
        if self.queue:
            return self.queue.popleft()
        raise IndexError("dequeue from empty queue")

    def is_empty(self):
        return len(self.queue) == 0

    def __len__(self):
        return len(self.queue)
