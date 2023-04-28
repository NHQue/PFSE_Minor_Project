import streamlit as st
import plotly.graph_objects as go
import calculate_forces as cf
import section_properties_module as spm


import matplotlib
matplotlib.use("Agg")

st.header("Composite Facade Beam")
st.subheader("Structural Analysis using sectionproperties")

## ---------------------------------------------------------
## SIDEBAR
## ---------------------------------------------------------
st.sidebar.header("Input Parameters")

#Main Beam
st.sidebar.subheader("Main Beam - Box section")
main_beam_height = st.sidebar.number_input("**Box Height** ($mm$)", value=400)
main_beam_width = st.sidebar.number_input("**Box Width** ($mm$)", value=200)
main_beam_t = st.sidebar.number_input("**Box t** ($mm$)", value=10)
main_beam_fy = st.sidebar.selectbox("**Box Yield strength** (MPa)",(235, 350, 460))

# Secondary Beam
st.sidebar.subheader("Second Beam - Angle")
angle_length = st.sidebar.number_input("**Angle Length** ($mm$)", value=200)
angle_t = st.sidebar.number_input("**Angle t** ($mm$)", value=10)
angle_fy = st.sidebar.selectbox("**Angle Yield strength** (MPa)",(235, 350, 460))



## ---------------------------------------------------------
## ---------------------------------------------------------
length_input = st.slider("Length of beam (mm)", min_value=1.0, max_value=8.0, value=5.0, step=0.05)
point_on_beam_input = st.slider("Point on beam (mm)", min_value=0.0, max_value=length_input, value=0.0, step=0.05)

dead_load = st.number_input("**Dead Load** ($kN/m$)", value=2.0, step=0.1)
live_load = st.number_input("**Live Load** ($kN/m$)", value=1.0, step=0.1)
design_load = cf.calc_factored_load(dead_load, live_load)

Mzz = cf.calc_moment_shear_beam_udl(length_input, design_load, point_on_beam_input)[1]
Vy = cf.calc_moment_shear_beam_udl(length_input, design_load, point_on_beam_input)[0]

st.write("Design Load: ", round(design_load,1), "kN/m")
st.write("Moment: ", round(Mzz,2), "kNm")
st.write("Shear: ", round(Vy,2), "kN")

box_mat = spm.make_steel_material(main_beam_fy)
box = spm.make_box_section(main_beam_height, main_beam_width, main_beam_t, 10<main_beam_t, box_mat)
box

angle_mat = spm.make_steel_material(angle_fy)
angle = spm.make_angle_section(angle_length, angle_t, 10 < angle_t, angle_mat)
angle

section = spm.make_composite_section(angle, box)
section

if st.button('Calculate'):
    analysis_result = spm.perform_analysis(section, Mzz, Vy)
    analysis_result
