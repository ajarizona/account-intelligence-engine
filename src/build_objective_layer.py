"""
build_objective_layer.py

Distills the nine industry strategy references into a single, vendor-agnostic
objective layer the Account Intelligence Engine reads at match-and-score time.

Output: data/objective_layer.json

Design notes:
- Every industry carries the same shape: business objectives (each with a
  strategic focus and the KPIs leaders actually track), the strategic tensions
  between those objectives, and how digital strategy maps onto them.
- The strategic_tensions block is deliberate. It is what stops the engine from
  leading with a use case that wins one KPI while damaging another.
- This layer is vendor-neutral on purpose. No product, no vendor, no client.
"""

import json
from pathlib import Path

SCHEMA_VERSION = "1.0"

INDUSTRIES = [
    {
        "id": "retail-banking",
        "name": "Retail Banking",
        "overview": (
            "Retail banks compete on the strength of primary customer "
            "relationships, the cost and stability of their funding base, and "
            "the quality of their loan book. The objectives below are managed "
            "in balance with one another rather than maximized individually."
        ),
        "business_objectives": [
            {"id": "profitability", "name": "Profitability & Financial Performance",
             "strategic_focus": "Generate sustainable returns and efficient earnings",
             "kpis": ["Net Interest Margin (NIM)", "Return on Equity (ROE)", "Return on Assets (ROA)", "Cost-to-Income Ratio", "Revenue growth"]},
            {"id": "acquisition", "name": "Customer Acquisition & Growth",
             "strategic_focus": "Grow the customer base and market share",
             "kpis": ["New accounts opened", "Customer Acquisition Cost (CAC)", "Customer growth rate", "Market share"]},
            {"id": "retention", "name": "Customer Retention & Loyalty",
             "strategic_focus": "Keep and deepen primary relationships",
             "kpis": ["Churn / attrition rate", "Net Promoter Score (NPS)", "Customer Lifetime Value (CLV)", "Retention rate"]},
            {"id": "deposit-funding", "name": "Deposit & Funding Growth",
             "strategic_focus": "Secure low-cost, stable funding",
             "kpis": ["Deposit growth", "CASA ratio", "Loan-to-deposit ratio", "Cost of funds"]},
            {"id": "lending-credit", "name": "Lending Growth & Credit Quality",
             "strategic_focus": "Expand the loan book within risk appetite",
             "kpis": ["Loan book growth", "Non-Performing Loan (NPL) ratio", "Provision coverage ratio", "Charge-off / credit loss rate"]},
            {"id": "cross-sell", "name": "Cross-Sell & Share of Wallet",
             "strategic_focus": "Increase value per existing customer",
             "kpis": ["Products per customer", "Revenue per customer", "Share of wallet"]},
            {"id": "operational-efficiency", "name": "Operational Efficiency",
             "strategic_focus": "Lower cost-to-serve and improve productivity",
             "kpis": ["Cost-to-Income Ratio", "Cost per transaction", "Straight-through processing rate", "Automation rate"]},
            {"id": "risk-compliance", "name": "Risk & Regulatory Compliance",
             "strategic_focus": "Stay solvent, liquid and compliant",
             "kpis": ["Capital adequacy (CET1 / CAR)", "Liquidity Coverage Ratio (LCR)", "Fraud loss rate", "Audit / compliance findings"]},
            {"id": "customer-experience", "name": "Customer Experience",
             "strategic_focus": "Differentiate on service quality",
             "kpis": ["CSAT", "Customer Effort Score (CES)", "Complaint resolution time", "First-contact resolution"]},
        ],
        "strategic_tensions": [
            {"name": "Lending growth vs. credit quality", "description": "Aggressive loan-book growth inflates volume but pulls against credit quality and the NPL ratio."},
            {"name": "Deposit gathering vs. cost of funds", "description": "Growing deposits competes with keeping the cost of funds low."},
            {"name": "Growth investment vs. cost-to-income", "description": "Investing to grow pulls against the cost-to-income ratio, the metric executives watch most closely."},
        ],
        "digital_strategy": {
            "framing": "Digital is rarely a standalone objective in retail banking. It is a cross-cutting enabler that improves performance against nearly every objective above. The goal is what digital allows the bank to achieve, not going digital for its own sake.",
            "levers": [
                {"area": "Acquisition", "description": "Digital onboarding lowers CAC and widens reach beyond the branch footprint."},
                {"area": "Retention & experience", "description": "A strong mobile app and low-friction UX directly move NPS, CSAT and churn."},
                {"area": "Efficiency", "description": "Channel migration and automation cut cost-to-serve and cost per transaction, the single biggest lever on the cost-to-income ratio."},
                {"area": "Cross-sell", "description": "Data and personalization engines raise products-per-customer and share of wallet."},
                {"area": "Risk", "description": "Real-time monitoring and digital fraud detection reduce loss rates."},
            ],
            "digital_kpis": ["Digital adoption rate", "% of transactions via digital channels", "Mobile app MAU / DAU", "Digital sales penetration", "Digital onboarding completion rate", "Cost-to-serve reduction from channel shift", "App store rating"],
        },
    },
    {
        "id": "insurance",
        "name": "Insurance",
        "overview": (
            "Insurers create value through disciplined underwriting, efficient "
            "claims handling, and prudent management of reserves and investment "
            "assets. Profitability hinges on pricing risk accurately and "
            "controlling loss and expense ratios; growth depends on distribution "
            "reach and policyholder persistency."
        ),
        "business_objectives": [
            {"id": "underwriting-profitability", "name": "Underwriting Profitability",
             "strategic_focus": "Price risk accurately and control losses",
             "kpis": ["Combined ratio", "Loss ratio", "Expense ratio", "Underwriting profit"]},
            {"id": "premium-growth", "name": "Premium Growth & Market Share",
             "strategic_focus": "Grow the book profitably",
             "kpis": ["Gross Written Premium (GWP) growth", "New business premium", "Policies in force", "Market share"]},
            {"id": "retention-persistency", "name": "Retention & Persistency",
             "strategic_focus": "Keep policies on the books",
             "kpis": ["Policy renewal / retention rate", "Persistency rate", "Lapse rate", "NPS"]},
            {"id": "claims", "name": "Claims Management & Efficiency",
             "strategic_focus": "Settle fairly, quickly and accurately",
             "kpis": ["Claims cycle time", "Claims settlement ratio", "Loss Adjustment Expense (LAE) ratio", "Claims leakage", "Fraud detection rate"]},
            {"id": "distribution", "name": "Distribution Effectiveness",
             "strategic_focus": "Maximize productive channel reach",
             "kpis": ["New business by channel", "Quote-to-bind ratio", "Agent / broker productivity", "Producer retention"]},
            {"id": "investment-capital", "name": "Investment & Capital Management",
             "strategic_focus": "Generate returns and hold adequate capital",
             "kpis": ["Investment yield / return", "Solvency ratio (Solvency II / RBC)", "Reserve adequacy"]},
            {"id": "risk-compliance", "name": "Risk & Regulatory Compliance",
             "strategic_focus": "Maintain solvency and compliance",
             "kpis": ["Solvency capital ratio", "Reserve adequacy", "Regulatory breaches", "Audit findings"]},
            {"id": "customer-experience", "name": "Customer Experience",
             "strategic_focus": "Win on service, especially at claim",
             "kpis": ["NPS", "CSAT", "Claims satisfaction", "First Notice of Loss (FNOL) experience"]},
        ],
        "strategic_tensions": [
            {"name": "Growth vs. underwriting discipline", "description": "Loosening standards inflates GWP but degrades the loss ratio. The combined ratio is the headline measure of underwriting health."},
            {"name": "Claims speed vs. leakage control", "description": "Faster settlement improves experience but pulls against leakage control."},
        ],
        "digital_strategy": {
            "framing": "Digital reshapes the insurance value chain from quote to claim. It is the primary lever for reducing the expense ratio, improving the experience at moments of truth, and enabling new risk-based products.",
            "levers": [
                {"area": "Acquisition", "description": "Digital quote-and-bind journeys raise conversion and lower distribution cost."},
                {"area": "Underwriting", "description": "Automated and data-driven underwriting improves speed and risk selection."},
                {"area": "Claims", "description": "Self-service FNOL and straight-through claims cut cycle time and LAE."},
                {"area": "Pricing & products", "description": "Telematics and usage-based models enable more granular, competitive pricing."},
                {"area": "Retention", "description": "Digital servicing and proactive engagement lift persistency."},
            ],
            "digital_kpis": ["Digital quote conversion rate", "% of claims filed digitally", "Automated / straight-through underwriting rate", "Self-service adoption", "Digital policy issuance rate", "Expense ratio reduction from automation"],
        },
    },
    {
        "id": "wealth-management",
        "name": "Wealth Management",
        "overview": (
            "Wealth managers grow by attracting and retaining client assets, "
            "deepening relationships, and delivering advice that meets client "
            "goals. Economics are driven by assets under management, the fee "
            "margin earned on those assets, and the productivity of the advisor "
            "force."
        ),
        "business_objectives": [
            {"id": "aum-growth", "name": "AUM Growth",
             "strategic_focus": "Grow assets under management organically",
             "kpis": ["AUM growth", "Net New Assets (NNA) / net new money", "Organic growth rate"]},
            {"id": "revenue-profitability", "name": "Revenue & Profitability",
             "strategic_focus": "Earn efficient returns on assets",
             "kpis": ["Revenue on assets (bps)", "Fee margin", "Pre-tax margin", "Revenue per advisor"]},
            {"id": "client-acquisition", "name": "Client Acquisition",
             "strategic_focus": "Win new client households",
             "kpis": ["New client households", "Referral rate", "Prospect conversion rate"]},
            {"id": "retention-depth", "name": "Client Retention & Depth",
             "strategic_focus": "Retain clients and broaden relationships",
             "kpis": ["Client retention rate", "Attrition rate", "Share of wallet", "Households with multiple solutions"]},
            {"id": "advisor-productivity", "name": "Advisor Productivity & Retention",
             "strategic_focus": "Maximize and keep advisor talent",
             "kpis": ["AUM per advisor", "Revenue per advisor", "Clients per advisor", "Advisor attrition"]},
            {"id": "investment-performance", "name": "Investment Performance",
             "strategic_focus": "Meet client goals and benchmarks",
             "kpis": ["Performance vs. benchmark", "Risk-adjusted returns", "% portfolios meeting goals"]},
            {"id": "risk-compliance", "name": "Risk & Compliance",
             "strategic_focus": "Uphold suitability and fiduciary duty",
             "kpis": ["Suitability / KYC compliance", "Fiduciary adherence", "Regulatory breaches"]},
            {"id": "client-experience", "name": "Client Experience",
             "strategic_focus": "Deepen trust and engagement",
             "kpis": ["NPS", "Client satisfaction", "Financial-planning engagement rate"]},
        ],
        "strategic_tensions": [
            {"name": "Advisor productivity vs. service depth", "description": "More clients per advisor raises productivity but can dilute relationships."},
            {"name": "Recruiting-led growth vs. margin", "description": "Growth through recruiting pulls against margin. Net new assets is the truest signal of organic health, since total AUM can rise on market performance alone."},
        ],
        "digital_strategy": {
            "framing": "Digital in wealth management is about augmenting the advisor and meeting clients where they are, not replacing the relationship. It scales advice, lowers servicing cost, and creates the always-on engagement clients now expect.",
            "levers": [
                {"area": "Onboarding", "description": "Digital account opening shortens time-to-fund and reduces friction."},
                {"area": "Advice delivery", "description": "Hybrid and robo models extend goal-based advice to more clients economically."},
                {"area": "Engagement", "description": "Client portals and apps provide transparency and drive planning interactions."},
                {"area": "Advisor enablement", "description": "Digital tools and analytics raise advisor productivity and next-best-action quality."},
                {"area": "Retention", "description": "Richer digital experiences increase stickiness and share of wallet."},
            ],
            "digital_kpis": ["Digital client engagement rate", "% clients active on portal / app", "Digital onboarding completion rate", "Hybrid / digital advice adoption", "Advisor tool utilization"],
        },
    },
    {
        "id": "healthcare-provider",
        "name": "Healthcare Provider",
        "overview": (
            "Health systems balance three goals that can compete: high-quality "
            "clinical outcomes, accessible patient experience, and financial "
            "sustainability. Under value-based care, clinical quality ties "
            "directly to reimbursement."
        ),
        "business_objectives": [
            {"id": "clinical-quality", "name": "Clinical Quality & Outcomes",
             "strategic_focus": "Deliver safe, effective care",
             "kpis": ["Readmission rate", "Mortality / hospital-acquired condition rates", "CMS Star / quality measures", "Infection rates"]},
            {"id": "access-volume", "name": "Patient Access & Volume Growth",
             "strategic_focus": "Expand access and capture demand",
             "kpis": ["Patient volume", "New patient acquisition", "Appointment wait times", "Referral capture rate", "Market share"]},
            {"id": "financial-sustainability", "name": "Financial Sustainability",
             "strategic_focus": "Maintain margin and liquidity",
             "kpis": ["Operating margin", "Cost per case", "Days cash on hand", "Days in A/R", "Denial rate"]},
            {"id": "patient-experience", "name": "Patient Experience",
             "strategic_focus": "Improve satisfaction and ease of care",
             "kpis": ["HCAHPS / patient satisfaction", "NPS", "Patient effort", "Wait times"]},
            {"id": "operational-efficiency", "name": "Operational Efficiency & Capacity",
             "strategic_focus": "Optimize throughput and utilization",
             "kpis": ["Bed occupancy", "Average Length of Stay (ALOS)", "OR utilization", "Staffing ratios"]},
            {"id": "workforce", "name": "Workforce Engagement",
             "strategic_focus": "Retain and sustain clinicians",
             "kpis": ["Clinician burnout / turnover", "Nurse vacancy rate", "Staff engagement"]},
            {"id": "value-based", "name": "Value-Based / Population Health",
             "strategic_focus": "Manage total cost and outcomes",
             "kpis": ["Total cost of care", "Quality measure attainment", "Preventive care rates", "Risk-adjusted outcomes"]},
            {"id": "safety-compliance", "name": "Safety & Regulatory Compliance",
             "strategic_focus": "Ensure safety and accreditation",
             "kpis": ["Patient safety events", "Accreditation status", "Compliance findings"]},
        ],
        "strategic_tensions": [
            {"name": "Throughput vs. quality and safety", "description": "Length-of-stay and throughput targets pull against quality and safety."},
            {"name": "Volume growth vs. value-based incentives", "description": "Volume growth pulls against value-based incentives that reward avoiding unnecessary utilization."},
            {"name": "Margin pressure vs. workforce investment", "description": "Margin pressure pulls against the workforce investment that sustains both quality and access."},
        ],
        "digital_strategy": {
            "framing": "Digital health is central to access, experience and efficiency. The digital front door and virtual care extend reach, while data and automation relieve operational and clinician burden.",
            "levers": [
                {"area": "Access", "description": "Telehealth and online scheduling expand capacity and reduce wait times."},
                {"area": "Experience", "description": "Patient portals and digital check-in lower effort and improve satisfaction."},
                {"area": "Efficiency", "description": "EHR optimization and automation reduce administrative load and revenue-cycle friction."},
                {"area": "Outcomes", "description": "Remote patient monitoring and analytics support proactive, lower-cost care."},
                {"area": "Workforce", "description": "Ambient documentation and decision support help reduce clinician burnout."},
            ],
            "digital_kpis": ["Telehealth visit volume / share", "Patient portal adoption", "Online scheduling rate", "Digital check-in rate", "Remote monitoring enrollment"],
        },
    },
    {
        "id": "healthcare-payer",
        "name": "Healthcare Payer",
        "overview": (
            "Health plans succeed by managing medical costs, growing and "
            "retaining membership, and improving quality scores that drive "
            "reimbursement and competitiveness. The medical loss ratio anchors "
            "the economics, while Star and HEDIS ratings increasingly shape "
            "revenue and market position."
        ),
        "business_objectives": [
            {"id": "medical-cost", "name": "Medical Cost Management",
             "strategic_focus": "Control trend and utilization",
             "kpis": ["Medical Loss Ratio (MLR)", "PMPM cost", "Medical cost trend", "Utilization rates"]},
            {"id": "membership", "name": "Membership Growth & Retention",
             "strategic_focus": "Grow and keep members",
             "kpis": ["Membership growth", "Member retention", "New enrollment", "Lapse rate", "Market share"]},
            {"id": "financial-performance", "name": "Financial Performance",
             "strategic_focus": "Run an efficient, profitable plan",
             "kpis": ["Administrative cost ratio", "Operating margin", "Premium revenue growth", "Profit margin"]},
            {"id": "quality-stars", "name": "Quality & Star Ratings",
             "strategic_focus": "Improve measured quality and outcomes",
             "kpis": ["CMS Star Ratings", "HEDIS scores", "Member health outcomes"]},
            {"id": "member-experience", "name": "Member Experience & Engagement",
             "strategic_focus": "Improve satisfaction and engagement",
             "kpis": ["NPS", "CAHPS", "Member satisfaction", "Digital engagement", "Call-center service levels"]},
            {"id": "network", "name": "Provider Network Management",
             "strategic_focus": "Build effective, value-based networks",
             "kpis": ["Network adequacy", "Provider satisfaction", "Value-based contract penetration", "In-network utilization"]},
            {"id": "care-management", "name": "Care & Utilization Management",
             "strategic_focus": "Close gaps and avoid unnecessary cost",
             "kpis": ["Prior-auth turnaround time", "Care-management enrollment", "Avoidable ED / admissions", "Gaps-in-care closure"]},
            {"id": "risk-compliance", "name": "Risk & Regulatory Compliance",
             "strategic_focus": "Ensure accuracy and compliance",
             "kpis": ["Risk-adjustment accuracy", "Regulatory compliance", "Audit findings"]},
        ],
        "strategic_tensions": [
            {"name": "MLR control vs. Star ratings and satisfaction", "description": "Cutting the medical loss ratio through restrictive utilization management can damage Star ratings, member satisfaction and provider relationships, all of which feed back into revenue. The durable approach lowers cost through better care management and gap closure rather than access friction."},
        ],
        "digital_strategy": {
            "framing": "Digital lets payers engage members directly, automate high-volume transactions, and apply analytics to manage cost and quality proactively rather than retrospectively.",
            "levers": [
                {"area": "Member engagement", "description": "Apps and portals improve satisfaction, gap closure and self-service."},
                {"area": "Automation", "description": "Auto-adjudication and digital prior auth cut administrative cost and turnaround."},
                {"area": "Care management", "description": "Predictive analytics identify rising-risk members for earlier intervention."},
                {"area": "Quality", "description": "Digital outreach supports HEDIS gap closure and Star-rating improvement."},
                {"area": "Access", "description": "Integrated telehealth steers members to lower-cost, convenient care."},
            ],
            "digital_kpis": ["Digital member adoption", "% claims auto-adjudicated", "Digital prior-auth rate", "Self-service rate", "App / portal engagement"],
        },
    },
    {
        "id": "retail",
        "name": "Retail",
        "overview": (
            "Retailers compete on assortment, price, availability and experience "
            "across stores and digital channels. Economics are driven by gross "
            "margin, inventory productivity, and the traffic-to-conversion "
            "funnel, and increasingly by how well physical and online channels "
            "operate as one."
        ),
        "business_objectives": [
            {"id": "revenue-comps", "name": "Revenue & Comparable Sales Growth",
             "strategic_focus": "Grow sales across channels and the existing store base",
             "kpis": ["Total revenue growth", "Comparable / like-for-like sales (comps)", "Sales per square foot", "Online sales growth"]},
            {"id": "gross-margin", "name": "Gross Margin & Profitability",
             "strategic_focus": "Protect margin and earnings quality",
             "kpis": ["Gross margin %", "Merchandise margin", "Markdown rate", "Operating / EBIT margin"]},
            {"id": "acquisition-traffic", "name": "Customer Acquisition & Traffic",
             "strategic_focus": "Drive traffic and win new customers",
             "kpis": ["Foot traffic", "Web traffic / sessions", "New customers", "Customer Acquisition Cost (CAC)"]},
            {"id": "retention-loyalty", "name": "Retention & Loyalty",
             "strategic_focus": "Increase repeat purchase and lifetime value",
             "kpis": ["Repeat purchase rate", "Loyalty enrollment & penetration", "Customer Lifetime Value (CLV)", "Retention rate"]},
            {"id": "conversion-basket", "name": "Conversion & Basket",
             "strategic_focus": "Convert demand and grow basket size",
             "kpis": ["Conversion rate", "Average Order Value (AOV)", "Units Per Transaction (UPT)", "Attach rate"]},
            {"id": "inventory-supply", "name": "Inventory & Supply Chain Efficiency",
             "strategic_focus": "Maximize inventory productivity and availability",
             "kpis": ["Inventory turnover", "Sell-through rate", "GMROI", "Out-of-stock rate", "Shrinkage"]},
            {"id": "omnichannel", "name": "Omnichannel Integration",
             "strategic_focus": "Operate stores and digital as one",
             "kpis": ["% sales omnichannel", "BOPIS / click-and-collect adoption", "Ship-from-store rate", "Online-offline blend"]},
            {"id": "operational-efficiency", "name": "Operational Efficiency",
             "strategic_focus": "Lower cost-to-serve and fulfill",
             "kpis": ["Cost per order / fulfillment cost", "Labor cost %", "SG&A ratio", "Order accuracy"]},
            {"id": "customer-experience", "name": "Customer Experience",
             "strategic_focus": "Differentiate on service and ease",
             "kpis": ["NPS", "CSAT", "Return rate", "On-time delivery", "Review ratings"]},
        ],
        "strategic_tensions": [
            {"name": "Promotion vs. margin", "description": "Discounting lifts comparable sales and clears inventory but erodes gross margin."},
            {"name": "Availability vs. carrying cost", "description": "Too much inventory drives markdowns; too little drives stockouts and lost sales."},
            {"name": "Online growth vs. store margin", "description": "Online growth can cannibalize higher-margin store sales while carrying higher fulfillment cost. GMROI is the discipline that ties margin to inventory productivity."},
        ],
        "digital_strategy": {
            "framing": "Digital is the connective tissue of modern retail, not a separate channel. It widens reach, personalizes the experience, and unifies inventory and the customer relationship across stores and online.",
            "levers": [
                {"area": "Acquisition", "description": "Digital marketing, marketplaces and social commerce widen reach and improve marketing efficiency."},
                {"area": "Conversion", "description": "Personalization, search and recommendations raise conversion rate and average order value."},
                {"area": "Omnichannel", "description": "BOPIS, ship-from-store and unified inventory blend channels and turn stores into fulfillment nodes."},
                {"area": "Supply chain", "description": "Demand forecasting and real-time inventory visibility cut stockouts and markdowns."},
                {"area": "Loyalty", "description": "Apps and data-driven CRM lift repeat purchase rate and customer lifetime value."},
            ],
            "digital_kpis": ["E-commerce sales penetration (% digital)", "Online conversion rate", "App adoption / MAU", "BOPIS / click-and-collect adoption", "Digital marketing ROAS", "Personalization-driven revenue", "Real-time inventory visibility coverage"],
        },
    },
    {
        "id": "media-entertainment",
        "name": "Media & Entertainment",
        "overview": (
            "Media and entertainment businesses compete for audience attention "
            "and then monetize it through subscriptions, advertising, or both. "
            "Engagement is the leading indicator of retention and monetization, "
            "while content investment is the largest cost and the primary growth "
            "driver."
        ),
        "business_objectives": [
            {"id": "audience-growth", "name": "Subscriber / Audience Growth",
             "strategic_focus": "Grow reach and the subscriber base",
             "kpis": ["Subscriber net adds", "Total subscribers / MAU", "Reach", "Market share"]},
            {"id": "engagement", "name": "Engagement",
             "strategic_focus": "Maximize attention and consumption",
             "kpis": ["Time spent / watch time", "DAU/MAU ratio", "Consumption per user", "Session frequency"]},
            {"id": "retention", "name": "Retention",
             "strategic_focus": "Reduce churn and extend lifetime",
             "kpis": ["Churn rate", "Retention / renewal rate", "Subscriber lifetime"]},
            {"id": "monetization", "name": "Monetization & Revenue",
             "strategic_focus": "Grow revenue per user and in total",
             "kpis": ["ARPU", "Subscription revenue", "Advertising revenue", "Total revenue growth"]},
            {"id": "content-roi", "name": "Content ROI & Effectiveness",
             "strategic_focus": "Spend content dollars efficiently",
             "kpis": ["Content cost efficiency", "Engagement per dollar", "Hit rate", "% engagement from originals"]},
            {"id": "advertising", "name": "Advertising Effectiveness",
             "strategic_focus": "Maximize ad yield on ad-supported tiers",
             "kpis": ["Ad revenue", "CPM", "Fill rate", "Viewability", "Ad-load tolerance"]},
            {"id": "profitability", "name": "Profitability",
             "strategic_focus": "Convert scale into margin",
             "kpis": ["Contribution margin", "Content amortization efficiency", "Operating margin"]},
            {"id": "brand-experience", "name": "Brand & Experience",
             "strategic_focus": "Strengthen affinity and discovery",
             "kpis": ["NPS", "Satisfaction", "Recommendation relevance"]},
        ],
        "strategic_tensions": [
            {"name": "Content spend vs. margin", "description": "More content investment drives engagement and growth but pressures margin, and hit-driven economics make returns uncertain."},
            {"name": "Subscription vs. advertising experience", "description": "Subscription and advertising models pull in different directions on ad load and experience. Engagement per content dollar is the discipline that ties strategy together."},
        ],
        "digital_strategy": {
            "framing": "Digital platforms are the distribution, data and monetization engine for modern media. Personalization and data-driven decisions determine which content gets made, watched, retained and monetized.",
            "levers": [
                {"area": "Discovery", "description": "Recommendation engines lift engagement and reduce churn."},
                {"area": "Distribution", "description": "Direct-to-consumer platforms own the audience relationship and its data."},
                {"area": "Content decisions", "description": "Viewing data informs greenlighting and content-ROI discipline."},
                {"area": "Monetization", "description": "Programmatic and addressable advertising raise digital ad yield."},
                {"area": "Experience", "description": "Streaming quality and personalization improve satisfaction and retention."},
            ],
            "digital_kpis": ["Recommendation-driven engagement %", "Personalization lift", "Cross-platform reach", "Digital ad yield", "Streaming quality-of-experience"],
        },
    },
    {
        "id": "b2b-saas",
        "name": "B2B SaaS",
        "overview": (
            "In B2B SaaS, value compounds through recurring revenue, so "
            "retention and expansion matter as much as new acquisition. The most "
            "important strategic question is whether net revenue retention and "
            "unit economics support efficient, durable growth."
        ),
        "business_objectives": [
            {"id": "recurring-revenue", "name": "Recurring Revenue Growth",
             "strategic_focus": "Grow ARR durably",
             "kpis": ["ARR / MRR growth", "New ARR", "Growth rate"]},
            {"id": "acquisition", "name": "Customer Acquisition",
             "strategic_focus": "Win new logos efficiently",
             "kpis": ["New logos", "CAC", "Win rate", "Pipeline conversion", "Magic number"]},
            {"id": "retention-expansion", "name": "Retention & Expansion",
             "strategic_focus": "Keep and grow existing accounts",
             "kpis": ["Net Revenue Retention (NRR)", "Gross Revenue Retention (GRR)", "Logo churn", "Expansion ARR"]},
            {"id": "customer-success", "name": "Customer Success & Adoption",
             "strategic_focus": "Drive value realization",
             "kpis": ["Product adoption / active usage", "Time-to-value", "Customer health score", "CSAT / NPS"]},
            {"id": "unit-economics", "name": "Unit Economics & Efficiency",
             "strategic_focus": "Grow profitably and capital-efficiently",
             "kpis": ["CAC payback period", "LTV / CAC ratio", "Rule of 40", "Sales efficiency"]},
            {"id": "plg", "name": "Product-Led Growth & Engagement",
             "strategic_focus": "Convert usage into revenue",
             "kpis": ["Activation rate", "Product-Qualified Leads (PQLs)", "Free-to-paid conversion", "Engagement / stickiness (DAU/MAU)"]},
            {"id": "profitability", "name": "Profitability & Cash",
             "strategic_focus": "Balance growth with burn",
             "kpis": ["Gross margin", "Burn multiple", "FCF margin", "Rule of 40"]},
            {"id": "market-expansion", "name": "Market Expansion",
             "strategic_focus": "Extend into new segments and geos",
             "kpis": ["TAM penetration", "ACV growth", "New segment / geo revenue"]},
        ],
        "strategic_tensions": [
            {"name": "Growth vs. efficiency", "description": "Reconciled through the Rule of 40 (growth rate plus profit margin >= 40%). Acquisition spend pulls against CAC payback discipline; the goal is efficient growth, not growth at any cost."},
            {"name": "New logos vs. retention leverage", "description": "Net revenue retention above 100% means the installed base grows even without new logos, making retention the highest-leverage objective."},
        ],
        "digital_strategy": {
            "framing": "For B2B SaaS the product is the digital channel, so digital strategy is really go-to-market and product motion: how self-serve, sales-led and product-led approaches combine, and how data and AI differentiate the offering.",
            "levers": [
                {"area": "Product-led growth", "description": "Self-serve signup and in-product activation lower CAC and seed expansion."},
                {"area": "Onboarding", "description": "Automated onboarding shortens time-to-value and improves retention."},
                {"area": "Expansion", "description": "Usage data and in-app prompts surface upsell at the point of value."},
                {"area": "Differentiation", "description": "Embedded AI and analytics raise stickiness and willingness to pay."},
                {"area": "Ecosystem", "description": "Integrations and platform APIs deepen switching costs and reach."},
            ],
            "digital_kpis": ["Self-serve signup conversion", "PLG-sourced ARR %", "In-product activation rate", "Onboarding automation rate", "Feature adoption depth"],
        },
    },
    {
        "id": "travel-hospitality",
        "name": "Travel & Hospitality",
        "overview": (
            "Travel and hospitality businesses manage perishable capacity, so "
            "success depends on filling inventory at the right price, owning the "
            "customer relationship through loyalty, and earning ancillary "
            "revenue. Yield and distribution mix are as important as occupancy "
            "itself."
        ),
        "business_objectives": [
            {"id": "revenue-yield", "name": "Revenue Growth & Yield",
             "strategic_focus": "Optimize price and demand for perishable inventory",
             "kpis": ["RevPAR", "Average Daily Rate (ADR)", "Occupancy rate", "Load factor (air)", "Total revenue growth"]},
            {"id": "demand-bookings", "name": "Demand & Bookings Growth",
             "strategic_focus": "Drive and convert demand",
             "kpis": ["Booking volume", "Direct booking share", "Conversion rate", "Market share"]},
            {"id": "loyalty", "name": "Loyalty",
             "strategic_focus": "Own the customer relationship",
             "kpis": ["Loyalty enrollment & penetration", "Repeat guest rate", "Member revenue share", "NPS"]},
            {"id": "customer-experience", "name": "Customer Experience",
             "strategic_focus": "Deliver consistent, high-rated stays and journeys",
             "kpis": ["Guest satisfaction (GSS)", "NPS", "Online review scores", "Complaint resolution"]},
            {"id": "operational-efficiency", "name": "Operational Efficiency",
             "strategic_focus": "Protect margin on each unit sold",
             "kpis": ["Cost per occupied room", "Labor cost %", "GOPPAR", "On-time performance (air)"]},
            {"id": "ancillary-revenue", "name": "Ancillary Revenue",
             "strategic_focus": "Grow revenue beyond the core unit",
             "kpis": ["Ancillary revenue per guest", "Upsell / cross-sell attach rate", "F&B / spa revenue"]},
            {"id": "distribution", "name": "Distribution & Channel Mix",
             "strategic_focus": "Shift mix toward profitable channels",
             "kpis": ["Direct vs. OTA mix", "Distribution / acquisition cost", "Channel contribution"]},
            {"id": "capacity-utilization", "name": "Asset & Capacity Utilization",
             "strategic_focus": "Maximize use of fixed capacity",
             "kpis": ["Occupancy", "Load factor", "Asset utilization"]},
        ],
        "strategic_tensions": [
            {"name": "Rate vs. occupancy", "description": "Discounting fills rooms or seats but erodes RevPAR and yield. Disciplined revenue management optimizes total profitability, not any one occupancy or rate figure."},
            {"name": "Direct booking vs. marketing cost", "description": "Direct-booking strategies reduce OTA commissions but require marketing investment to replace that demand."},
            {"name": "Loyalty value vs. redemption cost", "description": "Loyalty programs build lifetime value yet carry redemption cost."},
        ],
        "digital_strategy": {
            "framing": "Digital owns the modern travel journey from inspiration to in-stay service. It is the principal lever for shifting demand to direct channels, personalizing offers, and lifting ancillary revenue.",
            "levers": [
                {"area": "Direct demand", "description": "Owned apps and sites shift share away from costly OTAs."},
                {"area": "Pricing", "description": "Dynamic pricing and AI revenue management optimize yield in real time."},
                {"area": "Experience", "description": "Mobile check-in, keyless entry and digital concierge reduce friction."},
                {"area": "Personalization", "description": "Data-driven offers raise conversion and ancillary attach rates."},
                {"area": "Loyalty", "description": "App-based programs deepen engagement and repeat booking."},
            ],
            "digital_kpis": ["Direct digital booking share", "App adoption", "Mobile check-in rate", "Digital conversion rate", "Personalization-driven revenue lift"],
        },
    },
]


def build():
    return {
        "schema_version": SCHEMA_VERSION,
        "description": (
            "Vendor-agnostic cross-industry objective layer for the Account "
            "Intelligence Engine. Each industry carries its business "
            "objectives, the KPIs leaders track, the strategic tensions "
            "between those objectives, and how digital strategy maps onto "
            "them. This layer contains no vendor, product, or client data."
        ),
        "industry_count": len(INDUSTRIES),
        "industries": INDUSTRIES,
    }


def main():
    out_dir = Path(__file__).parent.parent / "data"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "objective_layer.json"
    payload = build()
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    obj = sum(len(i["business_objectives"]) for i in INDUSTRIES)
    kpis = sum(len(o["kpis"]) for i in INDUSTRIES for o in i["business_objectives"])
    tensions = sum(len(i["strategic_tensions"]) for i in INDUSTRIES)
    print(f"Wrote {out_path}")
    print(f"  industries: {len(INDUSTRIES)}")
    print(f"  business objectives: {obj}")
    print(f"  KPIs: {kpis}")
    print(f"  strategic tensions: {tensions}")


if __name__ == "__main__":
    main()
