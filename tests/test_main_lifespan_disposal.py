import asyncio

import main


class _FakeConnection:
    async def run_sync(self, _fn):
        return None


class _FakeBeginContext:
    def __init__(self, engine):
        self.engine = engine

    async def __aenter__(self):
        self.engine.begin_calls += 1
        return _FakeConnection()

    async def __aexit__(self, exc_type, exc, tb):
        return False


class _FakeEngine:
    def __init__(self):
        self.begin_calls = 0
        self.disposed = False

    def begin(self):
        return _FakeBeginContext(self)

    async def dispose(self):
        self.disposed = True


def test_lifespan_disposes_both_async_engines(monkeypatch):
    primary_engine = _FakeEngine()
    secondary_engine = _FakeEngine()

    monkeypatch.setattr(main, "async_engine", primary_engine)
    monkeypatch.setattr(main, "db_async_engine", secondary_engine)

    async def _run_lifespan_once():
        async with main.lifespan(main.app):
            return None

    asyncio.run(_run_lifespan_once())

    assert primary_engine.begin_calls == 1
    assert secondary_engine.begin_calls == 1
    assert primary_engine.disposed is True
    assert secondary_engine.disposed is True
