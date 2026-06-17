import os
from datetime import datetime, date, time

import requests
import streamlit as st
from dotenv import load_dotenv

from agents import run_agent
from prompts import *

load_dotenv()

st.set_page_config(
    page_title="MarketMind Agents",
    page_icon="◐",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 12% 18%, rgba(220,203,255,0.95) 0%, transparent 28%),
        radial-gradient(circle at 85% 18%, rgba(246,157,213,0.75) 0%, transparent 26%),
        radial-gradient(circle at 45% 90%, rgba(182,156,255,0.60) 0%, transparent 34%),
        linear-gradient(135deg, #120925 0%, #27124F 34%, #5A3BD6 70%, #C7A7FF 100%);
    background-attachment: fixed;
    color: #FAF8FF;
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(250,248,255,0.72);
    backdrop-filter: blur(24px);
    border-right: 1px solid rgba(255,255,255,0.55);
}

section[data-testid="stSidebar"] * {
    color: #241642 !important;
}

.brand-logo {
    font-size: 31px;
    font-weight: 900;
    letter-spacing: 0.5px;
    color: #241642;
}

section[data-testid="stSidebar"] .stRadio label {
    font-weight: 700;
}

/* Headings */
.main-title {
    font-size: 70px;
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1.04;
    letter-spacing: -2px;
}

.gradient-text {
    background: linear-gradient(90deg, #FFFFFF, #F6B5E4, #C8B6FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900;
}

.subtitle {
    font-size: 20px;
    color: #F7F0FF;
    font-weight: 600;
    line-height: 1.8;
}

/* Luxury glass */
.glass-card {
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.36);
    border-radius: 34px;
    padding: 34px;
    box-shadow: 0 28px 80px rgba(28, 11, 69, 0.34);
    backdrop-filter: blur(28px);
    margin-bottom: 24px;
}

.glass-card h2,
.glass-card h3,
.glass-card p,
.glass-card li {
    color: #FFFFFF;
}

/* Workflow */
.workflow-step {
    background: rgba(255,255,255,0.18);
    border-radius: 18px;
    padding: 15px 18px;
    margin-bottom: 12px;
    border: 1px solid rgba(255,255,255,0.30);
    color: white;
    font-weight: 800;
}

/* Agent cards */
.agent-card {
    background: rgba(255,255,255,0.20);
    border-radius: 28px;
    padding: 28px;
    text-align: left;
    border: 1px solid rgba(255,255,255,0.34);
    box-shadow: 0 18px 45px rgba(28,11,69,0.25);
    min-height: 230px;
}

.agent-number {
    width: 46px;
    height: 46px;
    background: linear-gradient(135deg, #FFFFFF, #F6B5E4);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    margin-bottom: 18px;
    color: #3C236E;
}

.agent-title {
    font-size: 22px;
    font-weight: 900;
    color: #FFFFFF;
}

.agent-desc {
    color: #F9F4FF;
    font-size: 16px;
    line-height: 1.65;
    font-weight: 500;
}

.status-done {
    color: #DFFFEF;
    font-weight: 900;
    letter-spacing: 1px;
}

/* Forms */
label,
.stSelectbox label,
.stTextInput label,
.stTextArea label,
.stMultiSelect label,
.stDateInput label,
.stTimeInput label,
.stRadio label {
    color: #FFFFFF !important;
    font-weight: 850 !important;
    font-size: 16px !important;
}

input,
textarea,
div[data-baseweb="select"] {
    background: rgba(255,255,255,0.96) !important;
    color: #241642 !important;
    border-radius: 16px !important;
    font-weight: 650 !important;
    border: 1px solid rgba(255,255,255,0.65) !important;
}

input::placeholder,
textarea::placeholder {
    color: #77658E !important;
}

div[data-baseweb="select"] * {
    color: #241642 !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #6D4AFF, #C86FFF, #F69DD5);
    color: white;
    border: none;
    border-radius: 18px;
    padding: 14px 26px;
    font-weight: 900;
    min-height: 50px;
    box-shadow: 0 15px 40px rgba(90,50,200,0.42);
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 22px 55px rgba(90,50,200,0.55);
}

.stDownloadButton button {
    background: #FAF8FF;
    color: #2C145E;
    border-radius: 18px;
    font-weight: 900;
}

/* Text readability */
p, li {
    font-size: 16px;
    line-height: 1.75;
}

h1, h2, h3 {
    color: white;
}

/* Report output */
.report-box {
    background: rgba(250,248,255,0.96);
    color: #241642;
    padding: 30px;
    border-radius: 28px;
    box-shadow: 0 22px 60px rgba(28,11,69,0.26);
}

.report-box * {
    color: #241642 !important;
}

/* Instagram phone */
.phone-preview {
    width: 360px;
    max-width: 100%;
    background: #111111;
    border-radius: 40px;
    padding: 13px;
    margin: 24px auto;
    box-shadow: 0 30px 70px rgba(0,0,0,0.42);
}

.phone-screen {
    background: #FFFFFF;
    border-radius: 30px;
    overflow: hidden;
}

.insta-top {
    padding: 17px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #ECE7F5;
    color: #241642;
    font-weight: 900;
}

.profile-circle {
    width: 42px;
    height: 42px;
    background: linear-gradient(135deg,#6D4AFF,#F69DD5,#FFE4F6);
    border-radius: 50%;
    margin-right: 12px;
}

.insta-image {
    height: 285px;
    background:
        radial-gradient(circle at 20% 25%, #FFE4F6 0%, transparent 25%),
        radial-gradient(circle at 80% 25%, #C8B6FF 0%, transparent 26%),
        linear-gradient(135deg,#6D4AFF,#C86FFF,#F69DD5);
    color: white;
    font-size: 22px;
    font-weight: 900;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    letter-spacing: 0.3px;
    padding: 20px;
}

.insta-actions {
    color: #241642;
    font-size: 22px;
    padding: 13px 17px;
}

.insta-caption {
    color: #241642;
    padding: 0px 17px 22px 17px;
    font-size: 14px;
    line-height: 1.6;
    font-weight: 500;
}

.insta-caption strong {
    color: #241642;
    font-weight: 900;
}

/* Timeline */
.timeline {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 26px;
}

.timeline-item {
    background: rgba(255,255,255,0.22);
    color: white;
    padding: 11px 18px;
    border-radius: 18px;
    font-weight: 900;
    border: 1px solid rgba(255,255,255,0.38);
}

.status-card {
    background: rgba(255,255,255,0.20);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    margin-top: 15px;
    border: 1px solid rgba(255,255,255,0.35);
}

.status-card h3,
.status-card p {
    color: white;
}

/* Code block / n8n page */
pre {
    border-radius: 22px !important;
    background: rgba(250,248,255,0.96) !important;
}

code {
    color: #241642 !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 18px;
}
            /* Fix unreadable submit/button states */
.stButton button,
.stFormSubmitButton button {
    background: linear-gradient(135deg, #6D4AFF, #C86FFF, #F69DD5) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 18px !important;
    font-weight: 900 !important;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: linear-gradient(135deg, #5B2EFF, #B85CFF, #F69DD5) !important;
    color: #FFFFFF !important;
    border: none !important;
}

/* Fix white boxes / form container readability */
div[data-testid="stForm"] {
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.32);
    border-radius: 28px;
    padding: 28px;
    backdrop-filter: blur(24px);
}

/* Fix alert text visibility */
div[data-testid="stAlert"] * {
    color: #241642 !important;
    font-weight: 700 !important;
}

/* Make code/output blocks readable */
pre, code {
    background: #FAF8FF !important;
    color: #241642 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "final_output" not in st.session_state:
    st.session_state.final_output = ""

if "post_output" not in st.session_state:
    st.session_state.post_output = ""

if "edited_post" not in st.session_state:
    st.session_state.edited_post = ""

if "automation_status" not in st.session_state:
    st.session_state.automation_status = "Waiting for Approval"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("<div class='brand-logo'>MarketMind</div>", unsafe_allow_html=True)
    st.caption("Agentic AI Marketing Platform")

    page = st.radio(
        "Navigation",
        [
            "Landing Page",
            "Campaign Generator",
            "Instagram Approval",
            "Campaign Chatbot",
            "n8n Automation"
        ]
    )

    st.markdown("---")
    st.success("Agents Ready")
    st.caption("Supervisor • Research • Strategy • Content • Critic • Scheduler")

# ---------------- LANDING PAGE ----------------
if page == "Landing Page":
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown("""
        <div class="glass-card">
            <div class="main-title">
                MarketMind <br><span class="gradient-text">Agents</span>
            </div>
            <p class="subtitle">
                Autonomous AI Content Marketing Automation Platform.
                Plan, create, review, schedule and automate marketing campaigns using multi-agent AI.
            </p>
            <h3>Plan • Create • Approve • Schedule • Publish</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
            <h3>Why this is Agentic AI?</h3>
            <p>
            MarketMind is not only a text generator. It uses a supervisor-controlled multi-agent
            workflow where each agent has a separate responsibility. The system generates campaign
            strategy, Instagram content, quality review, human approval and automation-ready output.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h2>Agent Workflow</h2>
            <div class="workflow-step">01. User Input</div>
            <div class="workflow-step">02. Supervisor Agent</div>
            <div class="workflow-step">03. Research Agent</div>
            <div class="workflow-step">04. Strategy Agent</div>
            <div class="workflow-step">05. Content Agent</div>
            <div class="workflow-step">06. Critic Agent</div>
            <div class="workflow-step">07. Human Approval</div>
            <div class="workflow-step">08. Scheduler Agent + n8n</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Core Agents")

    a1, a2, a3 = st.columns(3)
    a4, a5, a6 = st.columns(3)

    agents = [
        ("01", "Research Agent", "Analyzes audience, market trends and competitors."),
        ("02", "Strategy Agent", "Creates campaign direction, funnel and positioning."),
        ("03", "Content Agent", "Generates captions, emails, ad copy and blog ideas."),
        ("04", "Critic Agent", "Reviews content quality, tone, CTA and brand safety."),
        ("05", "Scheduler Agent", "Creates posting calendar and publishing timeline."),
        ("06", "Automation Agent", "Sends approved content to n8n workflow.")
    ]

    for col, agent in zip([a1, a2, a3, a4, a5, a6], agents):
        with col:
            st.markdown(f"""
            <div class="agent-card">
                <div class="agent-number">{agent[0]}</div>
                <p class="agent-title">{agent[1]}</p>
                <p class="agent-desc">{agent[2]}</p>
                <p class="status-done">ACTIVE</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------- CAMPAIGN GENERATOR ----------------
elif page == "Campaign Generator":
    st.markdown("<h1 class='gradient-text'>Generate Marketing Campaign</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <p class="subtitle">
        Enter product details. The agents will create research, strategy, content, review and schedule.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("campaign_form"):
        col1, col2 = st.columns(2)

        with col1:
            business_name = st.text_input("Business / Product Name", placeholder="Example: Fasal AI")
            industry = st.text_input("Industry / Niche", placeholder="Example: Agriculture AI")
            target_audience = st.text_input("Target Audience", placeholder="Example: Farmers, small businesses")

        with col2:
            goal = st.selectbox("Campaign Goal", ["Awareness", "Sales", "Leads", "Engagement"])
            platforms = st.multiselect(
                "Platforms",
                ["Instagram", "LinkedIn", "Facebook", "Email", "Blog"],
                default=["Instagram"]
            )
            brand_tone = st.selectbox(
                "Brand Tone",
                ["Professional", "Luxury", "Friendly", "Emotional", "Bold", "Islamic modest tone"]
            )

        extra_details = st.text_area(
            "Extra Details",
            placeholder="Write product features, offer, location, target city etc."
        )

        submitted = st.form_submit_button("Generate Agentic Campaign")

    if submitted:
        user_input = f"""
        Business: {business_name}
        Industry: {industry}
        Audience: {target_audience}
        Goal: {goal}
        Platforms: {platforms}
        Brand Tone: {brand_tone}
        Extra Details: {extra_details}
        """

        with st.spinner("Supervisor Agent planning workflow..."):
            supervisor = run_agent(SUPERVISOR_PROMPT, user_input)

        with st.spinner("Research Agent analyzing market..."):
            research = run_agent(RESEARCH_PROMPT, user_input)

        with st.spinner("Strategy Agent creating campaign strategy..."):
            strategy = run_agent(STRATEGY_PROMPT, research)

        with st.spinner("Content Agent generating marketing content..."):
            content = run_agent(CONTENT_PROMPT, strategy)

        with st.spinner("Critic Agent reviewing and improving content..."):
            critic = run_agent(CRITIC_PROMPT, content)

        with st.spinner("Scheduler Agent creating 7-day calendar..."):
            schedule = run_agent(SCHEDULER_PROMPT, critic)

        final_output = f"""
# MarketMind Agents Campaign Report

## Supervisor Agent Plan
{supervisor}

## Research Agent Output
{research}

## Strategy Agent Output
{strategy}

## Content Agent Output
{content}

## Critic Agent Review
{critic}

## Scheduler Agent Calendar
{schedule}
"""

        st.session_state.final_output = final_output
        st.session_state.post_output = ""
        st.session_state.edited_post = ""
        st.session_state.automation_status = "Waiting for Approval"

        st.success("Campaign generated successfully.")

    if st.session_state.final_output:
        st.markdown("<div class='report-box'>", unsafe_allow_html=True)
        st.markdown(st.session_state.final_output)
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            "Download Campaign Report",
            st.session_state.final_output,
            file_name="marketmind_campaign_report.txt"
        )

# ---------------- INSTAGRAM APPROVAL ----------------
elif page == "Instagram Approval":
    st.markdown("<h1 class='gradient-text'>Instagram Approval Studio</h1>", unsafe_allow_html=True)

    if not st.session_state.final_output:
        st.warning("Generate a campaign first from Campaign Generator.")
    else:
        st.markdown("""
        <div class="timeline">
            <div class="timeline-item">Generated</div>
            <div class="timeline-item">Reviewed</div>
            <div class="timeline-item">Editing</div>
            <div class="timeline-item">Human Approval</div>
            <div class="timeline-item">Scheduled</div>
            <div class="timeline-item">n8n Automation</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
            <h3>Instagram Human-in-the-Loop Workflow</h3>
            <p>
            The Instagram Agent creates a post draft. The human reviewer can edit it,
            improve it with AI, approve it, schedule it, and then send the final version
            to n8n email automation.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Create Instagram Post from Campaign"):
            insta_prompt = f"""
            Based on this campaign, create one professional Instagram post.

            Make the output clean and easy to paste.

            Include:
            - Post Title
            - Caption
            - Hashtags
            - Image Design Prompt
            - CTA
            - Best Posting Time
            - Quality Score out of 100

            Campaign:
            {st.session_state.final_output}
            """

            with st.spinner("Instagram Content Agent creating post..."):
                generated_post = run_agent(
                    "You are an Instagram Marketing Agent. Create high-converting Instagram post content.",
                    insta_prompt
                )

            st.session_state.post_output = generated_post
            st.session_state.edited_post = generated_post
            st.session_state.automation_status = "Draft Generated"
            st.rerun()

        # Structural Fix: Nested columns & processing logic completely inside the active session block
        if st.session_state.post_output:
            col_preview, col_editor = st.columns([1, 1.25])

            with col_preview:
                st.markdown("### Instagram Preview")

                preview_text = (
                    st.session_state.edited_post[:300]
                    .replace("<", "")
                    .replace(">", "")
                )

                st.markdown(
                    f"""
                    <div class="phone-preview">
                        <div class="phone-screen">
                            <div class="insta-top">
                                <div class="profile-circle"></div>
                                marketmind.ai
                            </div>
                            <div class="insta-image">
                                ✨ AI GENERATED IMAGE ✨
                            </div>
                            <div class="insta-actions">
                                ❤️ 245 &nbsp;&nbsp; 💬 37 &nbsp;&nbsp; 📤
                            </div>
                            <div class="insta-caption">
                                <strong>marketmind.ai</strong><br>
                                {preview_text}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="status-card">
                        <h3>Automation Status</h3>
                        <p>{st.session_state.automation_status}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_editor:
                st.markdown("### Edit Final Instagram Post")

                edited_post = st.text_area(
                    "Human Editable Post Draft",
                    value=st.session_state.edited_post,
                    height=360
                )
                st.session_state.edited_post = edited_post

                col_ai1, col_ai2 = st.columns(2)

                with col_ai1:
                    if st.button("Improve with AI"):
                        improve_prompt = f"""
                        Improve this Instagram post.

                        Make it:
                        - More engaging
                        - More professional
                        - Stronger CTA
                        - Cleaner formatting
                        - Better hashtags
                        - Less generic and less AI-ish

                        Current post:
                        {st.session_state.edited_post}
                        """

                        with st.spinner("AI Improvement Agent improving post..."):
                            improved_post = run_agent(
                                "You are a senior social media strategist. Improve the given Instagram post.",
                                improve_prompt
                            )

                        st.session_state.edited_post = improved_post
                        st.session_state.automation_status = "Improved by AI"
                        st.rerun()

                with col_ai2:
                    if st.button("Regenerate Post"):
                        regenerate_prompt = f"""
                        Regenerate a better Instagram post from this campaign.

                        Requirements:
                        - Premium brand tone
                        - Strong hook
                        - Short caption
                        - Clear CTA
                        - 8 to 12 hashtags
                        - Image design prompt
                        - Quality score

                        Campaign:
                        {st.session_state.final_output}
                        """

                        with st.spinner("Instagram Agent regenerating post..."):
                            regenerated_post = run_agent(
                                "You are a professional Instagram content strategist.",
                                regenerate_prompt
                            )

                        st.session_state.post_output = regenerated_post
                        st.session_state.edited_post = regenerated_post
                        st.session_state.automation_status = "Regenerated"
                        st.rerun()

                st.markdown("### Human Approval Gate")

                approval = st.radio(
                    "Final Approval Decision",
                    ["Waiting", "Approved", "Rejected"],
                    horizontal=True
                )

                col_date, col_time = st.columns(2)

                with col_date:
                    schedule_date = st.date_input("Schedule Date", value=date.today())

                with col_time:
                    schedule_time = st.time_input("Schedule Time", value=time(18, 0))

                if approval == "Approved":
                    st.success("Human approved the final edited Instagram post.")
                    st.session_state.automation_status = "Approved and Ready"

                    if st.button("Send Final Approved Post to n8n"):
                        webhook_url = os.getenv("N8N_WEBHOOK_URL")

                        if not webhook_url:
                            st.error("N8N_WEBHOOK_URL not found in .env file.")
                        else:
                            payload = {
                                "type": "instagram_post",
                                "approval_status": approval,
                                "scheduled_date": str(schedule_date),
                                "scheduled_time": str(schedule_time),
                                "post_content": st.session_state.edited_post,
                                "created_at": str(datetime.now()),
                                "source": "MarketMind Agents",
                                "human_reviewed": True
                            }

                            try:
                                response = requests.post(webhook_url, json=payload, timeout=15)

                                if response.status_code in [200, 201]:
                                    st.session_state.automation_status = "Sent to n8n Successfully"
                                    st.success("Final approved post sent to n8n automation.")
                                else:
                                    st.session_state.automation_status = "n8n Error"
                                    st.error(f"n8n returned status code: {response.status_code}")

                            except Exception as e:
                                st.session_state.automation_status = "Failed to Send"
                                st.error(f"Failed to send to n8n: {e}")

                elif approval == "Rejected":
                    st.session_state.automation_status = "Rejected by Human"
                    st.error("Post rejected. Edit, improve, or regenerate before approval.")

                else:
                    st.session_state.automation_status = "Waiting for Human Approval"
                    st.warning("Waiting for human approval.")

# ---------------- CHATBOT ----------------
elif page == "Campaign Chatbot":
    st.markdown("<h1 class='gradient-text'>Campaign Assistant Chatbot</h1>", unsafe_allow_html=True)

    if not st.session_state.final_output:
        st.warning("Generate a campaign first.")
    else:
        st.markdown("""
        <div class="glass-card">
        <h3>Ask AI About Your Campaign</h3>
        <p>
        Example questions: Make this caption more emotional, give better hooks,
        explain this strategy, rewrite for Pakistani audience, or make it luxury tone.
        </p>
        </div>
        """, unsafe_allow_html=True)

        user_question = st.chat_input("Ask about your campaign...")

        if user_question:
            st.session_state.chat_history.append(("user", user_question))

            chatbot_prompt = f"""
            You are a Campaign Assistant Agent.
            Answer the user's question using this campaign output.

            Campaign:
            {st.session_state.final_output}

            User Question:
            {user_question}
            """

            with st.spinner("Campaign Assistant thinking..."):
                answer = run_agent(
                    "You are a helpful AI assistant for marketing campaign improvement.",
                    chatbot_prompt
                )

            st.session_state.chat_history.append(("assistant", answer))

        for role, message in st.session_state.chat_history:
            with st.chat_message(role):
                st.markdown(message)

# ---------------- N8N AUTOMATION ----------------
elif page == "n8n Automation":
    st.markdown("<h1 class='gradient-text'>n8n Automation Setup</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    <h3>Recommended n8n Flow</h3>
    <p>Webhook Trigger → Set Node → Email Notification</p>
    </div>
    """, unsafe_allow_html=True)

    st.code("""
Webhook Node:
Method: POST
Path: marketmind-instagram

Expected JSON:
{
  "type": "instagram_post",
  "approval_status": "Approved",
  "scheduled_date": "2026-06-20",
  "scheduled_time": "18:00:00",
  "post_content": "...",
  "created_at": "...",
  "source": "MarketMind Agents",
  "human_reviewed": true
}
""")

    st.info(
        "Your current working automation is: Streamlit → n8n Webhook → Set Node → Email Notification."
    )