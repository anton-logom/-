# Лабораторная работа 4. Абстрактная фабрика и Строитель
# Бушный А.О. БСМО-03-20

class VirtualDisk:
    # Абстрактный виртуальный диск
    type = ''
    size = 1
    iops = 1


class DiskCreator:
    def __init__(self):
        self.disk = VirtualDisk()
        self.disksize = int(input("введите объём диска в GB: "))


class HddDisk(DiskCreator):
    def set_type(self):
        self.disk.type = 'HDD'

    def set_params(self):
        self.disk.size = self.disksize
        self.disk.iops = 500


class SsdDisk(DiskCreator):
    def set_type(self):
        self.disk.type = 'SSD'

    def set_params(self):
        self.disk.size = self.disksize
        self.disk.iops = self.disksize * 10



class DiskBuilder:
    __builder = ''

    def set_disk(self, builder):
        self.__builder = builder

    def create_disk(self):
        self.__builder.set_type()
        self.__builder.set_params()

    def get_disk(self):
        return self.__builder.disk


class VirtualServer:
    # Абстрактный виртуальный сервер
    cpu_cores = 1
    ram_size = 1
    operating_system = ''
    programs = ''
    disk = VirtualDisk()


class ServerCreator:
    def __init__(self):
        self.server = VirtualServer()
        self.disk = DiskBuilder()


class DBServer(ServerCreator):
    # Шаблон сервера баз данных с SSD диском
    def set_hardware(self):
        self.server.cpu_cores = 1
        self.server.ram_size = 4
        self.disk.set_disk(SsdDisk())
        self.disk.create_disk()
        self.server.disk = self.disk.get_disk()

    def set_software(self):
        self.server.operating_system = 'Linux'
        self.server.programs = ['mariadb', 'mongodb']


class FileServer(ServerCreator):
    # шаблон файлового сервера с HDD диском
    def set_hardware(self):
        self.server.cpu_cores = 2
        self.server.ram_size = 8
        self.disk.set_disk(HddDisk())
        self.disk.create_disk()
        self.server.disk = self.disk.get_disk()

    def set_software(self):
        self.server.operating_system = 'Windows'
        self.server.programs = ['IIS']


class ServerBuilder:
    __builder = ''

    def set_server(self, builder):
        self.__builder = builder

    def create_server(self):
        self.__builder.__init__()
        self.__builder.set_hardware()
        self.__builder.set_software()

    def get_server(self):
        return self.__builder.server



if __name__ == '__main__':

    # инициализируем два сервера
    dbsrv1 = DBServer()
    filesrv1 = FileServer()

    # инициализируем фабрику
    cloud = ServerBuilder()

    # создаем сервер БД
    print ('==инициализируем 1-й сервер==')
    cloud.set_server(dbsrv1)
    cloud.create_server()

    # печатем параметры сервера и диска
    srvinfo = cloud.get_server()
    print('ядер CPU: ', srvinfo.cpu_cores)
    print('объём RAM: ', srvinfo.ram_size)
    print('ОС и ПО: ', srvinfo.operating_system, srvinfo.programs)
    print('Характеристики диска: ', srvinfo.disk.type, ', ', srvinfo.disk.size, 'Gb ', srvinfo.disk.iops, ' iops')
    print()

    # создаем файловый сервер
    print('==инициализируем 2-й сервер==')
    cloud.set_server(filesrv1)
    cloud.create_server()

    # печатем параметры сервера и диска
    srvinfo = cloud.get_server()
    print('ядер CPU: ', srvinfo.cpu_cores)
    print('объём RAM: ', srvinfo.ram_size)
    print('ОС и ПО: ', srvinfo.operating_system, srvinfo.programs)
    print('Характеристики диска: ', srvinfo.disk.type, ', ', srvinfo.disk.size, 'Gb ', srvinfo.disk.iops, ' iops')
