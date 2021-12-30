import testinfra
import pytest

@pytest.fixture()
def AnsibleVars(host):
  default_vars = host.ansible("include_vars", "file=defaults/main.yml")["ansible_facts"]
  test_vars = host.ansible("include_vars", "file=molecule/default/vars.yml")["ansible_facts"]
  merged_vars = { **default_vars, **test_vars }
  return merged_vars

def test_user(host, AnsibleVars):
  users = AnsibleVars["users"]
  for user in users:
    # Если пользователь создан
    if "state" not in user or user["state"] == "present":
      # Проверяем, что пользователь существует
      assert host.user(user["login"]).exists

      # Проверяем оболочку
      system_default_shell = host.file("/etc/shells").content_string.split("\n")[1].split("/")[-1]
      user_default_shell = AnsibleVars["default_shell"]
      user_settings_shell = user["shell"] if "shell" in user else user_default_shell
      user_current_shell = host.user(user["login"]).shell.split("/")[-1]
      assert (
        user_current_shell in [
          system_default_shell,
          user_default_shell,
          user_settings_shell
        ]
      )

      # Проверяем персональные каталоги
      if "dirs" in user:
        for dir in user["dirs"]:
          dir_path = dir["dir"] if dir["dir"][0] == "/" else (host.user(user["login"]).home+"/"+dir["dir"])
          assert (
            host.file(dir_path).is_directory and
            host.file(dir_path).mode == int(dir["mode"], 8)
          )

      # Проверяем, что пароль установлен или пользователь создан без пароля
      if "passwd" in user:
        assert host.user(user["login"]).password == user["passwd"]
      else:
        assert host.user(user["login"]).password in ["!", "!!"]

      # Проверяем группы пользователя
      if "groups" in user:
        user_groups = host.user(user["login"]).groups
        for group in user["groups"]:
          assert group in user_groups

      # Проверяем публичные ключи
      if "ssh_keys" in user:
        user_keys = host.file(
          host.user(user["login"]).home+"/.ssh/authorized_keys"
        ).content_string.split("\n")
        for key in user["ssh_keys"]:
          assert key in user_keys

      # Проверяем конфиги. Чтобы не ходить наружу за ними будем проверять только inline
      if "configs" in user:
        for config in user["configs"]:
          config_path = config["dst"] if config["dst"][0] == "/" else (host.user(user["login"]).home+"/"+config["dst"])
          if "inline" in config and str(config["inline"]).lower() == "true":
            assert str.encode(config["src"]) in host.file(config_path).content

    # Если пользователь не существует
    else:
      # Проверяем, что пользователь не существует
      assert not host.user(user["login"]).exists
