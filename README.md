📱 Mobile App Event Tracking Dashboard (Python)
---
Project Overview
---
A Python project simulating and analyzing a mobile app event tracking dataset across iOS and Android platforms for 2,000 users over 60 days. Modeled after real-world mobile instrumentation plans used with tools like Segment, Amplitude, and Firebase, this project calculates key mobile product health metrics — including DAU/MAU stickiness, onboarding funnel completion, and feature adoption rates — and assembles them into a multi-panel analytics dashboard.

📊 Key Analytical Insights
---
1. The Onboarding Funnel Loses More Than Half of Users Before Completion
The mobile onboarding funnel dropped by over 50% between the first step (app opened) and the final step (first share sent), with the sharpest single drop occurring between profile completion and first event created.
The Evidence: While 78% of users who opened the app started onboarding, only 38% reached the first share step — a loss of more than half the potential activated user base across just four steps.
Takeaway: The drop between profile completion and first event created is the highest-priority fix in the onboarding flow. This single step represents the largest volume of users abandoning before reaching the product's core value moment. A targeted redesign of this transition would have the highest expected impact on activation rates.
2. The Product Exceeded the B2B SaaS Stickiness Benchmark
The DAU/MAU stickiness ratio confirmed the product was performing above the 20% threshold considered healthy for B2B SaaS products.
The Evidence: iOS users made up 58% of the active user base vs. 42% Android, consistent with typical B2B mobile app platform distributions. High-engagement users (top quartile) averaged active sessions on 75-95% of available days, contributing disproportionately to the DAU figure.
Takeaway: Strong stickiness signals that users who activate are returning regularly. The growth opportunity is less about improving retention for engaged users and more about increasing the number of users who reach activation in the first place — reinforcing the onboarding funnel finding above.
---
🔍 Methodology
---
Event Instrumentation & Technical Implementation
Event Taxonomy Design: Defined a 12-event tracking plan across 5 funnel stages (Acquisition, Activation, Engagement, Expansion, Monetization), mirroring how a real mobile analytics instrumentation plan would be structured before engineering implementation.
User Segmentation: Assigned each of 2,000 simulated users an engagement tier (dormant, low, medium, high) that governed their activity frequency and event firing probability, creating a realistic distribution of user behavior patterns.
Event Log Generation: Simulated a 60-day event log where each active user fires events based on their engagement tier and the relative probability weight of each event, producing a dataset that reflects real mobile analytics data structure.
Mobile Metrics Calculation:
DAU: Counted unique users firing any event per day across the full 60-day window.
MAU: Counted unique users active within each calendar month.
Stickiness (DAU/MAU): Calculated the ratio for the most recent complete month.
Onboarding Funnel: Measured unique users reaching each step as a percentage of total app opens.
Feature Adoption: Calculated the percentage of all active users who had ever fired each core feature event.
Dashboard Assembly: Built a 6-panel matplotlib dashboard combining DAU trend, platform split, onboarding funnel, feature adoption rates, event volume by stage, and a KPI summary panel.

📁 Files
---
File	Description
`mobile_event_analytics.py`	Full instrumentation and analysis script
`outputs/07_mobile_dashboard.png`	6-panel mobile analytics dashboard
`outputs/mobile_event_log.csv`	Raw event log (user ID, date, event name, platform)

🛠️ Tools & Libraries
---
Tool	Purpose
Python	Core programming language
pandas	Event log aggregation and metric calculation
numpy	Data simulation and numerical operations
matplotlib	Multi-panel dashboard visualization

📖 Glossary of Metrics
---
Event Instrumentation: The process of defining which user actions to track inside an app (button clicks, feature usage, page views) and setting up the logging that records each action as a data point.
Event Taxonomy: The organized catalog of all trackable events in a product, grouped by funnel stage, with standardized naming conventions.
DAU (Daily Active Users): The number of unique users who perform at least one action in the app on a given day.
MAU (Monthly Active Users): The number of unique users who perform at least one action in the app within a calendar month.
Stickiness (DAU/MAU): The ratio of average daily active users to monthly active users. Expressed as a percentage; higher values indicate users return more frequently. A ratio above 20% is considered healthy for B2B SaaS products.
Onboarding Funnel: The sequence of steps a new user must complete to reach the product's core value moment. Drop-off at each step is tracked to identify friction points.
Feature Adoption Rate: The percentage of active users who have used a specific product feature at least once. Low adoption rates signal discovery or usability problems.
Activation: The moment a user completes enough of the onboarding flow to experience the core value of the product for the first time.

Data Source
---
All data is synthetically generated using Python's `numpy` and `random` libraries to simulate realistic mobile app event tracking behavior across iOS and Android platforms.
