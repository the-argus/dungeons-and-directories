def aabb_collide(width_1, height_1, x1, y1, width_2, height_2, x2, y2):
    h1_div = height_1/2
    h2_div = height_2/2
    w1_div = width_1/2
    w2_div = width_2/2
    x_satisfied = ((x1 + w1_div) > (x2 - w2_div)
                   and (x1 - w1_div) < (x2 + w2_div))
    y_satisfied = ((y1 + h1_div) > (y2 - h2_div)
                   and (y1 - h1_div) < (y2 + h2_div))
    return x_satisfied and y_satisfied
