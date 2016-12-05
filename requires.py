
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class RequiresNginxStats(RelationBase):
    scope = scopes.GLOBAL

    auto_accessors = ['status_url']

    @hook('{requires:nginx-stats}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        if conv.get_remote('status_url'):
            conv.set_state('{relation_name}.available')

    @hook('{requires:nginx-stats}-relation-{departed,broken}')
    def broken(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.available')

    def configuration(self):
        conv = self.conversation()
        return {k: conv.get_remote(k) for k in self.auto_accessors}
