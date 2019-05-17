from charms.reactive import when, when_not
from charms.reactive.flags import set_flag
from charmhelpers.core.hookenv import (
    config,
    log,
    metadata,
    status_set,
)


from charms import layer


@when_not('layer.docker-resource.jenkins_image.fetched')
def fetch_image():
    layer.docker_resource.fetch('jenkins_image')


@when('layer.docker-resource.jenkins_image.available')
@when_not('jenkins.configured')
def config_jenkins():
    status_set('maintenance', 'Configuring jenkins container')

    spec = make_pod_spec()
    log('set pod spec:\n{}'.format(spec))
    layer.caas_base.pod_spec_set(spec)

    set_flag('jenkins.configured')


def make_pod_spec():
    with open('reactive/spec_template.yaml') as spec_file:
        pod_spec_template = spec_file.read()

    md = metadata()
    cfg = config()

    image_info = layer.docker_resource.get_info('jenkins_image')

    context = {
        'name': md.get('name'),
        'annotations': cfg.get('annotations'),
        'docker_image_path': image_info.registry_path,
        'docker_image_username': image_info.username,
        'docker_image_password': image_info.password,
    }
    return pod_spec_template % context


@when('jenkins.configured')
def jenkins_active():
    status_set('active', '')
