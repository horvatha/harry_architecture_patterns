from copy import deepcopy
from datetime import date, timedelta
import pytest

from model import LineItem, Batch, allocate_from_batch_list

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


@pytest.fixture()
def batch__line_item__fixture():
    batch4 = Batch(sku="horse", available_quantity=4)
    batch1 = Batch(sku="horse", available_quantity=1)
    line_item = LineItem(sku="horse", qty=2)
    yield batch4, batch1, line_item


@pytest.fixture()
def batches_local_and_shipment():
    batch_local = Batch(sku="horse", available_quantity=4)
    batch_shipment_1day = Batch(sku="horse", available_quantity=4, eta=tomorrow)
    batch_shipment_days = Batch(sku="horse", available_quantity=4, eta=later)
    yield batch_local, batch_shipment_1day, batch_shipment_days


def test_allocating_to_a_batch_reduces_the_available_quantity(batch__line_item__fixture):
    batch4, batch1, line_item = batch__line_item__fixture
    batch4.allocate(line_item)
    assert batch4.available_quantity == 2


def test_can_allocate_if_available_greater_than_required(batch__line_item__fixture):
    batch4, batch1, line_item = batch__line_item__fixture
    batch4.allocate(line_item)
    assert line_item.status == "allocated"


def test_cannot_allocate_if_available_smaller_than_required(batch__line_item__fixture):
    batch4, batch1, line_item = batch__line_item__fixture
    batch1_copy = deepcopy(batch1)
    line_item_copy = deepcopy(line_item)
    with pytest.raises(AssertionError) as excinfo:
        batch1.allocate(line_item)
    assert line_item == line_item_copy
    assert batch1 == batch1_copy


def test_can_allocate_if_available_equal_to_required(batch__line_item__fixture):
    batch4, _, _ = batch__line_item__fixture
    line_item = LineItem(sku='horse', qty=4)
    batch4.allocate(line_item)
    assert line_item.status == "allocated"


def test_prefers_warehouse_batches_to_shipments(batches_local_and_shipment):
    batch_local, batch_shipment_1day, batch_shipment_days = batches_local_and_shipment
    line_item = LineItem(sku="horse", qty=2)
    batch = allocate_from_batch_list(line_item, [batch_local, batch_shipment_1day])
    assert batch == batch_local
    assert batch.available_quantity == 2


def test_prefers_earlier_batches(batches_local_and_shipment):
    batch_local, batch_shipment_1day, batch_shipment_days = batches_local_and_shipment
    line_item = LineItem(sku="horse", qty=2)
    batch = allocate_from_batch_list(line_item, [batch_shipment_1day, batch_shipment_days])
    assert batch == batch_shipment_1day
    assert batch.available_quantity == 2
