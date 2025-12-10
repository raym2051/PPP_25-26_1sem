from abc import ABC, abstractmethod
from datetime import datetime
import json
import re
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass


class LogEntry(ABC):
    """Абстрактный базовый класс для лог-записей"""

    @abstractmethod
    def parse(self, log_string: str) -> bool:
        """Парсит строку лога. Возвращает True при успешном разборе"""
        pass

    @property
    @abstractmethod
    def level(self) -> str:
        """Уровень логирования (ERROR, WARNING, INFO, etc.)"""
        pass

    @property
    @abstractmethod
    def timestamp(self) -> datetime:
        """Временная метка в формате datetime"""
        pass

    @property
    @abstractmethod
    def message(self) -> str:
        """Текст сообщения"""
        pass

    def __str__(self) -> str:
        """Единый формат вывода"""
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.level} {self.message}"


#  Конкретные реализации парсеров
class Fmt1LogEntry(LogEntry):
    """Парсер для формата: [YYYY-MM-DD HH:MM:SS] LEVEL: Message"""

    def __init__(self):
        self._level = ""
        self._timestamp = datetime.min
        self._message = ""
        self._pattern = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (\w+): (.+)'

    def parse(self, log_string: str) -> bool:
        try:
            match = re.match(self._pattern, log_string)
            if not match:
                return False

            time_str, self._level, self._message = match.groups()
            self._timestamp = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            return True
        except:
            return False

    @property
    def level(self) -> str:
        return self._level

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def message(self) -> str:
        return self._message


class Fmt2LogEntry(LogEntry):
    """Парсер для формата: LEVEL;YYYY/MM/DD-HH:MM;Message"""

    def __init__(self):
        self._level = ""
        self._timestamp = datetime.min
        self._message = ""
        self._pattern = r'(\w+);(\d{4}/\d{2}/\d{2}-\d{2}:\d{2});(.+)'

    def parse(self, log_string: str) -> bool:
        try:
            match = re.match(self._pattern, log_string)
            if not match:
                return False

            self._level, time_str, self._message = match.groups()
            self._timestamp = datetime.strptime(time_str, '%Y/%m/%d-%H:%M')
            return True
        except:
            return False

    @property
    def level(self) -> str:
        return self._level

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def message(self) -> str:
        return self._message


class JsonLogEntry(LogEntry):
    """Парсер для JSON формата"""

    def __init__(self):
        self._level = ""
        self._timestamp = datetime.min
        self._message = ""

    def parse(self, log_string: str) -> bool:
        try:
            data = json.loads(log_string)
            self._level = data.get('level', '')
            self._message = data.get('msg', '') or data.get('message', '')

            time_str = data.get('time', '')
            # Пробуем разные форматы времени
            for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'):
                try:
                    self._timestamp = datetime.strptime(time_str, fmt)
                    return True
                except:
                    continue
            return False
        except:
            return False

    @property
    def level(self) -> str:
        return self._level

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def message(self) -> str:
        return self._message


class ErrorLogEntry(LogEntry):
    """Специальный класс для некорректных записей"""

    def __init__(self, log_string: str):
        self._log_string = log_string
        self._level = "ERROR"
        self._timestamp = datetime.now()
        self._message = f"Failed to parse log entry: {log_string}"

    def parse(self, log_string: str) -> bool:
        # Этот класс создается только для некорректных записей
        return True

    @property
    def level(self) -> str:
        return self._level

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def message(self) -> str:
        return self._message


# Фабрика для создания лог-записей
class LogFactory:
    """Фабрика для создания объектов лог-записей"""

    @staticmethod
    def create_log_entry(log_string: str) -> LogEntry:
        """Создает объект LogEntry из строки, определяя формат автоматически"""
        parsers = [Fmt1LogEntry(), Fmt2LogEntry(), JsonLogEntry()]

        for parser in parsers:
            if parser.parse(log_string):
                return parser

        # Если ни один парсер не сработал
        return ErrorLogEntry(log_string)


# Коллекция для хранения логов
class LogCollection:
    """Коллекция для хранения и обработки лог-записей"""

    def __init__(self):
        self.entries: List[LogEntry] = []

    def add(self, log_string: str) -> None:
        """Добавляет запись в коллекцию"""
        entry = LogFactory.create_log_entry(log_string)
        self.entries.append(entry)

    def add_multiple(self, log_strings: List[str]) -> None:
        """Добавляет несколько записей"""
        for log_str in log_strings:
            self.add(log_str)

    def filter_by_level(self, level: str) -> List[LogEntry]:
        """Фильтрует записи по уровню"""
        return [entry for entry in self.entries if entry.level.upper() == level.upper()]

    def filter_by_time_range(self, start: datetime, end: datetime) -> List[LogEntry]:
        """Фильтрует записи по временному диапазону"""
        return [entry for entry in self.entries
                if start <= entry.timestamp <= end]

    def count_by_level(self, level: Optional[str] = None) -> Dict[str, int]:
        """Подсчитывает количество записей по уровням"""
        counts = {}
        for entry in self.entries:
            lvl = entry.level
            if level is None or lvl.upper() == level.upper():
                counts[lvl] = counts.get(lvl, 0) + 1
        return counts

    def get_time_range(self) -> Tuple[Optional[datetime], Optional[datetime]]:
        """Возвращает минимальное и максимальное время в логах"""
        if not self.entries:
            return None, None

        timestamps = [entry.timestamp for entry in self.entries]
        return min(timestamps), max(timestamps)

    def get_all(self) -> List[LogEntry]:
        """Возвращает все записи"""
        return self.entries


# Обработчик команд
class LogCommandHandler:
    """Обработчик пользовательских команд"""

    def __init__(self, collection: LogCollection):
        self.collection = collection

    def execute(self, command: str) -> List[str]:
        """Выполняет команду и возвращает результат"""
        parts = command.strip().split()
        if not parts:
            return ["Empty command"]

        cmd = parts[0].lower()

        try:
            if cmd == "count":
                return self._handle_count(parts[1:])
            elif cmd == "range":
                return self._handle_range(parts[1:])
            elif cmd == "list":
                return self._handle_list(parts[1:])
            elif cmd == "stats":
                return self._handle_stats()
            elif cmd == "all":
                return self._handle_all()
            else:
                return [f"Unknown command: {cmd}"]
        except Exception as e:
            return [f"Error executing command: {str(e)}"]

    def _handle_count(self, args: List[str]) -> List[str]:
        """Обработка команды count"""
        if len(args) != 1 or not args[0].startswith("level="):
            return ["Usage: count level=LEVEL"]

        level = args[0].split('=')[1]
        count = self.collection.count_by_level(level)
        total = sum(count.values())
        return [f"Total {level} entries: {total}"]

    def _handle_range(self, args: List[str]) -> List[str]:
        """Обработка команды range"""
        if len(args) != 3:
            return ["Usage: range START_DATE START_TIME END_TIME (format: YYYY-MM-DD HH:MM HH:MM)"]

        try:
            start_date = args[0]
            start_time = args[1]
            end_time = args[2]

            start_dt = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{start_date} {end_time}", "%Y-%m-%d %H:%M")

            filtered = self.collection.filter_by_time_range(start_dt, end_dt)
            return [str(entry) for entry in filtered] or ["No entries found in specified range"]
        except ValueError:
            return ["Invalid time format. Use: YYYY-MM-DD HH:MM HH:MM"]

    def _handle_list(self, args: List[str]) -> List[str]:
        """Обработка команды list"""
        if len(args) != 1 or not args[0].startswith("level="):
            return ["Usage: list level=LEVEL"]

        level = args[0].split('=')[1]
        filtered = self.collection.filter_by_level(level)
        return [str(entry) for entry in filtered] or [f"No {level} entries found"]

    def _handle_stats(self) -> List[str]:
        """Вывод статистики"""
        counts = self.collection.count_by_level()
        start, end = self.collection.get_time_range()

        result = ["=== Log Statistics ==="]
        result.append(f"Total entries: {len(self.collection.entries)}")

        for level, count in sorted(counts.items()):
            result.append(f"{level}: {count}")

        if start and end:
            result.append(f"Time range: {start.strftime('%Y-%m-%d %H:%M:%S')} - {end.strftime('%Y-%m-%d %H:%M:%S')}")

        return result

    def _handle_all(self) -> List[str]:
        """Вывод всех записей"""
        return [str(entry) for entry in self.collection.get_all()] or ["No entries"]


# Основная программа
def main():
    """Пример использования системы"""
    collection = LogCollection()

    logs = [
        # fmt1 формат
        "[2025-10-01 12:34:56] INFO: System started",
        "[2025-10-01 12:35:01] DEBUG: Initializing components",
        "[2025-10-01 12:35:30] WARNING: High memory usage",

        # fmt2 формат
        "ERROR;2025/10/01-12:35;Disk full",
        "INFO;2025/10/01-12:36;Backup completed",

        # JSON формат
        '{"level": "WARNING", "time": "2025-10-01T12:36:00", "msg": "High load"}',
        '{"level": "INFO", "time": "2025-10-01T12:37:00", "message": "User logged in"}',

        # Некорректная запись
        "INVALID LOG FORMAT",
    ]

    collection.add_multiple(logs)

    handler = LogCommandHandler(collection)

    commands = [
        "stats",
        "count level=ERROR",
        "count level=WARNING",
        "list level=WARNING",
        "range 2025-10-01 12:30 13:00",
        "list level=INFO",
        "all"
    ]

    print("=== Log Processing System ===")
    for command in commands:
        print(f"\n> {command}")
        results = handler.execute(command)
        for result in results:
            print(result)


if __name__ == "__main__":
    main()
