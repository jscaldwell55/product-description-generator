# app.py
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Set Streamlit port for Render
os.environ['STREAMLIT_SERVER_PORT'] = os.environ.get('PORT', '8501')

# Page config
st.set_page_config(
    page_title="Jay's Product Description Generator",
    page_icon="✨",
    layout="wide"
)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_description(product_info, tone, target_length="medium"):
    """Generate product description using OpenAI API"""
    try:
        length_guide = {
            "short": "50-75 words",
            "medium": "100-150 words",
            "long": "200-250 words"
        }
        
        prompt = f"""
        Product Information: {product_info}
        
        Create a {tone} product description in {length_guide[target_length]}.
        Focus on benefits and value proposition.
        Use engaging language that resonates with potential customers.
        Maintain a {tone} tone throughout the description.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an experienced product marketing copywriter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating description: {str(e)}")
        return None

# Main UI
st.title("✨ Jay's Product Description Generator")
st.write("Transform basic product information into engaging marketing content!")

# Input sections
with st.form("product_form"):
    product_info = st.text_area(
        "Product Information",
        placeholder="Enter basic product features, specifications, and target audience...",
        height=150
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        tone = st.selectbox(
            "Select Tone",
            ["Professional", "Casual", "Luxury", "Technical", "Friendly", "Persuasive"]
        )
    
    with col2:
        length = st.selectbox(
            "Description Length",
            ["short", "medium", "long"]
        )
    
    submitted = st.form_submit_button("Generate Description")

if submitted:
    if not product_info.strip():
        st.warning("Please enter product information before generating.")
    else:
        with st.spinner("Generating description..."):
            description = generate_description(product_info, tone, length)
            if description:
                st.success("Description generated!")
                
                # Display the generated description
                st.write("### Generated Description")
                st.write(description)
                
                # Add a copy button
                st.text_area("Copy-ready version", description, height=200)
                
                # Add download button
                st.download_button(
                    label="Download Description",
                    data=description,
                    file_name=f"product_description_{tone.lower()}.txt",
                    mime="text/plain"
                )

# Add usage tips in an expander
with st.expander("💡 Tips for best results"):
    st.markdown("""
    - Include key product features and specifications
    - Mention target audience or use case
    - Specify any unique selling points
    - Include price point or value proposition
    - Mention any relevant certifications or awards
    """)

# Add sample input in an expander
with st.expander("📝 Sample Input"):
    st.markdown("""
    **Example Product Information:**
    ```
    Product: Smart Water Bottle
    Features: 
    - Temperature sensing
    - Hydration tracking
    - Mobile app integration
    - 24-hour battery life
    Price: $45
    Target: Fitness enthusiasts and health-conscious professionals
    USP: AI-powered hydration reminders based on personal habits
    ```
    """)
