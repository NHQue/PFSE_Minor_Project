import sectionproperties.pre.library.steel_sections as steel_geom
from sectionproperties.pre.pre import Material
from sectionproperties.analysis.section import Section

def make_steel_material(yield_strength):
    steel = Material(
        f"{'{:,}'.format(yield_strength)} MPa Steel",
        elastic_modulus=210e3,
        poissons_ratio=0.3, 
        yield_strength=yield_strength, 
        density=7.81,
        color="teal"
    )
    return steel

def make_box_section(d, b, t, r_out, material):
    box = steel_geom.rectangular_hollow_section(
        d=d, 
        b=b, 
        t=t, 
        r_out=t*2, 
        n_r=8,
        material=material
    )
    return box

def make_angle_section(l, t, r_out, material):
    angle = steel_geom.angle_section(
        d=l, 
        b=l, 
        t=t,
        r_r=t/2, 
        r_t=t/2, 
        n_r=9,
        material=material
    )
    return angle


def make_composite_section(angle, box):
    mirrored_angle = (
        angle
        .mirror_section(axis='y')
        .mirror_section(axis='x')
        .align_to(box, on="top", inner=True)
        .align_to(box, on='left')
        .shift_section(y_offset=-0)        
    )

    composite_geometry = mirrored_angle + box
    composite_geometry = ((box - mirrored_angle) + mirrored_angle)
    composite_geometry = composite_geometry.align_center()

    return composite_geometry


def perform_analysis(composite_geometry, Vy, Mxx, Mzz):

    composite_geometry.create_mesh([20, 10])
    sec = Section(composite_geometry, time_info=True)
    sec.plot_mesh()
    sec.calculate_geometric_properties()
    sec.calculate_plastic_properties()
    sec.calculate_warping_properties()
    result = sec.calculate_stress(Vy=Vy, Mxx=Mxx, Mzz=Mzz)

    return result


