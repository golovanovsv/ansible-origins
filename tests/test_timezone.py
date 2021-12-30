import testinfra
import pytest

@pytest.fixture()
def AnsibleVars(host):
  default_vars = host.ansible("include_vars", "file=defaults/main.yml")["ansible_facts"]
  test_vars = host.ansible("include_vars", "file=molecule/default/vars.yml")["ansible_facts"]
  merged_vars = { **default_vars, **test_vars }
  return merged_vars

def test_timezone(host, AnsibleVars):
  # TODO: Сделать проверку для dhl-based дистрибутивов
  tz = host.file("/etc/timezone")
  if tz.is_file:
    server_timezone = tz.content_string.replace("\n", "")
    config_timezone = AnsibleVars["default_timezone"] if "timezone" not in AnsibleVars else AnsibleVars["timezone"]
    assert server_timezone == config_timezone
