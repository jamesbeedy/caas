from charms.reactive import when, when_not
from charms.reactive.flags import set_flag
from charmhelpers.core.hookenv import (
    config,
    log,
    metadata,
    status_set,
)


from charms import layer


@when_not('layer.docker-resource.jupyter_image.fetched')
def fetch_image():
    layer.docker_resource.fetch('jupyter_image')


@when('layer.docker-resource.jupyter_image.available')
@when_not('jupyter.configured')
def config_juptyer():
    status_set('maintenance', 'Configuring jupyter container')

    spec = make_pod_spec()
    log('set pod spec:\n{}'.format(spec))
    layer.caas_base.pod_spec_set(spec)

    set_flag('jupyter.configured')


def make_pod_spec():
    with open('reactive/spec_template.yaml') as spec_file:
        pod_spec_template = spec_file.read()

    md = metadata()
    cfg = config()

    user = cfg.get('user')
    set_flag('user', user)
    password = cfg.get('password')
    set_flag('password', password)

    image_info = layer.docker_resource.get_info('jupyter_image')

    data = {
        'name': md.get('name'),
        'docker_image_path': image_info.registry_path,
        'docker_image_username': image_info.username,
        'docker_image_password': image_info.password,
    }
    data.update(cfg)
    return pod_spec_template % data


@when('juputer.configured')
def jupter_active():
    status_set('active', '')
