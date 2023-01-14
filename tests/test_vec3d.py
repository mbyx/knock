import math

from attrs import astuple

from knock.depict.vec3d import Size, Vec3D, deg2rad, rad2deg


def test_deg2rad() -> None:
    assert deg2rad(180.0) == math.pi
    assert deg2rad(-90.0) == -math.pi / 2


def test_rad2deg() -> None:
    assert rad2deg(math.pi) == 180.0
    assert rad2deg(-math.pi / 2) == -90.0


def test_deg2rad_and_rad2deg_cancel_each_other() -> None:
    assert rad2deg(deg2rad(45.0)) == 45.0
    assert rad2deg(deg2rad(-45.0)) == -45.0


def test_init_with_mixed_args() -> None:
    vec = Vec3D(2.0, 3, 4.5)
    assert astuple(vec) == (2.0, 3, 4.5)


def test_vec3d_origin_returns_origin_vector() -> None:
    origin: Vec3D = Vec3D.origin()
    assert astuple(origin) == (0, 0, 0)


def test_vec3d_scalar() -> None:
    assert Vec3D.scalar(10.0) == Vec3D(10.0, 10.0, 10.0)


def test_vec3d_angle2d() -> None:
    assert rad2deg(Vec3D(1.0, 1.0, 0.0).angle_2d()) == 45.0
    assert rad2deg(Vec3D(-1.0, -1.0, 0.0).angle_2d()) == -135.0


def test_vec3d_size() -> None:
    assert Vec3D(3, 4, 0).size() == 5.0
    assert Vec3D(3, -4, 0).size() == 5.0


def test_size_of_unit_vector_is_one() -> None:
    assert Vec3D(4, 5, 6).normalize().size() == 1.0


def test_normalizing_vector_with_size_zero() -> None:
    assert Vec3D.origin().normalize() == Vec3D.origin()


def test_normalize_keeps_angle() -> None:
    vec: Vec3D = Vec3D(4, 5, 0)
    assert vec.angle_2d() == vec.normalize().angle_2d()


def test_vec3d_dot_product() -> None:
    v1: Vec3D = Vec3D(4, 5, 0)
    v2: Vec3D = Vec3D(4, 5, 6)
    assert v1.dot(v2) == 41


def test_vec3d_dot_product_is_commutative() -> None:
    v1: Vec3D = Vec3D(4, 5, 0)
    v2: Vec3D = Vec3D(4, 5, 6)
    assert v1.dot(v2) == v2.dot(v1)


def test_vec3d_cross_product_is_anti_commutative() -> None:
    v1: Vec3D = Vec3D(4, 5, 0)
    v2: Vec3D = Vec3D(4, 5, 6)
    assert v1.cross(v2) == -1 * v2.cross(v1)


def test_vec3d_constrain_size() -> None:
    assert math.isclose(Vec3D(4.0, 3.0, 0.0).constrain_size(6.0, 10.0).size(), 6.0)
    assert math.isclose(Vec3D(12.0, 5.0, 0.0).constrain_size(6.0, 10.0).size(), 10.0)


def test_vec3d_constrain() -> None:
    screen_bounds = (Vec3D(0, 0, 0), Vec3D(640, 360, 0))
    assert Vec3D(4, 5, 0).constrain(*screen_bounds) == Vec3D(4, 5, 0)


def test_vec3d_arithmetic() -> None:
    v1: Vec3D = Vec3D(4, 5, 0)
    v2: Vec3D = Vec3D(3, 6, 1)
    # __*__ methods.
    assert v1 + v2 == Vec3D(7, 11, 1)
    assert v1 - v2 == Vec3D(1, -1, -1)
    assert v1 * 2 == Vec3D(8, 10, 0)
    assert v1 / 2 == Vec3D(2.0, 2.5, 0.0)
    # __r*__ method.
    assert 2 * v1 == Vec3D(8, 10, 0)


def test_size_width_and_height_accessors() -> None:
    window: Size = Size(640, 360)
    assert window.width == 640
    assert window.height == 360


def test_size_width_and_height_setters() -> None:
    window: Size = Size(640, 360)
    window.width = 1280
    window.height = 720
    assert window.width == 1280
    assert window.height == 720
