from abc import ABCMeta, abstractmethod

class Observer(metaclass=ABCMeta):
    """наблюдатель"""

    @abstractmethod
    def update(self, message: str) -> None:
        """
        Получение нового сообщения
        """
        pass

class Iterator(metaclass=ABCMeta):
    """
    Абстрактный итератор
    """
    _error = None   # класс ошибки, которая прокидывается в случае выхода за границы коллекции

    def __init__(self, collection, cursor):

        self._collection = collection  # коллекция, по которой производится проход итератором
        self._cursor = cursor  # изначальное положение курсора в коллекции (ключ)

    @abstractmethod
    def current(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def remove(self):
        pass

    def _raise_key_exception(self):
        # ошибка, связанную с невалидным индексом, содержащимся в курсоре
        raise self._error('Коллекция  {} does not have key "{}"'.format(
            self.__class__.__name__, self._cursor))

class Collection(metaclass=ABCMeta):
    """
    Абстрактная коллекция
    """

    @abstractmethod
    def iterator(self):
        pass

class DictIterator(Iterator):
    """
    Итератор, проходящий по словарю
    """

    _error = KeyError

    def __init__(self, collection: dict):
        super().__init__(collection, next(iter(collection)))
        self._keys = list(self._collection.keys())
        self._keys.pop(0)

    def current(self):
        if self._cursor in self._collection:
            return self._collection[self._cursor]
        self._raise_key_exception()

    def next(self):
        if len(self._keys):
            self._cursor = self._keys.pop(0)
            return self._collection[self._cursor]
        else:
            self._raise_key_exception()

    def has_next(self):
        return len(self._keys) > 0

    def remove(self):
        if self._cursor in self._collection:
            del self._collection[self._cursor]
            try:
                self.next()
            except self._error:
                raise KeyError('Коллекция {} пустая'.format(self.__class__.__name__))
        else:
            self._raise_key_exception()

class DictCollection(Collection):
    """
    Коллекция-обертка для словаря
    """
    def __init__(self, collection: dict):
        self._collection = collection

    def iterator(self):
        return DictIterator(self._collection)


class Observable(metaclass=ABCMeta):
    """
    Абстрактный наблюдаемый
    """

    def __init__(self) -> None:
        self.observers = []

    def register(self, observer: Observer) -> None:
        """Регистрация нового наблюдателя на подписку """
        self.observers.append(observer)

    def notify_observers(self, message: str) -> None:
        #Передача сообщения всем подписчикам

        for observer in self.observers:
            observer.update(message)


class MailingList(Observable):

    def add_news(self, news: str) -> None:
        #выпуск новой рассылки
        self.notify_observers(news)


class email(Observer):
    def __init__(self, email: str) -> None:
        self.email = email

    def update(self, message: str) -> None:
        #обновление почты получение новых писем

        print(f'{self.email} отправлено сообщение {message}')


if __name__ == '__main__':

    #коллекция всех рассылок
    collection = DictCollection({1: 'информация о скидках',
                                 2: 'информация о новых продуктах',
                                 3: 'распродажа на алиэкспресс',
                                 4: 'список продуктов с кэшбеком'})
    iterator = collection.iterator()

    # emailы пользователей
    email1 = email('anton@mail.ru')
    email2 = email('em2@mail.ru')
    email3 = email('em3@mail.ru')
    email4 = email('em4@mail.ru')

    # экземпляры рассылок
    mailing1 = MailingList()
    mailing2 = MailingList()

    # добавляем емэйлы в экземпляры рассылок
    mailing1.register(email1)
    mailing1.register(email2)

    mailing2.register(email1)
    mailing2.register(email3)
    mailing2.register(email4)

    print('Текущая рассылка: '+iterator.current())
    mailing1.add_news(iterator.current())

    iterator.next()
    print()
    print('Текущая рассылка: '+iterator.next()+' неактуальна, удаляем')
    iterator.remove()
    print()
    print('Текущая рассылка: '+iterator.current())
    mailing2.add_news(iterator.current())
    print(iterator.has_next())
    print()


