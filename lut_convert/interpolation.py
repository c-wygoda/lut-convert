from numpy import empty


def interpolate_tetrahedral(to_resize, size, new_size):
    """
    taken from https://github.com/michelerenzullo/LUTify
    """
    resized = empty((new_size, new_size, new_size, 3), dtype=to_resize.dtype)
    ratio = float(size - 1.0) / float(new_size - 1.0)
    for x in range(new_size):
        for y in range(new_size):
            for z in range(new_size):
                lr = sorted((0, int(x * ratio), size - 1))[1]
                ur = sorted((0, lr + 1, size - 1))[1]
                lg = sorted((0, int(y * ratio), size - 1))[1]
                ug = sorted((0, lg + 1, size - 1))[1]
                lb = sorted((0, int(z * ratio), size - 1))[1]
                ub = sorted((0, lb + 1, size - 1))[1]
                fR = x * ratio - lr
                fG = y * ratio - lg
                fB = z * ratio - lb
                if fG >= fB >= fR:
                    resized[x, y, z] = (
                        (1 - fG) * to_resize[lr, lg, lb]
                        + (fG - fB) * to_resize[lr, ug, lb]
                        + (fB - fR) * to_resize[lr, ug, ub]
                        + fR * to_resize[ur, ug, ub]
                    )
                elif fB > fR > fG:
                    resized[x, y, z] = (
                        (1 - fB) * to_resize[lr, lg, lb]
                        + (fB - fR) * to_resize[lr, lg, ub]
                        + (fR - fG) * to_resize[ur, lg, ub]
                        + fG * to_resize[ur, ug, ub]
                    )
                elif fB > fG >= fR:
                    resized[x, y, z] = (
                        (1 - fB) * to_resize[lr, lg, lb]
                        + (fB - fG) * to_resize[lr, lg, ub]
                        + (fG - fR) * to_resize[lr, ug, ub]
                        + fR * to_resize[ur, ug, ub]
                    )
                elif fR >= fG > fB:
                    resized[x, y, z] = (
                        (1 - fR) * to_resize[lr, lg, lb]
                        + (fR - fG) * to_resize[ur, lg, lb]
                        + (fG - fB) * to_resize[ur, ug, lb]
                        + fB * to_resize[ur, ug, ub]
                    )
                elif fG > fR >= fB:
                    resized[x, y, z] = (
                        (1 - fG) * to_resize[lr, lg, lb]
                        + (fG - fR) * to_resize[lr, ug, lb]
                        + (fR - fB) * to_resize[ur, ug, lb]
                        + fB * to_resize[ur, ug, ub]
                    )
                elif fR >= fB >= fG:
                    resized[x, y, z] = (
                        (1 - fR) * to_resize[lr, lg, lb]
                        + (fR - fB) * to_resize[ur, lg, lb]
                        + (fB - fG) * to_resize[ur, lg, ub]
                        + fG * to_resize[ur, ug, ub]
                    )
    return resized
