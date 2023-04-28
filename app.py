import streamlit as st
import plotly.graph_objects as go
import calculate_forces as cf
import section_properties_module as spm
from PIL import Image


import matplotlib
matplotlib.use("Agg")

st.set_option('deprecation.showPyplotGlobalUse', False)


st.header("Composite Facade Beam")
st.subheader("Structural Analysis using sectionproperties")

## ---------------------------------------------------------
## SIDEBAR
## ---------------------------------------------------------
image = Image.open('pfse.png')
st.sidebar.image(image, width=50)

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
## ---------------------------------------------------------
length_input = st.slider("Length of beam (m)", min_value=1.0, max_value=8.0, value=5.0, step=0.05)
pos_on_beam_input = st.slider("Position on beam (m)", min_value=0.0, max_value=length_input, value=0.0, step=0.05)

dead_load = st.number_input("**Dead Load** ($kN/m$)", value=2.0, step=0.1, min_value= 0.4, max_value=10.0)
live_load = st.number_input("**Live Load** ($kN/m$)", value=1.0, step=0.1, min_value= 0.5, max_value=10.0)
design_load = cf.calc_factored_load(dead_load, live_load)

Mzz = cf.calc_moment_shear_beam_udl(length_input, design_load, pos_on_beam_input)[1]
Vy = cf.calc_moment_shear_beam_udl(length_input, design_load, pos_on_beam_input)[0]

st.write("Design Load: ", round(design_load,1), "kN/m")
st.write("Moment: ", round(Mzz,2), "kNm")
st.write("Shear: ", round(Vy,2), "kN")

box_mat = spm.make_steel_material(fy)
box = spm.make_box_section(main_beam_height, main_beam_width, main_beam_t, 10<main_beam_t, box_mat)
box

angle_mat = spm.make_steel_material(fy)
angle = spm.make_angle_section(angle_length, angle_t, 10 < angle_t, angle_mat)
angle

section = spm.make_composite_section(angle, box)
section

import matplotlib.pyplot as plt


if st.button('Calculate'):
    analysis_result = spm.perform_analysis(section, Mzz, Vy)
    st.write(analysis_result)
    fig = analysis_result.plot_stress_vm()
    fig.savefig('image.png')
    st.pyplot(fig)




