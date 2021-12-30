import testinfra
import pytest

@pytest.fixture()
def AnsibleVars(host):
  default_vars = host.ansible("include_vars", "file=defaults/main.yml")["ansible_facts"]
  test_vars = host.ansible("include_vars", "file=molecule/default/vars.yml")["ansible_facts"]
  merged_vars = { **default_vars, **test_vars }
  return merged_vars

def test_python_installed(host):
  assert (
    host.package("python").is_installed or 
    host.package("python2").is_installed or 
    host.package("python3").is_installed
  )

def test_pip_packages_installed(host, AnsibleVars):
  pips = host.pip.get_packages()
  for package in AnsibleVars["extra_pip_software"]:
    assert package in pips
