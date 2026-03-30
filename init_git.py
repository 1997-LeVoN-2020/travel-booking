#!/usr/bin/env python
"""
Скрипт для инициализации Git репозитория
"""

import os
from pathlib import Path
from git import Repo
from git.util import Actor

# Путь к проекту
project_path = Path(__file__).parent

print(f"📁 Инициализирую репозиторий в: {project_path}")

try:
    # Инициализируем репозиторий
    repo = Repo.init(project_path)
    print("✅ Репозиторий инициализирован")
    
    # Настраиваем пользователя
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", "Channel Manager")
        git_config.set_value("user", "email", "admin@channelmanager.local")
    print("✅ Конфигурация пользователя установлена")
    
    # Добавляем все файлы
    repo.index.add([item for item in repo.untracked_files])
    print(f"✅ Добавлено {len(repo.untracked_files)} файлов")
    
    # Делаем первый коммит
    repo.index.commit("Initial commit: Travel booking management system")
    print("✅ Первый коммит успешно создан")
    
    print("\n" + "="*60)
    print("✨ Репозиторий успешно создан!")
    print("="*60)
    
    print("\n📋 Следующие шаги:")
    print("1. Создайте репозиторий на GitHub: https://github.com/new")
    print("2. Назовите его 'travel-booking'")
    print("3. Выполните команду для связи с GitHub:")
    print("\n   git remote add origin https://github.com/YOUR_USERNAME/travel-booking.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
