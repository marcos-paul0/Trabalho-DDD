import unittest
import tempfile
import shutil
from katalog.infrastructure.in_memory_repository import InMemoryMidiaRepository
from katalog.infrastructure.file_repository import FileBasedMidiaRepository
from katalog.domain.factories import MidiaFactory


class RepositoryTests(unittest.TestCase):
    def test_in_memory_repository(self):
        repo = InMemoryMidiaRepository()
        m = MidiaFactory.criar_item('RepoTest', 10)
        repo.salvar(m)
        found = repo.buscar_por_id(str(m.id))
        self.assertEqual(found.titulo, m.titulo)

    def test_file_repository(self):
        tmp = tempfile.mkdtemp()
        try:
            repo = FileBasedMidiaRepository(folder=tmp)
            m = MidiaFactory.criar_item('FileRepo', 5)
            repo.salvar(m)
            found = repo.buscar_por_id(str(m.id))
            self.assertEqual(found.titulo, m.titulo)
        finally:
            shutil.rmtree(tmp)


if __name__ == '__main__':
    unittest.main()
