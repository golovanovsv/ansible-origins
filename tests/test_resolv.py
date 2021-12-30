# /etc/resolv.conf read-only for docker driver
# import testinfra
# import pytest

# @pytest.fixture()
# def AnsibleVars(host):
#   default_vars = host.ansible("include_vars", "file=../../defaults/main.yml")["ansible_facts"]
#   test_vars = host.ansible("include_vars", "file=vars.yml")["ansible_facts"]
#   merged_vars = { **default_vars, **test_vars }
#   return merged_vars

# def test_resolv(host, AnsibleVars):
#   resolv_conf = host.file("/etc/resolv.conf").content_string.split("\n")
#   for dns in AnsibleVars["dns_servers"]:
#     assert "nameserver "+dns in resolv_conf
#   assert "options timeout:"+AnsibleVars["dns_timeout"] in resolv_conf
