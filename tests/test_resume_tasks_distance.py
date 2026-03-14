import builtins

from tasks import resume_tasks


def test_fallback_levenshtein_distance_expected_value():
    assert resume_tasks._fallback_levenshtein("kitten", "sitting") == 3


def test_distance_falls_back_when_levenshtein_package_missing(monkeypatch):
    original_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "Levenshtein":
            raise ModuleNotFoundError("simulated missing dependency")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    resume_tasks._distance_impl = None

    assert resume_tasks._distance("abc", "adc") == 1
    assert resume_tasks._distance_impl is resume_tasks._fallback_levenshtein
