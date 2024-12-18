import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Set Streamlit port for Render
os.environ['STREAMLIT_SERVER_PORT'] = os.environ.get('PORT', '8501')

# Page config
st.set_page_config(
    page_title="Vapi AI Content Generator",
    page_icon="🎙️",
    layout="wide"
)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define customer segments and personas
SEGMENTS = {
    "Enterprise Businesses": {
        "focus": "Large companies seeking voice AI for customer support and call center enhancement",
        "personas": [
            "Innovation-Driven CTO",
            "IT Director",
            "Customer Experience Leader",
            "Operations Manager"
        ],
        "specific_needs": "Scalability, enterprise integration, security, compliance"
    },
    "SMBs": {
        "focus": "Small/medium businesses automating customer interactions",
        "personas": [
            "Business Owner",
            "Operations Manager",
            "Marketing Manager",
            "Customer Service Lead"
        ],
        "specific_needs": "Cost-effective solutions, easy integration, minimal setup"
    },
    "Developers/Tech Startups": {
        "focus": "Building applications with voice capabilities",
        "personas": [
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
            "Mobile App Developer",
            "API Integration Specialist",
            "Machine Learning Engineer",
            "Technical Architect",
            "DevOps Engineer",
            "Technical Founder",
            "Product Manager",
            "Developer"
        ],
        "specific_needs": "API access, documentation, flexible integration, SDKs, sample code"
    },
    "Call Centers": {
        "focus": "Voice AI automation and enhancement for customer service operations",
        "personas": [
            "Call Center Director",
            "Customer Service Operations Manager",
            "Quality Assurance Manager",
            "Workforce Optimization Manager",
            "Training and Development Lead"
        ],
        "specific_needs": "Agent augmentation, call analytics, quality monitoring, training tools"
    },
    "Education Platforms": {
        "focus": "Voice-based learning and tutoring capabilities",
        "personas": [
            "E-Learning Platform Designer",
            "EdTech Product Manager",
            "Learning Experience Director",
            "Educational Content Manager"
        ],
        "specific_needs": "Language support, learning engagement, accessibility"
    }
}

CONTENT_TYPES = {
    "Product Description": {
        "focus": "Technical capabilities and benefits",
        "length": "medium",
        "style": "Professional and informative"
    },
    "Social Media Post": {
        "focus": "Engagement and virality",
        "length": "short",
        "style": "Conversational and exciting"
    },
    "Blog Post": {
        "focus": "Thought leadership and education",
        "length": "long",
        "style": "Informative and engaging"
    },
    "Email Campaign": {
        "focus": "Conversion and action",
        "length": "medium",
        "style": "Persuasive and personal"
    },
    "Case Study": {
        "focus": "Problem-solution narrative",
        "length": "long",
        "style": "Detailed and results-focused"
    },
    "Landing Page": {
        "focus": "Conversion and value proposition",
        "length": "medium",
        "style": "Compelling and benefit-focused"
    }
}

def generate_content(feature, segment, persona, content_type, tone):
    """Generate Vapi-specific content using OpenAI API"""
    try:
        segment_info = SEGMENTS[segment]
        content_info = CONTENT_TYPES[content_type]
        
        if persona == "No Persona":
            prompt = f"""
            Generate {content_type} content for Vapi's voice AI technology feature: {feature}

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
            3. Emphasize Vapi's voice AI value proposition
            4. Include appropriate call-to-action for {content_type}
            
            Make the content compelling and focused on how Vapi's voice AI technology solves specific challenges for this segment.
            """
        else:
            prompt = f"""
            Generate {content_type} content for Vapi's voice AI technology feature: {feature}

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
            4. Emphasize Vapi's voice AI value proposition
            5. Include appropriate call-to-action for {content_type}
            
            Make the content compelling and focused on how Vapi's voice AI technology solves specific challenges for this persona.
            """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an experienced B2B SaaS marketing copywriter who specializes in voice AI technology and startup marketing."},
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
st.title("AI Content Generator")
st.write("Create targeted content for an AI startup across different segments and formats.")

# Input sections
with st.form("content_form"):
    feature = st.text_area(
        "Voice AI Feature/Capability",
        placeholder="Describe the Vapi feature or capability you want to promote...",
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
                
                # Display segment and content type context
                st.info(f"Segment Focus: {SEGMENTS[segment]['focus']}\nContent Type: {CONTENT_TYPES[content_type]['focus']}")
                
                # Display the generated content
                st.write(f"### Generated {content_type}")
                st.write(content)
                
                # Add a copy button
                st.text_area("Copy-ready version", content, height=200)
                
                # Add download button
                st.download_button(
                    label="Download Content",
                    data=content,
                    file_name=f"vapi_{segment}_{content_type}_{tone.lower()}.txt",
                    mime="text/plain"
                )

# Add usage tips in an expander
with st.expander("💡 Tips for best results"):
    st.markdown("""
    ### Writing Effective Feature Descriptions
    - Focus on specific voice AI capabilities
    - Include technical specifications and advantages
    - Highlight differentiators from competitors
    - Mention specific problems solved
    
    ### Segment-Specific Considerations
    - **Enterprise**: Focus on scalability, security, and integration
    - **SMBs**: Emphasize ease of use and cost-effectiveness
    - **Developers**: Highlight API capabilities and documentation
    - **Call Centers**: Focus on efficiency, agent empowerment, and quality metrics
    - **Education**: Emphasize engagement and accessibility features
    
    ### Content Type Guidelines
    - **Product Description**: Technical details and benefits
    - **Social Media**: Short, engaging snippets with clear CTAs
    - **Blog Posts**: In-depth analysis and thought leadership
    - **Email Campaigns**: Personalized and action-oriented
    - **Case Studies**: Problem-solution format with results
    - **Landing Pages**: Clear value proposition and benefits

    ### Developer-Specific Considerations
    - **Frontend Developers**: Focus on client-side SDKs, UI components, and WebSocket implementation
    - **Backend Developers**: Emphasize API integration, authentication, and server-side processing
    - **Mobile Developers**: Highlight mobile SDKs, offline capabilities, and performance optimization
    - **ML Engineers**: Focus on model customization, training capabilities, and analytics
    - **DevOps**: Address deployment, monitoring, and scaling considerations
    
    ### Technical Content Tips
    - Include code snippets when relevant
    - Provide specific implementation examples
    - Reference documentation links
    - Mention integration patterns
    - Address performance considerations
    - Discuss security implementations
    """)

# Add sample input
with st.expander("📝 Sample Inputs"):
    st.markdown("""
    ### Enterprise Example
    ```
    Feature: Advanced Call Center AI
    - Real-time voice recognition
    - Sentiment analysis
    - Multiple language support
    - Enterprise-grade security
    - CRM integration
    - Custom workflow automation
    ```
    
    ### Call Center Example
    ```
    Feature: Agent Assist AI
    - Real-time agent prompting
    - Call sentiment analysis
    - Automated quality scoring
    - Performance analytics
    - Multi-language support
    - Agent training tools
    - Call disposition automation
    - Compliance monitoring
    ```
    
    ### Developer Examples
    ```
    Feature: Voice AI API Integration
    - RESTful API endpoints
    - WebSocket support for real-time voice processing
    - Multiple SDK options (Python, JavaScript, Java, Go)
    - Custom ML model training capabilities
    - Extensive API documentation
    - Interactive API playground
    - Sandbox testing environment
    - Usage-based pricing
    - Rate limiting controls
    - Error handling and retry logic
    - Real-time voice analytics
    - Custom webhook support
    ```

    ### Developer Tools
    - API Reference Documentation
    - Interactive Swagger/OpenAPI specs
    - Code snippets in multiple languages
    - Sample applications
    - WebSocket implementation examples
    - Voice processing libraries
    - Testing utilities
    - Performance monitoring tools
    ```

    ### Integration Features
    - OAuth 2.0 authentication
    - API key management
    - Rate limiting configuration
    - Custom model deployment
    - Webhook configuration
    - Error logging and monitoring
    - Performance analytics
    - Language model fine-tuning
    ```
    """)
