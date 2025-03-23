# HubSpot Partner Finder Agent
# This agent scrapes web and LinkedIn data to identify ideal partners for HubSpot's solution partner program

import streamlit as st
import requests
import json
import pandas as pd
import time
from bs4 import BeautifulSoup
import re
from linkedin_api import Linkedin
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="HubSpot Partner Finder",
    page_icon="🔍",
    layout="wide"
)

# Define the IPP criteria
IPP_CRITERIA = {
    "Company Profile": [
        "51+ employees",
        "Clear organizational structure (Marketing, Sales, Professional Services, Customer Success)",
        "Offers enterprise software and related services",
        "Established processes for marketing planning, sales, SaaS implementation, and customer lifecycle management"
    ],
    "Customer Focus": [
        "Targets customers with 201+ employees",
        "Supports environments with 101+ users",
        "Manages full customer lifecycle",
        "Focuses on specific industries with deep expertise"
    ],
    "Tech Stack Expertise": [
        "Expertise in enterprise software tools",
        "Can develop custom integrations using APIs/SDKs",
        "Participates in partner programs from enterprise software vendors"
    ],
    "Strategic Alignment": [
        "Has executive sponsors for partnerships",
        "Has established or willing to establish HubSpot practice",
        "Committed to invest resources in HubSpot partnership"
    ],
    "Specializations": [
        "Digital Marketing (SEO, PPC, Social Media, Content, Email)",
        "CRM Implementation and Optimization",
        "RevOps (Revenue Operations)"
    ]
}

# Function to search for companies
def search_companies(query, location=None, industry=None, api_key=None):
    st.write(f"Searching for companies matching: {query}")
    
    # This would typically use a real API like LinkedIn or Clearbit
    # For demonstration, returning mock data
    if not api_key:
        st.warning("API key not provided. Using mock data.")
        
    # In a real implementation, this would make API calls
    # Mock data for demonstration
    mock_results = [
        {
            "name": "Digital Growth Partners",
            "website": "digitalgrowthpartners.com",
            "employees": 75,
            "location": "Boston, MA",
            "industry": "Digital Marketing",
            "description": "Full-service digital marketing agency specializing in SEO, PPC, and CRM implementation",
            "founded": 2012,
            "specializations": ["Digital Marketing", "CRM Implementation", "Content Marketing"]
        },
        {
            "name": "RevOps Solutions Inc.",
            "website": "revopssolutions.com",
            "employees": 120,
            "location": "Austin, TX",
            "industry": "Business Consulting",
            "description": "Revenue Operations consultancy helping enterprise businesses align sales, marketing and customer service",
            "founded": 2015,
            "specializations": ["RevOps", "CRM Implementation", "Marketing Automation"]
        },
        {
            "name": "Enterprise CRM Experts",
            "website": "enterprisecrm.co",
            "employees": 65,
            "location": "Chicago, IL",
            "industry": "Technology Consulting",
            "description": "CRM implementation specialists for mid-market and enterprise companies",
            "founded": 2010,
            "specializations": ["CRM Implementation", "Systems Integration", "Custom Development"]
        }
    ]
    
    return mock_results

# Function to scrape company website
def scrape_company_website(url):
    st.write(f"Analyzing website: {url}")
    
    try:
        # In a real implementation, this would make actual requests
        # Mock data for demonstration
        if "digitalgrowthpartners" in url:
            return {
                "technologies": ["Salesforce", "Marketo", "Google Analytics", "WordPress"],
                "services": ["SEO", "PPC", "Content Marketing", "Email Marketing", "CRM Implementation"],
                "target_industries": ["SaaS", "Healthcare", "Finance"],
                "case_studies": 12,
                "team_size_mentioned": "70+ professionals",
                "enterprise_focus": True
            }
        elif "revopssolutions" in url:
            return {
                "technologies": ["HubSpot", "Salesforce", "Tableau", "Zapier"],
                "services": ["RevOps Consulting", "CRM Implementation", "Sales Enablement", "Marketing Automation"],
                "target_industries": ["Technology", "Manufacturing", "Professional Services"],
                "case_studies": 8,
                "team_size_mentioned": "Over 100 consultants",
                "enterprise_focus": True
            }
        elif "enterprisecrm" in url:
            return {
                "technologies": ["Salesforce", "Microsoft Dynamics", "Oracle", "SAP"],
                "services": ["CRM Strategy", "Implementation", "Training", "Support"],
                "target_industries": ["Healthcare", "Financial Services", "Manufacturing"],
                "case_studies": 15,
                "team_size_mentioned": "60+ specialists",
                "enterprise_focus": True
            }
        else:
            return {
                "technologies": [],
                "services": [],
                "target_industries": [],
                "case_studies": 0,
                "team_size_mentioned": "",
                "enterprise_focus": False
            }
    except Exception as e:
        st.error(f"Error scraping website: {e}")
        return None

# Function to get LinkedIn data
def get_linkedin_data(company_name, linkedin_username=None, linkedin_password=None):
    st.write(f"Retrieving LinkedIn data for: {company_name}")
    
    if not linkedin_username or not linkedin_password:
        st.warning("LinkedIn credentials not provided. Using mock data.")
    
    # In a real implementation, this would use the LinkedIn API
    # Mock data for demonstration
    if company_name == "Digital Growth Partners":
        return {
            "follower_count": 4500,
            "employee_count": 78,
            "year_founded": 2012,
            "headquarters": "Boston, MA",
            "specialties": ["Digital Marketing", "CRM", "Marketing Automation"],
            "recent_posts": 15,
            "enterprise_clients": ["Acme Corp", "Tech Innovators", "Global Health"],
            "key_executives": [
                {"name": "Sarah Johnson", "title": "CEO"},
                {"name": "Mike Chen", "title": "CTO"},
                {"name": "Lisa Patel", "title": "VP of Client Services"}
            ]
        }
    elif company_name == "RevOps Solutions Inc.":
        return {
            "follower_count": 7200,
            "employee_count": 122,
            "year_founded": 2015,
            "headquarters": "Austin, TX",
            "specialties": ["Revenue Operations", "CRM Implementation", "Sales Enablement"],
            "recent_posts": 22,
            "enterprise_clients": ["Enterprise Software Co.", "Financial Services Inc.", "ManufacturingPro"],
            "key_executives": [
                {"name": "Robert Wilson", "title": "CEO"},
                {"name": "Emily Rodriguez", "title": "COO"},
                {"name": "David Thompson", "title": "Chief Revenue Officer"}
            ]
        }
    elif company_name == "Enterprise CRM Experts":
        return {
            "follower_count": 3800,
            "employee_count": 67,
            "year_founded": 2010,
            "headquarters": "Chicago, IL",
            "specialties": ["CRM Strategy", "Enterprise Software", "Systems Integration"],
            "recent_posts": 8,
            "enterprise_clients": ["Healthcare Solutions", "Global Banking Corp", "Industrial Supplies Inc."],
            "key_executives": [
                {"name": "James Anderson", "title": "CEO"},
                {"name": "Sophia Martinez", "title": "CTO"},
                {"name": "Michael Lee", "title": "VP of Professional Services"}
            ]
        }
    else:
        return None

# Function to score a company based on IPP criteria
def score_company(company_data, website_data, linkedin_data):
    score = {
        "Company Profile": 0,
        "Customer Focus": 0,
        "Tech Stack Expertise": 0,
        "Strategic Alignment": 0,
        "Specializations": 0
    }
    
    max_scores = {
        "Company Profile": 4,
        "Customer Focus": 4,
        "Tech Stack Expertise": 3,
        "Strategic Alignment": 3,
        "Specializations": 3
    }
    
    # Score Company Profile
    if company_data["employees"] >= 51:
        score["Company Profile"] += 1
    
    if linkedin_data and len(linkedin_data["key_executives"]) >= 3:
        score["Company Profile"] += 1
    
    if website_data and len(website_data["services"]) >= 4:
        score["Company Profile"] += 1
    
    if website_data and website_data["case_studies"] >= 5:
        score["Company Profile"] += 1
    
    # Score Customer Focus
    if linkedin_data and linkedin_data["enterprise_clients"]:
        score["Customer Focus"] += 2
    
    if website_data and website_data["enterprise_focus"]:
        score["Customer Focus"] += 1
    
    if website_data and len(website_data["target_industries"]) >= 2:
        score["Customer Focus"] += 1
    
    # Score Tech Stack Expertise
    if website_data and len(website_data["technologies"]) >= 3:
        score["Tech Stack Expertise"] += 1
    
    has_enterprise_tech = False
    if website_data and website_data["technologies"]:
        enterprise_tech = ["Salesforce", "Oracle", "SAP", "Microsoft Dynamics", "Marketo", "Adobe"]
        if any(tech in enterprise_tech for tech in website_data["technologies"]):
            has_enterprise_tech = True
            score["Tech Stack Expertise"] += 1
    
    if has_enterprise_tech and "Integration" in str(website_data.get("services", [])):
        score["Tech Stack Expertise"] += 1
    
    # Score Strategic Alignment
    strategic_alignment_potential = 0
    
    if linkedin_data and "CTO" in str(linkedin_data["key_executives"]):
        strategic_alignment_potential += 1
    
    if website_data and "HubSpot" in str(website_data.get("technologies", [])):
        strategic_alignment_potential += 2
    elif website_data and any(crm in str(website_data.get("services", [])) for crm in ["CRM", "Customer Relationship"]):
        strategic_alignment_potential += 1
    
    score["Strategic Alignment"] = min(strategic_alignment_potential, max_scores["Strategic Alignment"])
    
    # Score Specializations
    specializations = set()
    if "Digital Marketing" in company_data.get("specializations", []) or any(s in str(website_data.get("services", [])) for s in ["SEO", "PPC", "Social Media", "Content"]):
        specializations.add("Digital Marketing")
    
    if "CRM" in company_data.get("specializations", []) or "CRM" in str(website_data.get("services", [])):
        specializations.add("CRM Implementation")
    
    if "RevOps" in company_data.get("specializations", []) or "Revenue Operations" in str(website_data.get("services", [])):
        specializations.add("RevOps")
    
    score["Specializations"] = min(len(specializations), max_scores["Specializations"])
    
    # Calculate percentage scores
    percentage_scores = {}
    for category, value in score.items():
        percentage_scores[category] = (value / max_scores[category]) * 100
    
    # Calculate overall match percentage
    total_score = sum(score.values())
    max_total = sum(max_scores.values())
    overall_match = (total_score / max_total) * 100
    
    return {
        "detailed_scores": score,
        "percentage_scores": percentage_scores,
        "overall_match": overall_match,
        "specializations": list(specializations)
    }

# Function to generate recommendations
def generate_recommendations(company_data, score_data, website_data, linkedin_data):
    recommendations = []
    
    # Evaluate company profile
    if score_data["percentage_scores"]["Company Profile"] < 75:
        if company_data["employees"] < 51:
            recommendations.append("Company size is below the recommended 51+ employees for Upmarket IPP")
        
        if not linkedin_data or len(linkedin_data["key_executives"]) < 3:
            recommendations.append("Consider establishing a clearer organizational structure with defined roles in Marketing, Sales, Professional Services, and Customer Success")
    
    # Evaluate customer focus
    if score_data["percentage_scores"]["Customer Focus"] < 75:
        if not linkedin_data or not linkedin_data["enterprise_clients"]:
            recommendations.append("Focus on targeting and showcasing enterprise clients (201+ employees)")
        
        if not website_data or not website_data["enterprise_focus"]:
            recommendations.append("Highlight ability to support environments with 101+ users")
        
        if not website_data or len(website_data["target_industries"]) < 2:
            recommendations.append("Develop and showcase deeper industry expertise in specific sectors")
    
    # Evaluate tech stack expertise
    if score_data["percentage_scores"]["Tech Stack Expertise"] < 75:
        if not website_data or len(website_data["technologies"]) < 3:
            recommendations.append("Expand expertise in enterprise software tools and highlight them in marketing materials")
        
        if not website_data or "Integration" not in str(website_data.get("services", [])):
            recommendations.append("Develop custom solution capabilities using APIs and SDKs")
    
    # Evaluate strategic alignment
    if score_data["percentage_scores"]["Strategic Alignment"] < 75:
        if not "HubSpot" in str(website_data.get("technologies", [])):
            recommendations.append("Consider establishing a HubSpot practice or partnering with HubSpot")
        
        recommendations.append("Designate an Executive Sponsor and Business Champion for the HubSpot relationship")
    
    # Evaluate specializations
    if score_data["percentage_scores"]["Specializations"] < 66:
        missing_specializations = []
        specializations = score_data.get("specializations", [])
        
        if "Digital Marketing" not in specializations:
            missing_specializations.append("Digital Marketing")
        
        if "CRM Implementation" not in specializations:
            missing_specializations.append("CRM Implementation")
        
        if "RevOps" not in specializations:
            missing_specializations.append("RevOps")
        
        if missing_specializations:
            recommendations.append(f"Consider expanding services to include: {', '.join(missing_specializations)}")
    
    return recommendations

# Main app
def main():
    st.title("🔍 HubSpot Partner Finder")
    st.subheader("Identify ideal partners for HubSpot's solution partner program")
    
    # Sidebar for API keys
    st.sidebar.title("API Configuration")
    
    with st.sidebar.expander("API Keys", expanded=True):
        linkedin_username = st.text_input("LinkedIn Email", type="password")
        linkedin_password = st.text_input("LinkedIn Password", type="password")
        clearbit_api_key = st.text_input("Clearbit API Key (optional)", type="password")
        hunter_api_key = st.text_input("Hunter.io API Key (optional)", type="password")
    
    # Display IPP criteria
    with st.sidebar.expander("Ideal Partner Profile Criteria", expanded=False):
        for category, items in IPP_CRITERIA.items():
            st.sidebar.subheader(category)
            for item in items:
                st.sidebar.markdown(f"- {item}")
    
    # Search tab
    st.subheader("Search for Potential Partners")
    
    col1, col2 = st.columns(2)
    with col1:
        search_query = st.text_input("Search for companies by keyword", "digital marketing agency")
    
    with col2:
        location = st.text_input("Location (optional)", "")
    
    col3, col4 = st.columns(2)
    with col3:
        industry_options = ["", "Digital Marketing", "Business Consulting", "Technology Consulting", "Software Development", "Marketing Agency"]
        industry = st.selectbox("Industry (optional)", industry_options)
    
    with col4:
        min_size = st.selectbox("Minimum company size", ["Any", "11-50", "51-200", "201-500", "501-1000", "1001+"], index=2)
    
    if st.button("Search Companies"):
        with st.spinner("Searching for companies..."):
            companies = search_companies(search_query, location, industry, clearbit_api_key)
            
            if not companies:
                st.warning("No companies found. Try adjusting your search criteria.")
            else:
                st.success(f"Found {len(companies)} potential partners")
                
                # Store companies in session state
                st.session_state.companies = companies
    
    # Display results if available
    if hasattr(st.session_state, 'companies') and st.session_state.companies:
        st.subheader("Potential Partners")
        
        for i, company in enumerate(st.session_state.companies):
            with st.expander(f"{company['name']} - {company['location']}", expanded=i==0):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Website:** {company['website']}")
                    st.markdown(f"**Industry:** {company['industry']}")
                    st.markdown(f"**Employees:** {company['employees']}")
                    st.markdown(f"**Founded:** {company['founded']}")
                    st.markdown(f"**Description:** {company['description']}")
                    st.markdown(f"**Specializations:** {', '.join(company['specializations'])}")
                
                with col2:
                    if st.button(f"Analyze Fit for {company['name']}", key=f"analyze_{i}"):
                        with st.spinner(f"Analyzing {company['name']}..."):
                            # Get website data
                            website_data = scrape_company_website(company['website'])
                            
                            # Get LinkedIn data
                            linkedin_data = get_linkedin_data(company['name'], linkedin_username, linkedin_password)
                            
                            # Score the company
                            if website_data and linkedin_data:
                                score_data = score_company(company, website_data, linkedin_data)
                                recommendations = generate_recommendations(company, score_data, website_data, linkedin_data)
                                
                                # Store analysis in session state
                                if not hasattr(st.session_state, 'analysis'):
                                    st.session_state.analysis = {}
                                
                                st.session_state.analysis[company['name']] = {
                                    "company": company,
                                    "website_data": website_data,
                                    "linkedin_data": linkedin_data,
                                    "score_data": score_data,
                                    "recommendations": recommendations
                                }
                                
                                st.rerun()
                            else:
                                st.error("Unable to analyze company. Check API credentials and try again.")
    
    # Display analysis if available
    if hasattr(st.session_state, 'analysis') and st.session_state.analysis:
        st.subheader("Partner Fit Analysis")
        
        # Sort companies by overall match score
        sorted_companies = sorted(
            st.session_state.analysis.items(),
            key=lambda x: x[1]["score_data"]["overall_match"],
            reverse=True
        )
        
        for company_name, analysis in sorted_companies:
            company = analysis["company"]
            score_data = analysis["score_data"]
            website_data = analysis["website_data"]
            linkedin_data = analysis["linkedin_data"]
            recommendations = analysis["recommendations"]
            
            with st.expander(f"{company_name} - {score_data['overall_match']:.1f}% Match", expanded=True):
                st.markdown(f"### {company_name}")
                
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    # Overall fit gauge chart
                    st.markdown(f"**Overall IPP Match:** {score_data['overall_match']:.1f}%")
                    
                    # Category scores
                    st.markdown("#### Category Scores")
                    for category, percentage in score_data["percentage_scores"].items():
                        st.markdown(f"**{category}:** {percentage:.1f}%")
                    
                    # Company details
                    st.markdown("#### Company Details")
                    st.markdown(f"**Employees:** {company['employees']}")
                    st.markdown(f"**Website:** {company['website']}")
                    st.markdown(f"**Specializations:** {', '.join(company['specializations'])}")
                    
                    if linkedin_data:
                        st.markdown("#### LinkedIn Insights")
                        st.markdown(f"**LinkedIn Followers:** {linkedin_data['follower_count']}")
                        st.markdown(f"**LinkedIn Employee Count:** {linkedin_data['employee_count']}")
                        st.markdown(f"**Enterprise Clients:** {', '.join(linkedin_data['enterprise_clients'])}")
                        
                        st.markdown("**Key Executives:**")
                        for exec in linkedin_data["key_executives"]:
                            st.markdown(f"- {exec['name']} ({exec['title']})")
                
                with col2:
                    # Website analysis
                    st.markdown("#### Website Analysis")
                    st.markdown(f"**Technologies:** {', '.join(website_data['technologies'])}")
                    st.markdown(f"**Services:** {', '.join(website_data['services'])}")
                    st.markdown(f"**Target Industries:** {', '.join(website_data['target_industries'])}")
                    st.markdown(f"**Case Studies:** {website_data['case_studies']}")
                    
                    # Recommendations
                    st.markdown("#### Recommendations")
                    if recommendations:
                        for rec in recommendations:
                            st.markdown(f"- {rec}")
                    else:
                        st.markdown("This company is an excellent match for the HubSpot Solution Partner Program!")
                
                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Export Analysis as PDF", key=f"pdf_{company_name}"):
                        st.info("PDF export functionality would be implemented here in a production application")
                
                with col2:
                    if st.button("Add to CRM", key=f"crm_{company_name}"):
                        st.info("CRM integration would be implemented here in a production application")

if __name__ == "__main__":
    main()