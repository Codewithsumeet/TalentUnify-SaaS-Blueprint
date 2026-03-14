import asyncio
import builtins
import importlib
import sys


def test_pinecone_client_degrades_gracefully_when_dependency_missing():
    original_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "pinecone":
            raise ModuleNotFoundError("simulated missing dependency")
        return original_import(name, *args, **kwargs)

    try:
        builtins.__import__ = fake_import
        sys.modules.pop("search.pinecone_client", None)
        pinecone_client = importlib.import_module("search.pinecone_client")

        result = asyncio.run(pinecone_client.query(vector=[0.1], top_k=1))
        assert result.matches == []

        asyncio.run(pinecone_client.upsert("candidate-1", [0.1], {"name": "Test"}))
        asyncio.run(pinecone_client.delete_candidate("candidate-1"))
    finally:
        builtins.__import__ = original_import
        sys.modules.pop("search.pinecone_client", None)
        importlib.import_module("search.pinecone_client")
