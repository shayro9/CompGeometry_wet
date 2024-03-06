from sys import argv
from helpers import *
from enum import Enum
import heapq
from sortedcontainers import SortedList


class EventType(Enum):
    START = 0
    END = 1
    INTERSECTION = 2


class Event(Point):
    def __init__(self, x, y, event_type, segment):
        super().__init__(x, y)
        self.type = event_type
        self.segment = segment


def interpret_file():
    file = argv[1]
    with open(file) as f:
        test_num = int(f.readline().strip('\n'))
        test_lines = []
        for i in range(test_num):
            segments_num = int(f.readline().strip('\n'))
            segments = []
            for j in range(segments_num):
                raw_seg = [float(g) for g in f.readline().strip('\n').split(" ")]
                p = Point(raw_seg[0], raw_seg[1])
                q = Point(raw_seg[2], raw_seg[3])
                segments.append(Segment(p, q))
            test_lines.append(segments)
        if f.readline() != '-1\n':
            raise Exception('Invalid file format')
    return test_lines


def handle_event(event, status, events):
    segment = event.segment
    x = event.x
    if event.type == EventType.START:
        index = status.insert(segment, x)
        above = status.above(index)
        below = status.below(index)

        if above:
            point = intersection(segment, above)
            new_event = Event(point.x, point.y, EventType.INTERSECTION, [above, segment])
            if new_event:
                heapq.heappush(events, new_event)
        if below:
            point = intersection(segment, below)
            new_event = Event(point.x, point.y, EventType.INTERSECTION, [below, segment])
            if new_event:
                heapq.heappush(events, new_event)
        return 0

    if event.type == EventType.INTERSECTION:
        status.swap(segment[0], segment[1], x)
        return 1
    if event.type == EventType.END:
        pass
    return 0


def count_intersections_sweep(segments):
    events = []
    counter = 0
    for segment in segments:
        events.append(Event(segment.p.x, segment.p.y, EventType.START, segment))
        events.append(Event(segment.q.x, segment.q.y, EventType.END, segment))

    heapq.heapify(events)
    status = StatusLine(events[0].x)

    while events:
        event = heapq.heappop(events)
        counter += handle_event(event, status, events)

    print(counter)


if __name__ == '__main__':
    tests_inputs = interpret_file()
    count_intersections_sweep(tests_inputs[0])

    pass
