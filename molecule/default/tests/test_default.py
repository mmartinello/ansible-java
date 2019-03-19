import os
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_apt_repository_key_is_added(host):
    cmd = host.run('apt-key list')
    sre_match_type = type(re.match('', ''))

    # Check the key ID
    key_id = 'C251 8248 EEA1 4886'
    pattern = re.compile(key_id)
    match = pattern.search(cmd.stdout)
    assert type(match) is sre_match_type

    # Check the key issuer name
    key_issuer = 'Launchpad VLC'
    pattern = re.compile(key_issuer)
    match = pattern.search(cmd.stdout)
    assert type(match) is sre_match_type


def test_java_command_exists(host):
    cmd = host.run('which java')
    assert cmd.stdout == '/usr/bin/java'


def test_java_version(host):
    cmd = host.run('java -version')
    lines = re.split('\n', cmd.stderr)

    regex = '^java version "(1\.8[0-9\._]+)"$'
    pattern = re.compile(regex)
    matches = pattern.search(lines[0])
    assert len(matches.groups()) is 1
