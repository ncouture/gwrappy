from datetime import datetime
from pytz import UTC
import humanize


class GcsResponse:
    def __init__(self, description):
        self.description = description.strip().title()
        self.start()

    def start(self):
        setattr(self, 'start_time', datetime.now(UTC))

    def load_resp(self, resp, override_updated=False):
        assert isinstance(resp, dict)
        setattr(self, 'resp', resp)
        setattr(self, 'size', humanize.naturalsize(int(resp['size'])))

        if override_updated:
            updated_at = datetime.now(UTC)
        else:
            updated_at = UTC.localize(datetime.strptime(resp['updated'], '%Y-%m-%dT%H:%M:%S.%fZ'))

        setattr(self, 'time_taken', dict(zip(
            ('m', 's'),
            divmod((updated_at - getattr(self, 'start_time')).seconds if updated_at > getattr(self, 'start_time') else 0, 60)
        )))

        setattr(self, 'full_path', 'gs://%s/%s' % (resp['bucket'], resp['name']))

    def __repr__(self):
        return '[BigQuery] %s %s (%s)' % (
            self.description,
            getattr(self, 'full_path'),
            '{m} Minutes {s} Seconds'.format(**getattr(self, 'time_taken'))
        )

    __str__ = __repr__