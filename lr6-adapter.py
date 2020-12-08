# Лабораторная работа 6.  Адаптер + Посредник ИЛИ Заместитель +Компоновщик.
# Бушный А.О. БСМО-03-20

from abc import ABCMeta, abstractmethod
from weakref import proxy
import inspect


class Mediator(metaclass=ABCMeta):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


# абстрактный сервер
class Server(metaclass=ABCMeta):
    def __init__(self, mediator: Mediator) -> None:
        # канал мониторинга
        self._mediator = proxy(mediator)

    @abstractmethod
    def send(self, message: str) -> None:
        # отправка запроса проверки
        pass

    @abstractmethod
    def receive(self, message: str) -> None:
        # получение ответа
        pass


# канал связи
class Channel(Mediator):
    def __init__(self) -> None:
        self._monserver = None
        self._monclient = None

    def set_monserver(self, monserver: Server) -> None:
        self._monserver = monserver

    def set_monclient(self, monclient: Server) -> None:
        self._monclient = monclient

    def send(self, message: str) -> None:
        sender = inspect.currentframe().f_back.f_locals['self']
        if sender == self._monclient:
            receiver = self._monserver
        else:
            receiver = self._monclient
        receiver.receive(message)


class ICMP_Check:
    def create_icmp_check(self):
        return 'ICMP запрос'


class SNMP_Check:
    def create_snmp_check(self):
        return 'SNMP запрос'


class SourceICMP(ICMP_Check):
    def generate_message(self):
        return self.create_icmp_check()


class SourceSNMP(SNMP_Check):
    def generate_message(self):
        return self.create_snmp_check()


class MonitoringRequest:
    def __init__(self, source):
        self.source = source

    def generate_message(self):
        return self.source.generate_message()


class Monitoring(Server):

    def send(self, message: str) -> None:
        self._mediator.send(message)

    def receive(self, message: str) -> None:
        print('MON: Получен ответ от сервера ', message)


class ImportantServer(Server):
    def send(self, message: str) -> None:
        self._mediator.send(message)

    def receive(self, message: str) -> None:
        print('CLI: Получен запрос от мониторинга: ', message)
        self.send('Available: ' + message)


if __name__ == '__main__':
    # создаем каналы связи
    channel1 = Channel()
    channel2 = Channel()

    # инициализируем проверки
    icmp = SourceICMP()
    snmp = SourceSNMP()

    # подключаем в канал сервер мониторинга
    MonitoringServer = Monitoring(channel1)

    # создаем проверяемый сервер 1, проверку для него и подключаем в канал
    Server1 = ImportantServer(channel1)
    Check1 = MonitoringRequest(icmp)
    channel1.set_monserver(MonitoringServer)
    channel1.set_monclient(Server1)

    # создаем проверяемый сервер 2, проверку для него и подключаем в канал
    Server2 = ImportantServer(channel2)
    Check2 = MonitoringRequest(snmp)
    channel2.set_monserver(MonitoringServer)
    channel2.set_monclient(Server2)

    # проверяем доступность сервера 1 его проверкой
    MonitoringServer.send(Check1.generate_message())

    # меняем канал и проверяем доступность сервера 2 его проверкой
    MonitoringServer = Monitoring(channel2)
    MonitoringServer.send(Check2.generate_message())
