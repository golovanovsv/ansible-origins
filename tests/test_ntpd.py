import testinfra
import pytest

@pytest.fixture()
def AnsibleVars(host):
  default_vars = host.ansible("include_vars", "file=defaults/main.yml")["ansible_facts"]
  test_vars = host.ansible("include_vars", "file=molecule/default/vars.yml")["ansible_facts"]
  merged_vars = { **default_vars, **test_vars }
  return merged_vars

def test_configs(host, AnsibleVars):
  # Проверяем содержимое файлов конфигураций
  timesyncd = host.file("/etc/systemd/timesyncd.conf").exists
  ntpd = host.file("/etc/ntp.conf").exists

  if timesyncd:
    config_file = host.file("/etc/systemd/timesyncd.conf").content_string
    for server in AnsibleVars["ntp_servers"]:
      assert server in config_file
    assert (not host.file("/lib/systemd/system/systemd-timesyncd.service.d/disable-with-time-daemon.conf").exists)
  
  if ntpd:
    config_file = host.file("/etc/ntp.conf").content_string
    for server in AnsibleVars["ntp_servers"]:
      assert "server " + server in config_file

def test_service(host, AnsibleVars):
  # Проверяем состояние сервисов
  timesyncd = host.file("/etc/systemd/timesyncd.conf").exists
  ntpd = host.file("/etc/ntp.conf").exists

  if timesyncd:
    assert host.service("systemd-timesyncd").is_enabled
    assert host.service("systemd-timesyncd").is_running
  
  if ntpd:
    distribution = host.system_info.distribution
    assert host.service(AnsibleVars["ntp_service"][distribution]).is_enabled
    assert host.service(AnsibleVars["ntp_service"][distribution]).is_running
