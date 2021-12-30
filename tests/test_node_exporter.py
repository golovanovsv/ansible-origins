import testinfra
import pytest
# import urllib3

# @pytest.fixture()
# def AnsibleVars(host):
#   default_vars = host.ansible("include_vars", "file=defaults/main.yml")["ansible_facts"]
#   test_vars = host.ansible("include_vars", "file=molecule/default/vars.yml")["ansible_facts"]
#   merged_vars = { **default_vars, **test_vars }
#   return merged_vars

def test_service_is_enabled(host):
  assert host.service("node-exporter").is_enabled

def test_service_is_running(host):
  assert host.service("node-exporter").is_running

# Необходимо выполнять исключительно с машины, где запущен docker
# def test_get_metrics(host, AnsibleVars):
#   ip = host.interface("eth0").addresses[0]
#   httpPool = urllib3.PoolManager()
#   response = httpPool.request("GET", "http://{}:{}".format(ip, AnsibleVars["node_exporter_listen_port"]))
#   assert(len(response.data) > 0)
