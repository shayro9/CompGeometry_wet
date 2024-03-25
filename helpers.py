from enum import Enum

PRECISION = 5


class Point:
    x: float  # float
    y: float  # float

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # def

    def __gt__(self, other):
        if self.x == other.x:
            return self.y > other.y
        return self.x > other.x
    # def


# class

class Segment:
    id: int  # to overcome numerical error when we find a point on an ...
    #    # already-known segment we identify segments with unique ID.
    #    # binary search with numerical errors is guaranteed to find an ...
    #    # index whose distance from the correct one is O(1) (here it is 2).
    #
    p: Point  # Point, after input we compare and swap to guarantee that p.x <= q.x
    q: Point  # Point
    a: float
    b: float

    def __init__(self, p, q):
        if p.x > q.x:
            p, q = q, p
        self.p = p
        self.q = q
        self.a = (self.p.y - self.q.y) / (self.p.x - self.q.x)
        self.b = self.p.y - (self.a * self.p.x)

    # def

    # the y-coordinate of the point on the segment whose x-coordinate ..
    #   is given. Segment boundaries are NOT enforced here.
    def calc(self, x):
        return self.a * x + self.b
    # def


# class

class EventType(Enum):
    START = 0
    END = 1
    INTERSECTION = 2


class Event(Point):
    def __init__(self, x, y, event_type, segment):
        super().__init__(x, y)
        self.type = event_type
        self.segment = segment

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def is_left_turn(a, b, c):  # (Point,Point,Point) -> bool
    x1 = a.x
    x2 = b.x
    x3 = c.x
    y1 = a.y
    y2 = b.y
    y3 = c.y
    return ((x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2))) > 0


# def

def intersection(s1, s2):  # (segment,segment) -> Point | None
    if ((is_left_turn(s1.p, s1.q, s2.p) != is_left_turn(s1.p, s1.q, s2.q)) and
            (is_left_turn(s2.p, s2.q, s1.p) != is_left_turn(s2.p, s2.q, s1.q))):

        a1 = s1.a
        a2 = s2.a

        b1 = s1.b
        b2 = s2.b

        # commutation consistency: sort by a (then by b)
        if a1 > a2 or (a1 == a2 and b1 > b2):
            a1, a2 = a2, a1
            b1, b2 = b2, b1
        # if

        #
        # a1 x + b1 = y
        # a2 x + b2 = y
        # (a1 - a2)x + (b1-b2) = 0
        # x = (b2-b1)/(a1-a2)
        #

        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1

        return Point(x, y)
    else:
        return None
    # else


# def

def intersects(s1, s2):  # (Segment,Segment) -> bool
    return not (intersection(s1, s2) is None)

# def


class StatusLine:
    arr: list[Segment]
    x: int

    def __init__(self, x):
        self.arr = list()
        self.x = x

    def insert(self, item: Segment, x):
        index = self.find_insert(item, x)
        self.arr.insert(index, item)
        return index

    def find_insert(self, item: Segment, x):  # (Segment, int) -> (Segment, int)
        self.x = x
        start, end, mid = 0, len(self.arr), (len(self.arr) - 1) // 2
        while start < end:
            item_h, mid_h = item.calc(x), self.arr[mid].calc(x)
            if item_h > mid_h:
                start = mid + 1
            if item_h < mid_h:
                end = mid
            mid = (start + end) // 2
        else:
            return start

    def find(self, item: Segment, x):  # (Segment, int) -> (Segment, int)
        self.x = x
        start, end, mid = 0, len(self.arr) - 1, (len(self.arr) - 1) // 2
        while start <= end:
            item_h, mid_h = round(item.calc(x), PRECISION), round(self.arr[mid].calc(x), PRECISION)
            if item_h == mid_h:
                return mid
            if item_h > mid_h:
                start = mid + 1
            if item_h < mid_h:
                end = mid
            mid = (start + end) // 2
        return None

    def delete(self, item: Segment, x):
        search = self.find(item, x)
        if not search is None:
            self.arr.pop(search)

    def swap(self, item1: Segment, item2: Segment, x):
        index1 = self.find(item1, x)
        index2 = None

        if not index1 is None:
            if index1 == len(self.arr):
                index2 = index1 - 1
            elif index1 == 0:
                index2 = index1 + 1
            else:
                index2 = index1 + 1 if self.arr[index1 + 1] == item2 else index1 - 1
            self.arr[index1], self.arr[index2] = self.arr[index2], self.arr[index1]

            return index1 if index1 < index2 else index2
        return None

    def above(self, index):
        if index is not None and index < len(self.arr) - 1:
            return self.arr[index + 1]
        return None

    def below(self, index):
        if index is not None and index > 0:
            return self.arr[index - 1]
        return None
