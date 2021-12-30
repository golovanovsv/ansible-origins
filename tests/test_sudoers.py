import testinfra
import pytest

@pytest.fixture()
def AnsibleVars(host):
  default_vars = host.ansible("include_vars", "file=defaults/main.yml")["ansible_facts"]
  test_vars = host.ansible("include_vars", "file=molecule/default/vars.yml")["ansible_facts"]
  merged_vars = { **default_vars, **test_vars }
  return merged_vars

def test_group_sudo(host):
  assert host.group("sudo").exists

def test_sudoers_file(host):
  sudoers = host.file("/etc/sudoers")
  assert sudoers.is_file
  assert sudoers.user == "root"
  assert sudoers.group == "root"
  assert oct(sudoers.mode) == "0o440"

def test_sudoers_extra_configs(host, AnsibleVars):
  assert host.file("/etc/sudoers.d").is_directory
  for entry in AnsibleVars["extra_sudoers_configs"]:
    file = host.file("/etc/sudoers.d/{}".format(entry["name"]))
    assert file.is_file
    assert file.user == "root"
    assert file.group == "root"
    assert oct(file.mode) == "0o440"
