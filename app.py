import streamlit as st
import plotly.graph_objects as go
import calculate_internal_forces as cf
import section_properties_module as spm
from PIL import Image
import matplotlib.pyplot as plt

import sectionproperties.pre.library.steel_sections as steel_geom
from sectionproperties.pre.pre import Material
from sectionproperties.analysis.section import Section

# import matplotlib
# matplotlib.use("Agg")

st.set_option('deprecation.showPyplotGlobalUse', False)

# st.header("Composite Facade Beam")
# st.subheader("Structural Analysis using sectionproperties")

col1, col2 = st.columns([100,10])

with col1:
    st.header("Composite Facade Beam")
    st.subheader("Structural Analysis using sectionproperties")
with col2:
    sketch = Image.open('sketch.png')
    st.image(sketch, width=200)


## ---------------------------------------------------------
## SIDEBAR
## ---------------------------------------------------------
logo = Image.open('pfse.png')
st.sidebar.image(logo, width=50)

st.sidebar.header("Input Parameters")

fy = st.sidebar.selectbox("**Steel yield strength** (MPa)",(235, 350, 460))

#Main Beam
st.sidebar.subheader("Main Beam - Box section")
main_beam_height = st.sidebar.number_input("**Box Height** ($mm$)", value=400, min_value= 160, max_value=1000)
main_beam_width = st.sidebar.number_input("**Box Width** ($mm$)", value=200, min_value= 100, max_value=400)
main_beam_t = st.sidebar.number_input("**Box t** ($mm$)", value=10, min_value= 4, max_value=50)

# Secondary Beam
st.sidebar.subheader("Second Beam - Angle")
angle_length = st.sidebar.number_input("**Angle Length** ($mm$)", value=140, min_value= 70, max_value=260)
angle_t = st.sidebar.number_input("**Angle t** ($mm$)", value=10, min_value= 4, max_value=20)


## ---------------------------------------------------------
## Assigning User Input to Variables
## ---------------------------------------------------------
length_input = st.slider("Length of beam (m)", min_value=1.0, max_value=8.0, value=5.0, step=0.05)
pos_on_beam_input = st.slider("Position on beam (m)", min_value=0.0, max_value=length_input, value=0.0, step=0.05)

dead_load = st.number_input("**Dead Load** ($kN/m$)", value=2.0, step=0.5, min_value= 0.4, max_value=10.0)
live_load = st.number_input("**Live Load** ($kN/m$)", value=1.0, step=0.5, min_value= 0.5, max_value=10.0)
design_load = cf.calc_factored_load(dead_load, live_load)

Mxx = cf.calc_moment_shear_beam_udl(length_input, design_load, pos_on_beam_input)[1]
Vy = cf.calc_moment_shear_beam_udl(length_input, design_load, pos_on_beam_input)[0]

st.write("Design Load: ", round(design_load,1), "kN/m")
st.write("Moment: ", round(Mxx,2), "kNm")
st.write("Shear: ", round(Vy,2), "kN")


## ---------------------------------------------------------
## Using Section Properties Module
## ---------------------------------------------------------

## Somehoew it didn't work for me when using the my functions from my custom module section_properties_module
## So I made it here with using sectionproprties directly in app.py

## Using section_properties_module module 
## ---------------------------------------------------------
# box_mat1 = spm.make_steel_material(fy)
# box1 = spm.make_box_section(main_beam_height, main_beam_width, main_beam_t, 10<main_beam_t, box_mat1)

# angle_mat1 = spm.make_steel_material(fy)
# angle1 = spm.make_angle_section(angle_length, angle_t, 10 < angle_t, angle_mat1)

# composite_section1 = spm.make_composite_section(angle1, box1)

# if st.button('Calculate1'):
#     st.pyplot(composite_section1.plot_geometry().get_figure())
#     analysis_result1 = spm.perform_analysis(composite_section1, Mzz, Vy)
#     st.pyplot(analysis_result1.plot_stress_vm().get_figure())


## Using sectionproperties directly in app.py 
## ---------------------------------------------------------

if st.button('Calculate'):

    steel_mat = Material(
        f"{'{:,}'.format(fy)} MPa Steel", 
        elastic_modulus=200e3,
        poissons_ratio=0.3, 
        yield_strength=fy, 
        density=7.7,
        color="goldenrod"
    )

    box = steel_geom.rectangular_hollow_section(
        d=main_beam_height, 
        b=main_beam_width, 
        t=main_beam_t,
        r_out=main_beam_t*2, 
        n_r=8,
        material=steel_mat
    )
    # box

    angle = steel_geom.angle_section(
        d=angle_length, 
        b=angle_length,
        t=angle_t,
        r_r=angle_t/2, 
        r_t=angle_t/2, 
        n_r=8,
        material=steel_mat
    )
    # angle

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
    # st.pyplot(composite_geometry.plot_geometry().get_figure())
    # analysis_result = spm.perform_analysis(composite_geometry, Mxx*1000000, Vy*1000, 0)
    # st.pyplot(analysis_result.plot_stress_vm().get_figure())


    composite_geometry.create_mesh([20, 10])
    sec = Section(composite_geometry, time_info=True)
    sec.plot_mesh()
    sec.calculate_geometric_properties()
    sec.calculate_plastic_properties()
    sec.calculate_warping_properties()
    result = sec.calculate_stress(Vy=Vy*1000, Mxx=Mxx*1000000, Mzz=0)
    st.pyplot(result.plot_stress_vm().get_figure())



    # composite_geometry.create_mesh([20, 10])
    # sec = Section(composite_geometry, time_info=True)
    # sec.plot_mesh()
    # sec.calculate_geometric_properties()
    # sec.calculate_plastic_properties()
    # sec.calculate_warping_properties()
    # st.write("Shear centre: ", sec.get_sc())
    # st.pyplot(sec.plot_centroids().get_figure())

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

st.write("Go to [sectionproperties](https://sectionproperties.readthedocs.io/en/latest/#)")
st.write("Check out [Structural Python](https://www.structuralpython.com/)")
