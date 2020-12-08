# Лабораторная работа 3. IoC/Цепочка обязанностей
# Бушный А.О. БСМО-03-20

import random

handlers = []


def server_handler(func):
    handlers.append(func)
    return func


class ServerRequire:
    # Класс с необходимыми требованиями
    def __init__(self):
        self.vcpu = 4
        self.ram = 8
        self.disktype = 'SSD'
        self.disksize = 50


class Server:
    # Класс виртуального сервера для проверки
    def __init__(self):
        self.name = None
        self.vcpu = 1
        self.ram = 1
        self.disktype = 'HDD'
        self.disksize = 50

    def reboot(self):
        print('Сервер ', self.name, ' перезагружен')


# набор проверок параметров

@server_handler
def handle_vcpu(server, reqirement):
    if server.vcpu < reqirement.vcpu:
        print("Недостаточно vcpu, необходимо:", reqirement.vcpu, " доступно:", server.vcpu)
        ans = input('Выполнить перезагрузку для добавления ресурсов? Y/n')
        if (ans == 'Y' or ans == 'y'):
            server.vcpu = reqirement.vcpu
            server.reboot()
    else:
        print("Проверка vcpu пройдена успешно")


@server_handler
def handle_ram(server, reqirement):
    if server.ram < reqirement.ram:
        print("Недостаточно RAM, необходимо:", reqirement.ram, " доступно:", server.ram)
        ans = input('Выполнить перезагрузку для добавления ресурсов? Y/n')
        if (ans == 'Y' or ans == 'y'):
            server.ram = reqirement.ram
            server.reboot()
    else:
        print("Проверка ram пройдена успешно")


@server_handler
def handle_disktype(server, reqirement):
    if str(server.disktype) != str(reqirement.disktype):
        print("Неверный тип диска, необходимо:", reqirement.disktype, " текущий:", server.disktype)
        server.disktype = reqirement.disktype
        print("Выполнена смена типа диска")

    else:
        print("Проверка типа диска пройдена успешно")


@server_handler
def handle_disksize(server, reqirement):
    if server.disksize < reqirement.disksize:
        print("Недостаточно места на диске, необходимо:", reqirement.disksize, " текущий:", server.disksize)
        server.disktsize = reqirement.disksize
        print("Выполнено увеличение объёма диска")

    else:
        print("Проверка объёма диска пройдена успешно")


# класс проверки с цепочкой обязанностей
class Checker:
    def __init__(self, handlers=[]):
        self.handlers = handlers
        self.requirement = ServerRequire()

    def add_handler(self, handler):
        self.handlers.append(handler)

    def handle_server(self, server, reqirement):
        for handler in self.handlers:
            handler(server, reqirement)


# функция генерации серверов с случайными характеристиками для демонстрации работы
def GenerateServers():
    Servers = []
    for i in range(1, 6):
        server = Server()
        server.name = 'TestServer ' + str(i)
        server.vcpu = random.randint(1, 8)
        server.ram = random.randint(1, 16)
        server.disksize = random.randint(20, 2000)
        dt = random.randint(1, 2)
        if dt == 1:
            server.disktype = 'HDD'
        else:
            server.disktype = 'SSD'
        Servers.append(server)
    return Servers


if __name__ == '__main__':
    checker = Checker(handlers)
    reqirement = ServerRequire()
    servers = GenerateServers()
    for i in servers:
        print("===Проверяем сервер: ", i.name, "===")
        print('vcpu: ', i.vcpu, ', ram: ', i.ram, ', ', str(i.disktype), ' ', i.disksize, 'GB')
        checker.handle_server(i, reqirement)
        print()
