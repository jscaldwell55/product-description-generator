import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from openai import OpenAI
import httpx

# Custom client configuration
timeout = httpx.Timeout(10.0, read=30.0)
client = OpenAI(
    http_client=httpx.Client(
        timeout=timeout,
        transport=httpx.HTTPTransport(retries=3)
    )
)

# Page config (This should come before other Streamlit operations)
st.set_page_config(
    page_title="Render AI Content Generator",
    page_icon="⚡",
    layout="wide"
)

# Define customer segments and personas
SEGMENTS = {
    "Freelancers": {
        "focus": "Independent developers and designers looking for a no-code solution to build web applications",
        "personas": ["Solo Developer", "Freelance Designer"],
        "specific_needs": "Ease of use, visual editor, backend-agnostic deployment"
    },
    "Startups": {
        "focus": "Early-stage companies building scalable applications quickly",
        "personas": ["Technical Founder", "Product Manager"],
        "specific_needs": "Rapid prototyping, collaboration tools, cost-effective scaling"
    },
    "Enterprises": {
        "focus": "Large businesses seeking robust tools for internal or customer-facing web apps",
        "personas": ["IT Manager", "Solution Architect"],
        "specific_needs": "Integration with existing systems, security, and scalability"
    }
}

CONTENT_TYPES = {
    "Product Description": {
        "focus": "Highlight features of Render's no-code platform",
        "length": "medium",
        "style": "Professional and informative"
    },
    "Landing Page": {
        "focus": "Showcase Render's value for developers and startups",
        "length": "medium",
        "style": "Compelling and value-driven"
    },
    "Case Study": {
        "focus": "Problem-solution narrative",
        "length": "long",
        "style": "Detailed and results-focused"
    },
    "Email Campaign": {
        "focus": "Conversion and action",
        "length": "medium",
        "style": "Persuasive and personal"
    },
    "Blog Post": {
        "focus": "Thought leadership and education",
        "length": "long",
        "style": "Informative and engaging"
    }
}

def generate_content(feature, segment, persona, content_type, tone):
    """Generate Render-specific content using OpenAI API"""
    try:
        segment_info = SEGMENTS[segment]
        content_info = CONTENT_TYPES[content_type]

        if persona == "No Persona":
            prompt = f"""
            Generate {content_type} content for Render's feature: {feature}

            Target Audience:
            - Segment: {segment} (Focus: {segment_info['focus']})
            - Specific Needs: {segment_info['specific_needs']}

            Content Requirements:
            - Type: {content_type}
            - Focus: {content_info['focus']}
            - Style: {content_info['style']}
            - Tone: {tone}

            Additional Requirements:
            1. Address key pain points for {segment} segment
            2. Include relevant use cases
            3. Emphasize Render's no-code platform value proposition
            4. Include appropriate call-to-action for {content_type}

            Make the content compelling and focused on how Render simplifies web app creation.
            """
        else:
            prompt = f"""
            Generate {content_type} content for Render's feature: {feature}

            Target Audience:
            - Segment: {segment} (Focus: {segment_info['focus']})
            - Specific Persona: {persona}
            - Specific Needs: {segment_info['specific_needs']}

            Content Requirements:
            - Type: {content_type}
            - Focus: {content_info['focus']}
            - Style: {content_info['style']}
            - Tone: {tone}

            Additional Requirements:
            1. Highlight benefits specific to this {persona}'s needs
            2. Address key pain points for {segment} segment
            3. Include relevant use cases
            4. Emphasize Render's no-code platform value proposition
            5. Include appropriate call-to-action for {content_type}

            Make the content compelling and focused on how Render simplifies web app creation.
            """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an experienced B2B SaaS marketing copywriter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None


# Main UI
st.title("Render Content Generator")
st.write("Generate targeted marketing content for Render's no-code platform across different segments and formats.")

# Input sections
with st.form("content_form"):
    feature = st.text_area(
        "Feature/Capability",
        placeholder="Describe the Render feature or capability you want to promote...",
        height=100
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        segment = st.selectbox("Select Customer Segment", list(SEGMENTS.keys()))
    with col2:
        selected_personas = ["No Persona"] + SEGMENTS[segment]["personas"]
        persona = st.selectbox("Select Specific Persona", selected_personas)
    with col3:
        content_type = st.selectbox("Select Content Type", list(CONTENT_TYPES.keys()))

    tone = st.selectbox(
        "Select Tone",
        ["Professional", "Technical", "Conversational", "Educational", "Persuasive", "Innovative"]
    )

    submitted = st.form_submit_button("Generate Content")

if submitted:
    if not feature.strip():
        st.warning("Please enter a feature before generating.")
    else:
        with st.spinner("Generating content..."):
            content = generate_content(feature, segment, persona, content_type, tone)
            if content:
                st.success("Content generated!")
                st.write(f"### Generated {content_type}")
                st.write(content)
                st.text_area("Copy-ready version", content, height=200)
                st.download_button(
                    label="Download Content",
                    data=content,
                    file_name=f"render_{segment}_{content_type}_{tone.lower()}.txt",
                    mime="text/plain"
                )

# Tips and Examples in Expanders
with st.expander("💡 Tips for Best Results"):
    st.markdown("""
    ### Writing Effective Feature Descriptions
    - Focus on ease of use, scalability, and integration.
    - Highlight differentiators from competitors.
    - Mention specific problems solved.

    ### Segment-Specific Considerations
    - **Freelancers**: Highlight ease of use and rapid deployment.
    - **Startups**: Emphasize prototyping and scaling capabilities.
    - **Enterprises**: Focus on security and seamless integration.

    ### Content Type Guidelines
    - **Product Description**: Technical details and benefits.
    - **Landing Pages**: Clear value proposition and benefits.
    - **Case Studies**: Problem-solution format with results.
    - **Email Campaigns**: Personalized and action-oriented.
    - **Blog Posts**: In-depth analysis and thought leadership.
    """)

with st.expander("📝 Sample Inputs"):
    st.markdown("""
    ### Sample Feature Descriptions
    - **Rapid Prototyping**: Build, test, and iterate web apps in hours, not days.
    - **Backend-Agnostic Deployment**: Integrate with any backend seamlessly.
    - **Collaboration Tools**: Enable real-time collaboration across teams.
    """)