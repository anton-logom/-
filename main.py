class SortArray(object):
    tool = None

    def __init__(self, nums):
        self.nums = nums

    def setTool(self, tool):
        self.tool = tool

    def sort(self):
        self.nums.sort()


class ToolBase:
    """
    Семейство сортировок
    """

    def sort(self, null):
        raise NotImplementedError()


class bubble_sort(ToolBase):
    """сортировка пузырьком"""
    def sort(nums):
        # We set swapped to True so the loop looks runs at least once
        swapped = True
        while swapped:
            swapped = False
            for i in range(len(nums) - 1):
                if nums[i] > nums[i + 1]:
                    # Swap the elements
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    # Set the flag to True so we'll loop again
                    swapped = True


class insertion_sort(ToolBase):
    """сортировка вставками"""
    def sort(nums):
        # Начнем со второго элемента, так как мы предполагаем, что первый элемент отсортирован
        for i in range(1, len(nums)):
            item_to_insert = nums[i]
            # И сохранить ссылку на индекс предыдущего элемента
            j = i - 1
            # Переместить все элементы отсортированного сегмента вперед, если они больше, чем элемент для вставки
            while j >= 0 and nums[j] > item_to_insert:
                nums[j + 1] = nums[j]
                j -= 1
            # Вставляем элемент
            nums[j + 1] = item_to_insert

class selection_sort(ToolBase):
    """сортирвка выбором"""
    def selection_sort(nums):
        # значение i соответствует тому, сколько значений было отсортировано
        for i in range(len(nums)):
            # Мы предполагаем, что первый элемент несортированного сегмента является наименьшим
            lowest_value_index = i
            # Этот цикл перебирает несортированные элементы
            for j in range(i + 1, len(nums)):
                if nums[j] < nums[lowest_value_index]:
                    lowest_value_index = j
            # Поменять местами значения самого низкого несортированного элемента с первым несортированным
            nums[i], nums[lowest_value_index] = nums[lowest_value_index], nums[i]


class BubbleArray(SortArray):
    """массив с сортировкой пузырьком"""
    tool = bubble_sort()


class InsertionArray(SortArray):
    """массив с сортирвокй вставками"""
    tool = insertion_sort()

class SelectionArray(SortArray):
    """массив с сортирвокй выбором"""
    tool = selection_sort()


array1 = BubbleArray([5, 2, 1, 8, 4])

array2 = SelectionArray([9, 1, 15, 28, 6])

array3 = InsertionArray([9, 1, 15, 28, 6])

array1.sort()
print ('выполняем для массива 1 сортировку пузырьком')
print(array1.nums)

array2.sort()
print('выполняем для массива 2 сортировку выбором')
print(array2.nums)

array3.setTool(bubble_sort())
array3.sort()
print ('выполняем для массива 3 сортировку пузырьком')
print(array3.nums)

