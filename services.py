from __future__ import annotations

import model
from model import OrderLine
from repository import AbstractRepository


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_batch(ref, sku: str, qty: int, eta, repo, session) -> None:
    batch = model.Batch(ref=ref, sku=sku, qty=qty, eta=eta)
    repo.add(batch)
    session.commit()


def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref


def deallocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    batch_reference = model.deallocate(line, batches)
    session.commit()
    return batch_reference
