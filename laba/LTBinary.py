from geom_classes import Point, Vector, Segment

def find_max_triangle(vertices):
    num_vertices = len(vertices)

    if num_vertices < 3:
        return None

    vertices.sort(key=lambda p: p[0])  # Сортування вершин за координатою x

    def divide_and_conquer(vertices):
        num_vertices = len(vertices)

        if num_vertices < 3:
            return None

        if num_vertices == 3:
            return vertices

        mid = num_vertices // 2
        left_vertices = vertices[:mid]
        right_vertices = vertices[mid:]

        left_triangle = divide_and_conquer(left_vertices)
        right_triangle = divide_and_conquer(right_vertices)

        cross_triangle = find_max_cross_triangle(vertices)

        return max(left_triangle, right_triangle, cross_triangle, key=calculate_area)

    def find_max_cross_triangle(vertices):
        num_vertices = len(vertices)
        mid = num_vertices // 2
        mid_x = vertices[mid][0]

        left_index = mid
        while left_index > 0 and vertices[left_index][0] == mid_x:
            left_index -= 1

        right_index = mid
        while right_index < num_vertices - 1 and vertices[right_index][0] == mid_x:
            right_index += 1

        left_vertices = vertices[:left_index + 1]
        right_vertices = vertices[right_index:]

        max_area = 0.0
        max_triangle = None

        for i in range(len(left_vertices)):
            p1 = left_vertices[i]

            for j in range(len(right_vertices)):
                p2 = right_vertices[j]
                segment = Segment(p1, p2)

                current_area = 0.0
                current_triangle = None

                for k in range(num_vertices):
                    if vertices[k] not in (p1, p2):
                        p = vertices[k]
                        area = segment.height(p)

                        if area > current_area:
                            current_area = area
                            current_triangle = [p1, p2, p]

                if current_area > max_area:
                    max_area = current_area
                    max_triangle = current_triangle

        return max_triangle

    def calculate_area(triangle):
        if triangle is None:
            return 0.0

        p1, p2, p3 = triangle
        segment1 = Segment(p1, p2)
        segment2 = Segment(p2, p3)

        return segment1.height(p3) / 2 + segment2.height(p1) / 2

    return divide_and_conquer(vertices)