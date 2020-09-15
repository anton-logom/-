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




class BubbleArray(SortArray):
    """массив с сортировкой пузырьком"""
    tool = bubble_sort()


class InsertionArray(SortArray):
    """массив с сортирвокй вставками"""
    tool = insertion_sort()


array1 = BubbleArray([5, 2, 1, 8, 4])

array2 = InsertionArray([9, 1, 15, 28, 6])

array3 = InsertionArray([9, 1, 15, 28, 6])

array1.sort()
print ('выполняем для массива 1 сортировку пузырьком')
print(array1.nums)

array2.sort()
print('выполняем для массива 2 сортировку вставками')
print(array2.nums)

array3.setTool(bubble_sort())
array3.sort()
print ('выполняем для массива 3 сортировку пузырьком')
print(array3.nums)

