"""Data reset preserves learner source and neighbouring module job namespaces."""
from fnmatch import fnmatch
from pathlib import Path

import pytest
from sqlalchemy.orm import Session

from app import course_reset
from app.config import Settings


class Queue:
    def __init__(self):
        self.data = {
            'arq:job:queued-module4': b'pending',
            'arq:result:assess:auto:exercises-module4:CLM-001:v1': b'done',
            'arq:retry:assess:auto:exercises-module4:CLM-001:v1': b'retry',
            'arq:result:assess:auto:exercises-module3:CLM-001:v1': b'other',
            'arq:result:assess:auto:exercises-module40:CLM-001:v1': b'other',
        }

    def exists(self, key):
        return key in self.data

    def zrange(self, *args):
        return [b'queued-module4']

    def delete(self, *keys):
        for key in keys:
            self.data.pop(key, None)

    def scan_iter(self, match):
        return [key for key in self.data if fnmatch(key, match)]


def configure(monkeypatch, service, queue, **overrides):
    settings = Settings(_env_file=None, **overrides)
    monkeypatch.setattr(course_reset, 'get_settings', lambda: settings)
    monkeypatch.setattr(course_reset, 'Redis', type('FakeRedis', (), {'from_url': staticmethod(lambda *a, **k: queue)}))
    monkeypatch.setattr(course_reset, 'SessionLocal', lambda: Session(service.repo.session.bind))


def test_reset_preserves_other_module_jobs_and_source(service, monkeypatch):
    queue = Queue()
    configure(monkeypatch, service, queue)
    source_file = Path(__file__).parents[1] / 'app/exercises/autonomy.py'
    original = source_file.read_bytes()
    service.claim('CLM-001').status = 'accepted'
    service.repo.commit()
    course_reset.main()
    service.repo.session.expire_all()
    assert len(service.list_claims()) == 7
    assert all(c['status'] == 'submitted' for c in service.list_claims())
    assert source_file.read_bytes() == original
    assert queue.data == {
        'arq:result:assess:auto:exercises-module3:CLM-001:v1': b'other',
        'arq:result:assess:auto:exercises-module40:CLM-001:v1': b'other',
    }
    course_reset.main()
    assert len(queue.data) == 2


def test_running_worker_blocks_reset(service, monkeypatch):
    queue = Queue()
    queue.data['exercises-module4:health-check'] = b'worker running'
    configure(monkeypatch, service, queue)
    before = dict(queue.data)
    with pytest.raises(ValueError, match='stop this module'):
        course_reset.main()
    assert queue.data == before


@pytest.mark.parametrize('overrides', [
    {'database_url': 'postgresql+psycopg://claims:claims@localhost:55432/exercises_module3'},
    {'redis_url': 'redis://localhost:6379/0'},
    {'arq_queue_name': 'exercises-module3'},
])
def test_unexpected_data_configuration_blocks_reset(service, monkeypatch, overrides):
    queue = Queue()
    configure(monkeypatch, service, queue, **overrides)
    before = dict(queue.data)
    with pytest.raises(ValueError, match='Reset refused'):
        course_reset.main()
    assert queue.data == before
