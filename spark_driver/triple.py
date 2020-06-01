from typing import List
# import logging as LOGGER


class Triple:
    def __init__(self, head: str, tail: str, relation: str):
        self.head = head
        self.tail = tail
        self.relation = relation

    @staticmethod
    def map_from_list(data: List[str]):
        if len(data) != 3:
            print("LENGTH TRIPLE DOES NOT EQUAL 3")
        else:
            return Triple(data[0], data[1], data[2])
    
    def __str__(self):
        self.__str__ = f"Triple(head={self.head}, relation={self.relation}, tail={self.tail})"



    