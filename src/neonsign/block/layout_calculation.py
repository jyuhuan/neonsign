class ItemsDistributor:
    avg: int
    mod: int

    def __init__(self, num_items: int, num_recipients: int):
        self.num_items: int = num_items
        self.num_recipients: int = num_recipients

        if num_recipients == 0:
            self.avg = 0
        else:
            self.avg = num_items // num_recipients

        if num_recipients == 0:
            self.mod = 0
        else:
            self.mod = self.num_items % self.num_recipients

    def num_items_for_recipient(self, i: int) -> int:
        if i < self.mod:
            return self.avg + 1
        else:
            return self.avg
