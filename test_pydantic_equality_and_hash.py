from pydantic import BaseModel


class Money(BaseModel):
    class Config:
        frozen = True  # creates __hash__ method

    qty: int
    currency: str


def test_two_instance_equals():
    five1 = Money(qty=5, currency="gbp")
    five2 = Money(qty=5, currency="gbp")
    assert five1 == five2
    # assert five1 is five2  # fails, they are not the same objects
    assert len({five1, five2}) == 1


class Batch(BaseModel):
    reference: str
    sku: str
    qty: int

    def __hash__(self):
        return hash(self.reference)


def test_can_create_batch_set():
    batch_set = {
        Batch(reference="batch1", sku="CHAIR", qty=30),
        Batch(reference="batch2", sku="TABLE", qty=3),
    }

    print(batch_set)
    assert len(batch_set) == 2
    assert isinstance(batch_set, set)