import streamlit as st

# -----------------------------------------------------------------------------
# Core Calculation Logic
# -----------------------------------------------------------------------------

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI using metric units."""
    return weight_kg / (height_m ** 2)

def convert_imperial_to_metric(height_ft: float, height_in: float, weight_lb: float) -> tuple[float, float, float]:
    """
    Convert imperial height and weight to metric.
    Returns: (height_m, height_cm, weight_kg)
    """
    total_inches = (height_ft * 12) + height_in
    height_cm = total_inches * 2.54
    height_m = height_cm / 100
    weight_kg = weight_lb * 0.453592
    return height_m, height_cm, weight_kg

def get_bmi_category(bmi: float) -> str:
    """Return the adult BMI category."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25.0:
        return "Healthy weight"
    elif 25.0 <= bmi < 30.0:
        return "Overweight"
    else:
        return "Obesity"

def calculate_healthy_weight_range(height_m: float) -> tuple[float, float]:
    """Calculate the healthy weight range (BMI 18.5 to 24.9) for a given height."""
    min_weight = 18.5 * (height_m ** 2)
    max_weight = 24.9 * (height_m ** 2)
    return min_weight, max_weight

def validate_inputs(height: float, weight: float) -> list[str]:
    """Validate height and weight inputs to prevent unrealistic values or crashes."""
    errors = []
    if height <= 0:
        errors.append("Please enter a height greater than zero.")
    elif height > 300: # cm
        errors.append("Height appears to be unrealistically high.")
    
    if weight <= 0:
        errors.append("Please enter a weight greater than zero.")
    elif weight > 600: # kg
        errors.append("Weight appears to be unrealistically high.")
        
    return errors

# -----------------------------------------------------------------------------
# UI Configuration & Styling
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Professional BMI Calculator",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern healthcare look
st.markdown("""
<style>
    .result-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .bmi-value {
        font-size: 48px;
        font-weight: bold;
        color: #1f77b4;
    }
    .bmi-category {
        font-size: 24px;
        font-weight: 500;
        margin-top: -10px;
    }
    .disclaimer-text {
        font-size: 12px;
        color: #666;
        text-align: justify;
        padding-top: 20px;
        border-top: 1px solid #ddd;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# App Layout
# -----------------------------------------------------------------------------

# Sidebar
with st.sidebar:
    st.header("Settings")
    prof_mode = st.toggle("Healthcare Professional Mode", value=False, help="Enable to see calculation details, formulas, and clinical notes.")

# Header
st.title("Professional BMI Calculator")
st.markdown("Calculate and understand BMI using metric or imperial measurements.")
st.divider()

# Input Section
st.subheader("Your Information")

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age (years)", min_value=2, max_value=120, value=30, step=1)
with col2:
    sex = st.selectbox("Sex", options=["Male", "Female", "Other / Prefer not to say"])

unit_system = st.radio("Measurement System", options=["Metric (cm, kg)", "Imperial (ft, in, lb)"], horizontal=True)

input_height = 0.0
input_weight = 0.0
height_m = 0.0
weight_kg = 0.0

col3, col4 = st.columns(2)

if unit_system.startswith("Metric"):
    with col3:
        input_height = st.number_input("Height (cm)", min_value=0.0, max_value=300.0, value=170.0, step=1.0)
    with col4:
        input_weight = st.number_input("Weight (kg)", min_value=0.0, max_value=600.0, value=70.0, step=0.1)
    
    height_m = input_height / 100
    weight_kg = input_weight

else:
    with col3:
        h_col1, h_col2 = st.columns(2)
        with h_col1:
            height_ft = st.number_input("Height (ft)", min_value=0.0, max_value=10.0, value=5.0, step=1.0)
        with h_col2:
            height_in = st.number_input("Height (in)", min_value=0.0, max_value=11.9, value=7.0, step=0.1)
    with col4:
        weight_lb = st.number_input("Weight (lb)", min_value=0.0, max_value=1500.0, value=154.0, step=1.0)
    
    # Calculate for validation purposes
    height_m, input_height, weight_kg = convert_imperial_to_metric(height_ft, height_in, weight_lb)
    input_weight = weight_lb # for validation checking

# Calculate Button
if st.button("Calculate BMI", type="primary", use_container_width=True):
    
    errors = validate_inputs(input_height, weight_kg) # input_height here is either cm or total cm converted from imperial
    
    if errors:
        for error in errors:
            st.error(error)
    else:
        st.divider()
        st.subheader("Results")
        
        # Core calculations
        bmi = calculate_bmi(weight_kg, height_m)
        
        # Display logic
        if age < 18:
            st.warning("Adult BMI categories are intended for adults. For people under 18, BMI should be interpreted using age- and sex-specific growth charts by an appropriate healthcare professional.")
            st.markdown(f"""
            <div class="result-box">
                <div>Your BMI</div>
                <div class="bmi-value">{bmi:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            category = get_bmi_category(bmi)
            
            # Color coding the category
            cat_color = "#333"
            if category == "Underweight":
                cat_color = "#3498db" # Blue
            elif category == "Healthy weight":
                cat_color = "#2ecc71" # Green
            elif category == "Overweight":
                cat_color = "#f39c12" # Orange
            elif category == "Obesity":
                cat_color = "#e74c3c" # Red
                
            st.markdown(f"""
            <div class="result-box">
                <div>Your BMI</div>
                <div class="bmi-value">{bmi:.1f}</div>
                <div class="bmi-category" style="color: {cat_color};">{category}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Simple explanation for general public
            st.info(f"Your BMI is **{bmi:.1f}**, which falls in the **{category}** category. "
                    f"This is an approximate indicator of total body fat for many adults.")
            
            # Visual Scale
            st.markdown("### BMI Scale")
            st.progress(min(max((bmi - 15) / (40 - 15), 0.0), 1.0))
            cols = st.columns(4)
            cols[0].caption("Underweight (<18.5)")
            cols[1].caption("Healthy (18.5-24.9)")
            cols[2].caption("Overweight (25-29.9)")
            cols[3].caption("Obesity (≥30)")
            
            # Healthy Weight Range
            min_wt, max_wt = calculate_healthy_weight_range(height_m)
            st.success(f"**Approximate Healthy Weight Range:** {min_wt:.1f} kg – {max_wt:.1f} kg")
            st.caption("Note: This is an approximate BMI-based range, not an individualized medical target.")
            
        
        # Healthcare Professional View
        if prof_mode:
            st.divider()
            st.subheader("⚕️ Professional View")
            
            with st.expander("Calculation Details", expanded=True):
                st.markdown("**Formula:** `BMI = weight (kg) / height (m)²`")
                
                if unit_system.startswith("Imperial"):
                    st.markdown("**Entered Values:**")
                    st.markdown(f"- Height: {height_ft} ft {height_in} in")
                    st.markdown(f"- Weight: {weight_lb} lbs")
                    st.markdown("**Converted Metric Values:**")
                    st.markdown(f"- Height: {height_m:.2f} m ({input_height:.1f} cm)")
                    st.markdown(f"- Weight: {weight_kg:.2f} kg")
                else:
                    st.markdown("**Entered Values:**")
                    st.markdown(f"- Height: {height_m:.2f} m ({input_height} cm)")
                    st.markdown(f"- Weight: {weight_kg:.2f} kg")
                    
                st.markdown("**Calculation:**")
                st.markdown(f"`{weight_kg:.2f} / ({height_m:.2f}²)` = **{bmi:.2f}**")
                
            with st.expander("Clinical Limitations", expanded=False):
                st.markdown("""
                - **Body Composition:** BMI does not distinguish between muscle mass and fat mass. Highly muscular individuals may be falsely categorized as overweight/obese.
                - **Distribution:** BMI does not account for fat distribution (visceral vs. subcutaneous).
                - **Demographics:** Standard BMI thresholds may not accurately reflect metabolic risk across all ethnicities (e.g., Asian populations often face risks at lower BMI thresholds).
                - **Age:** Not applicable to pediatric patients without growth charts. Older adults may have different healthy ranges.
                """)

# -----------------------------------------------------------------------------
# Information & Disclaimers
# -----------------------------------------------------------------------------

st.divider()

with st.expander("What is BMI & How is it Calculated?"):
    st.write("""
    **Body Mass Index (BMI)** is a measure of body fat based on height and weight that applies to adult men and women.
    
    The calculation is: `weight (kg) / height (m)²`
    
    While BMI is a useful screening tool, it does not directly measure body fat or metabolic health.
    """)

st.markdown("""
<div class="disclaimer-text">
    <strong>Privacy:</strong> Your entered information is used to perform the calculation and is not intentionally stored by this application.<br><br>
    <strong>Medical Disclaimer:</strong> BMI is a screening measure and does not diagnose disease or fully describe an individual's health. BMI may be interpreted differently for certain populations and circumstances. Consult a qualified healthcare professional for personalized medical advice.
</div>
""", unsafe_allow_html=True)
