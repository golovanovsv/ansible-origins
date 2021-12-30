# Ansible role: ansible-origins

Роль для базовой настройки сервера.

Параметры по-умолчанию находятяся в [defaults](defaults/main.yml).

## Ограничения

Роль работает только со следующими дистрибутивами Linux:

- Debian Stretch/Buster/Bullseye
- Ubuntu 18/20
- Amazon linux 2

## Выполняемые задачи

- Установка ПО [software.yml](tasks/software.yml) (tag: soft)
- Настройка sudoers [sudoers.yml](tasks/sudoers.yml) (tag: sudoers)
- Создание и настройка пользователей [main.yml](tasks/main.yml#lines-5) (tag: users)
- Настройка motd [main.yml](tasks/main.yml#lines-49) (tag: motd)
- Настройка hostname [hostname.yml](tasks/hostname.yml) (tag: hostname)
- Настройка timezone [timezone.yml](tasks/timezone.yml) (tag: timezone)
- Настройка DNS [resolv.yml](tasks/resolv.yml) (tag: dns)
- Настройка sysctl [sysctl.yml](tasks/sysctl.yml) (tag: sysctl)
- Настройка locale [locales.yml](tasks/locales.yml) (tag: locales)
- Дополнительных конфигурационных файлов [extra_configs.yml](tasks/extra_configs.yml) (tag: extra_configs)
- Настройка node-exporter`а [host.yml](tasks/monitoring/host.yml) (tag: monitoring)
