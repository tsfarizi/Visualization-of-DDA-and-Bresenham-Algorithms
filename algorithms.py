class DDAAlgorithm:
    def compute_line(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1

        steps = int(max(abs(dx), abs(dy)))

        x_inc = dx / steps
        y_inc = dy / steps

        x = x1
        y = y1

        points = []

        for step in range(steps + 1):
            point_info = {
                'x': x,
                'y': y,
                'rounded_x': int(round(x)),
                'rounded_y': int(round(y)),
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'dx': dx,
                'dy': dy,
                'x_inc': x_inc,
                'y_inc': y_inc,
                'step': step
            }
            points.append(point_info)
            x += x_inc
            y += y_inc

        return points

class BresenhamAlgorithm:
    def compute_line(self, x1, y1, x2, y2):
        points = []
        x1 = int(round(x1))
        y1 = int(round(y1))
        x2 = int(round(x2))
        y2 = int(round(y2))

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        err = dx - dy  
        x, y = x1, y1
        step = 0  

        while True:
            point_info = {
                'x': x,
                'y': y,
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'dx': dx,
                'dy': dy,
                'err': err,
                'sx': sx,
                'sy': sy,
                'step': step
            }
            points.append(point_info)

            if x == x2 and y == y2:
                break

            e2 = 2 * err  

            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

            step += 1  

        return points
