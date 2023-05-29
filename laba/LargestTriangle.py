from geom_classes import Point, Vector, Segment
import numpy as np
import Grehem

def largestTriangle(vertices):
    max_area = 0.0
    max_triangle = None

    # Перебираємо всі можливі трійки точок з опуклої оболонки
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            for k in range(j + 1, len(vertices)):
                point1 = vertices[i]
                point2 = vertices[j]
                point3 = vertices[k]

                # Обчислюємо площу трикутника, застосовуючи формулу Герона
                side1 = Vector(point1, point2).norm()
                side2 = Vector(point2, point3).norm()
                side3 = Vector(point3, point1).norm()

                s = (side1 + side2 + side3) / 2
                area = np.sqrt(s * (s - side1) * (s - side2) * (s - side3))

                # Перевіряємо, чи ця площа є максимальною
                if area > max_area:
                    max_area = area
                    max_triangle = (point1, point2, point3)

    return max_triangle
