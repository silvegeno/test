import tempfile
import unittest
from pathlib import Path

from rss_news import translate_to_ru


class TranslateFallbackTests(unittest.TestCase):
    """Перевод не должен ронять ленту: при отказе провайдера остаётся оригинал."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.cache = Path(self.directory.name) / "cache.json"

    def tearDown(self):
        self.directory.cleanup()

    def test_provider_failure_keeps_original_text(self):
        items = [{"title": "Banks Have Had It", "description": "Story about AI"}]

        def failing(text):
            raise RuntimeError("429 Too Many Requests")

        result = translate_to_ru(items, cache_path=self.cache, translator=failing)
        self.assertEqual(result[0]["title"], "Banks Have Had It")
        self.assertEqual(result[0]["description"], "Story about AI")
        self.assertFalse(result[0]["translated"])
        self.assertFalse(self.cache.exists(), "неудачный перевод не должен попадать в кеш")

    def test_stops_after_first_failure(self):
        items = [{"title": "A", "description": "B"}, {"title": "C", "description": "D"}]
        calls = []

        def failing(text):
            calls.append(text)
            raise RuntimeError("429")

        translate_to_ru(items, cache_path=self.cache, translator=failing)
        self.assertEqual(len(calls), 1, "после первой ошибки перебор провайдера прекращается")

    def test_success_is_cached_and_reused(self):
        calls = []

        def stub(text):
            calls.append(text)
            return "ПЕРЕВОД:" + text

        first = translate_to_ru([{"title": "Hello", "description": "World"}], cache_path=self.cache, translator=stub)
        self.assertEqual(first[0]["title"], "ПЕРЕВОД:Hello")
        self.assertTrue(first[0]["translated"])
        self.assertEqual(len(calls), 2)

        second = translate_to_ru([{"title": "Hello", "description": "World"}], cache_path=self.cache, translator=stub)
        self.assertEqual(len(calls), 2, "повторный прогон берёт переводы из кеша")
        self.assertTrue(second[0]["translated"])

    def test_empty_fields_do_not_block(self):
        result = translate_to_ru(
            [{"title": "Не указана", "description": ""}], cache_path=self.cache, translator=lambda text: "x"
        )
        self.assertTrue(result[0]["translated"])


if __name__ == "__main__":
    unittest.main()
