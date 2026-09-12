import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_book as book


class EclipsePdfTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        for name, path in (("BOOK_DIR", root), ("BUILD_DIR", root / "build"),
                           ("FIGURES_DIR", root / "figures")):
            mock = patch.object(book, name, path)
            mock.start()
            self.addCleanup(mock.stop)
        self.source = root / "figures/eclipse_spine/example.svg"
        self.source.parent.mkdir(parents=True)
        self.source.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')

    @staticmethod
    def render(command, **kwargs):
        Path(command[command.index("--output") + 1]).write_bytes(b"rendered")

    def test_cache_tracks_svg_content(self):
        with patch.object(book.shutil, "which", return_value="rsvg-convert"), \
                patch.object(book.subprocess, "run", side_effect=self.render) as run:
            first = book.flatten_eclipse_for_pdf(self.source)
            self.assertEqual(first, book.flatten_eclipse_for_pdf(self.source))
            self.assertEqual(run.call_count, 1)
            self.source.write_text('<svg xmlns="http://www.w3.org/2000/svg"><g/></svg>')
            second = book.flatten_eclipse_for_pdf(self.source)
            self.assertNotEqual(first, second)
            command = run.call_args.args[0]
            self.assertEqual(command[command.index("--width") + 1], "4200")
            self.assertEqual(command[command.index("--background-color") + 1], "white")

    def test_only_eclipse_links_change_and_attributes_survive(self):
        target = book.BUILD_DIR / "figure-rasters/example.png"
        md = ('![Caption](figures/eclipse_spine/example.svg){#fig:example width=100%}\n'
              '![Other](figures/mapping_mouth/example.svg){width=95%}')
        with patch.object(book, "flatten_eclipse_for_pdf", return_value=target) as render:
            result = book.prefer_png_images_for_pdf(md)
        self.assertEqual(result, md.replace("figures/eclipse_spine/example.svg",
                                            "build/figure-rasters/example.png"))
        render.assert_called_once_with(self.source)

    def test_conversion_failure_does_not_leave_cached_output(self):
        def fail(command, **kwargs):
            self.render(command)
            raise subprocess.CalledProcessError(1, command)

        with patch.object(book.shutil, "which", return_value="rsvg-convert"), \
                patch.object(book.subprocess, "run", side_effect=fail):
            with self.assertRaises(subprocess.CalledProcessError):
                book.flatten_eclipse_for_pdf(self.source)
        self.assertEqual(list((book.BUILD_DIR / "figure-rasters").glob("*.png")), [])

    def test_missing_converter_does_not_fall_back_to_broken_svg(self):
        with patch.object(book.shutil, "which", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "rsvg-convert is required"):
                book.flatten_eclipse_for_pdf(self.source)


if __name__ == "__main__":
    unittest.main()
