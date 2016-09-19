from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class ProvidesNginxStats(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:nginx-stats}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')

    @hook('{provides:nginx-stats}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.connected')

    def configure(self, port, path):
        address = hookenv.unit_get('private-address')
        url = 'http://{}:{}/{}'
        relation_info = {
            'status_url': url.format(address, port, path),
        }

        self.set_remote(**relation_info)
        self.set_state('{relation_name}.configured')
