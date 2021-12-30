import testinfra
import pytest
import re

@pytest.fixture()
def AnsibleVars(host):
  default_vars = host.ansible("include_vars", "file=defaults/main.yml")["ansible_facts"]
  test_vars = host.ansible("include_vars", "file=molecule/default/vars.yml")["ansible_facts"]
  merged_vars = { **default_vars, **test_vars }
  merged_vars["distibution"] = re.findall("ID=([a-z]+)", host.file("/etc/os-release").content_string)
  return merged_vars

def test_software_repo_present(host, AnsibleVars):
  # Проверка пакетных репозиториев для yum не реализована
  if AnsibleVars["distibution"] in ["ubuntu", "debian"]:
    repo = host.file("/etc/apt/sources.list.d/download_docker_com_linux_ubuntu.list")
    assert repo.is_file
    assert oct(repo.mode) == "0o644"
    assert repo.user == "root"
    assert repo.group == "root"

def test_software_installed(host, AnsibleVars):
  for package in AnsibleVars["extra_software"]:
    assert host.package(package).is_installed
