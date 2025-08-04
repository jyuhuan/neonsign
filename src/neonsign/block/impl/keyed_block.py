from neonsign.block.block import Block, WrapperBlock


class KeyedBlock(WrapperBlock):

    def __init__(self, original: Block, key: str):
        super().__init__(original)
        self.key = key
