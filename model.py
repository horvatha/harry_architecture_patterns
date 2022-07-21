from operator import itemgetter

from pydantic import BaseModel
from datetime import date


class LineItem(BaseModel):
    sku: str
    qty: int
    status: str = 'new'

    def set_state(self, status: str) -> None:
        self.status = status


class Batch(BaseModel):
    reference: str = ''
    sku: str
    available_quantity: int
    eta: date = date.today()  # today if in Warehouse

    def allocate(self, line_item: LineItem):
        assert self.available_quantity >= line_item.qty
        self.available_quantity -= line_item.qty
        line_item.set_state("allocated")


BatchList = list[Batch]


def allocate_from_batch_list(line_item: LineItem, batch_list: BatchList) -> Batch:
    given_item_batches = filter(
        lambda batch: batch.sku == line_item.sku,
        batch_list
    )
    earliest_batch = min(given_item_batches, key=lambda batch: batch.eta)
    earliest_batch.allocate(line_item)
    return earliest_batch
