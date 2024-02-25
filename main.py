from sys import argv

from helpers import Point, Segment


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tests_inputs = interpret_file()
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
