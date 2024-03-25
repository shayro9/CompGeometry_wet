import sys
from helpers import *
import heapq


def interpret_input():

    test_num = int(sys.stdin.readline().strip('\n'))
    test_lines = []
    for i in range(test_num):
        segments_num = int(sys.stdin.readline().strip('\n'))
        segments = []
        for j in range(segments_num):
            raw_seg = [float(g) for g in sys.stdin.readline().strip('\n').split(" ")]
            p = Point(raw_seg[0], raw_seg[1])
            q = Point(raw_seg[2], raw_seg[3])
            seg = Segment(p, q)
            segments.append(seg)
        test_lines.append(segments)
    if sys.stdin.readline() != '-1\n':
        raise Exception('Invalid file format')
    return test_lines


def add_intersection(seg1, seg2, events, x):
    if seg1 and seg2:
        point = intersection(seg1, seg2)
        if point:
            new_event = Event(point.x, point.y, EventType.INTERSECTION, [seg1, seg2])
            if new_event and new_event not in events and new_event.x > x:
                heapq.heappush(events, new_event)


def handle_event(event, status, events):
    segment = event.segment
    x = event.x
    if event.type == EventType.INTERSECTION:
        index = status.swap(segment[0], segment[1], x)
        above = status.above(index + 1)
        below = status.below(index)
        add_intersection(segment[0], above, events, x)
        add_intersection(below, segment[1], events, x)
        return 1

    if event.type == EventType.START:
        index = status.insert(segment, x)
        above = status.above(index)
        below = status.below(index)
        add_intersection(segment, above, events, x)
        add_intersection(below, segment, events, x)
        return 0

    if event.type == EventType.END:
        index = status.find(segment, x)
        above = status.above(index)
        below = status.below(index)
        status.delete(segment, x)
        add_intersection(below, above, events, x)
        return 0


def count_intersections_sweep(segments):
    events = []
    counter, counter2 = 0, 0
    for segment in segments:
        events.append(Event(segment.p.x, segment.p.y, EventType.START, segment))
        events.append(Event(segment.q.x, segment.q.y, EventType.END, segment))

    heapq.heapify(events)
    status = StatusLine(events[0].x)

    while events:
        event = heapq.heappop(events)
        counter += handle_event(event, status, events)
    return counter


if __name__ == '__main__':
    tests_inputs = interpret_input()

    for t in tests_inputs:
        sys.stdout.write(str(count_intersections_sweep(t)) + "\n")
