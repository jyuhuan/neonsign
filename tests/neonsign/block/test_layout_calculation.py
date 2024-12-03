from typing import List

from neonsign.block.layout_calculation import ItemsDistributor
from tests.neonsign.block.test_canvas import TestCanvas


class TestLayoutCalculation(TestCanvas):

    def test_items_distributor(self):

        def test(
                num_items: int,
                num_recipients: int,
                expected_result: List[int]
        ):
            distributor = ItemsDistributor(
                num_items=num_items,
                num_recipients=num_recipients
            )
            self.assertEqual(
                expected_result,
                [
                    distributor.num_items_for_recipient(i)
                    for i in range(0, num_recipients)
                ]
            )

        test(num_items=0, num_recipients=0, expected_result=[])
        test(num_items=4, num_recipients=0, expected_result=[])
        test(num_items=0, num_recipients=4, expected_result=[0, 0, 0, 0])
        test(num_items=3, num_recipients=4, expected_result=[1, 1, 1, 0])
        test(num_items=4, num_recipients=4, expected_result=[1, 1, 1, 1])
        test(num_items=7, num_recipients=4, expected_result=[2, 2, 2, 1])
        test(num_items=8, num_recipients=4, expected_result=[2, 2, 2, 2])

