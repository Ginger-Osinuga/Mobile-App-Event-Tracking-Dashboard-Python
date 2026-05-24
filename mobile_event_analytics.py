# =============================================================================
# Mobile App Event Tracking and Funnel Dashboard
# =============================================================================
# What this project does:
#   - Simulates a realistic mobile event tracking dataset (iOS and Android)
#     with the kinds of events a product analyst would instrument and analyze
#   - Analyzes user behavior across key mobile events: app open, onboarding
#     steps, feature usage, and conversion
#   - Calculates mobile-specific metrics: DAU/MAU ratio (stickiness),
#     session frequency, and feature adoption rates
#   - Builds a multi-panel dashboard summarizing mobile product health
#
# Why this matters for product analytics roles:
#   The job description specifically asks for "familiarity with mobile product
#   metrics, event instrumentation, and mobile experimentation frameworks."
#   This project directly addresses that requirement.
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime, timedelta
import random
import os

np.random.seed(55)
random.seed(55)
os.makedirs("outputs", exist_ok=True)

print("=" * 60)
print("PROJECT 4: Mobile App Event Tracking Dashboard")
print("=" * 60)


# -----------------------------------------------------------------------------
# STEP 1: Define the event taxonomy
# -----------------------------------------------------------------------------
# In a real product, these events would be defined in a tracking plan and
# instrumented by engineers via a tool like Segment, Amplitude, or Firebase.

MOBILE_EVENTS = {
    # Onboarding funnel
    "app_opened":             {"stage": "acquisition",  "weight": 1.00},
    "onboarding_started":     {"stage": "activation",   "weight": 0.78},
    "profile_completed":      {"stage": "activation",   "weight": 0.61},
    "first_event_created":    {"stage": "activation",   "weight": 0.49},
    "first_share_sent":       {"stage": "activation",   "weight": 0.38},
    # Core feature usage
    "calendar_synced":        {"stage": "engagement",   "weight": 0.55},
    "meeting_scheduled":      {"stage": "engagement",   "weight": 0.44},
    "reminder_set":           {"stage": "engagement",   "weight": 0.32},
    "integration_connected":  {"stage": "engagement",   "weight": 0.22},
    "team_member_invited":    {"stage": "expansion",    "weight": 0.18},
    # Conversion
    "upgrade_viewed":         {"stage": "monetization", "weight": 0.25},
    "upgrade_completed":      {"stage": "monetization", "weight": 0.12},
}

PLATFORMS = ["iOS", "Android"]
PLATFORM_SPLIT = [0.58, 0.42]   # iOS slightly dominant


# -----------------------------------------------------------------------------
# STEP 2: Generate synthetic event log
# -----------------------------------------------------------------------------
# We create 2,000 users with 60 days of event history.
# Each user fires events based on their engagement level.

NUM_USERS    = 2000
DAYS_OF_DATA = 60
start_date   = datetime(2024, 3, 1)

users = []
for uid in range(1, NUM_USERS + 1):
    platform    = random.choices(PLATFORMS, weights=PLATFORM_SPLIT)[0]
    signup_date = start_date + timedelta(days=random.randint(0, 30))
    # engagement score: 0=dormant, 1=low, 2=medium, 3=high
    engagement  = random.choices([0, 1, 2, 3], weights=[0.20, 0.30, 0.30, 0.20])[0]
    users.append({"user_id": uid, "platform": platform,
                  "signup_date": signup_date, "engagement": engagement})

users_df = pd.DataFrame(users)

# Generate event log
event_log = []
for _, user in users_df.iterrows():
    uid        = user["user_id"]
    platform   = user["platform"]
    signup     = user["signup_date"]
    engagement = user["engagement"]

    active_days = min(DAYS_OF_DATA, (start_date + timedelta(days=DAYS_OF_DATA) - signup).days)
    # Higher engagement = more active days
    days_active = random.randint(
        max(1, int(active_days * [0.05, 0.15, 0.40, 0.75][engagement])),
        max(2, int(active_days * [0.15, 0.40, 0.70, 0.95][engagement]))
    )
    active_day_offsets = sorted(random.sample(range(active_days), min(days_active, active_days)))

    for day_offset in active_day_offsets:
        event_date = signup + timedelta(days=day_offset)
        if event_date > start_date + timedelta(days=DAYS_OF_DATA):
            continue

        # Higher engagement = more events per session
        session_events = random.randint(1, [2, 4, 7, 12][engagement])

        for _ in range(session_events):
            # Pick an event weighted by its probability
            event_names   = list(MOBILE_EVENTS.keys())
            event_weights = [MOBILE_EVENTS[e]["weight"] * ([0.3, 0.6, 0.85, 1.0][engagement])
                             for e in event_names]
            event_name = random.choices(event_names, weights=event_weights)[0]

            event_log.append({
                "user_id":    uid,
                "platform":   platform,
                "event_name": event_name,
                "event_date": event_date.date(),
                "event_stage": MOBILE_EVENTS[event_name]["stage"],
            })

events_df = pd.DataFrame(event_log)
print(f"\nEvent log created: {len(events_df):,} events from {NUM_USERS:,} users")
print(f"Date range: {events_df['event_date'].min()} to {events_df['event_date'].max()}")
print(f"\nEvent counts:\n{events_df['event_name'].value_counts().to_string()}")


# -----------------------------------------------------------------------------
# STEP 3: Key mobile metrics
# -----------------------------------------------------------------------------

print("\n--- KEY MOBILE METRICS ---")

# Daily Active Users (DAU)
dau = events_df.groupby("event_date")["user_id"].nunique().reset_index()
dau.columns = ["date", "dau"]

# Monthly Active Users (MAU)
events_df["month"] = pd.to_datetime(events_df["event_date"]).dt.to_period("M")
mau = events_df.groupby("month")["user_id"].nunique()

# DAU/MAU stickiness (using last full month)
last_month_dau = dau[pd.to_datetime(dau["date"]).dt.to_period("M") == mau.index[-1]]["dau"].mean()
last_month_mau = mau.iloc[-1]
stickiness     = last_month_dau / last_month_mau
print(f"Average DAU (last month): {last_month_dau:.0f}")
print(f"MAU (last month):         {last_month_mau:,}")
print(f"Stickiness (DAU/MAU):     {stickiness:.1%}  (>20% is healthy for B2B SaaS)")

# Platform split
platform_users = events_df.groupby("platform")["user_id"].nunique()
print(f"\nActive users by platform:\n{platform_users.to_string()}")

# Onboarding funnel completion
print("\n--- MOBILE ONBOARDING FUNNEL ---")
onboarding_events = [
    "app_opened", "onboarding_started", "profile_completed",
    "first_event_created", "first_share_sent"
]
funnel_counts = {}
for ev in onboarding_events:
    funnel_counts[ev] = events_df[events_df["event_name"] == ev]["user_id"].nunique()

print(f"\n{'Event':<28} {'Users':>8} {'Drop from prev':>16} {'vs app_opened':>14}")
print("-" * 70)
prev = None
for ev, cnt in funnel_counts.items():
    from_prev = f"{cnt/prev*100:.1f}%" if prev else "---"
    from_top  = f"{cnt/funnel_counts['app_opened']*100:.1f}%"
    print(f"{ev:<28} {cnt:>8,} {from_prev:>16} {from_top:>14}")
    prev = cnt

# Feature adoption
print("\n--- FEATURE ADOPTION RATES ---")
feature_events = ["calendar_synced", "meeting_scheduled", "reminder_set",
                   "integration_connected", "team_member_invited"]
total_active = events_df["user_id"].nunique()
for ev in feature_events:
    users_who_did = events_df[events_df["event_name"] == ev]["user_id"].nunique()
    print(f"  {ev:<28}: {users_who_did:,} users ({users_who_did/total_active:.1%})")


# -----------------------------------------------------------------------------
# STEP 4: Multi-panel dashboard
# -----------------------------------------------------------------------------

fig = plt.figure(figsize=(16, 11))
fig.suptitle("Mobile App Analytics Dashboard", fontsize=16, fontweight="bold", y=0.98)

# Panel 1: DAU over time
ax1 = fig.add_subplot(2, 3, 1)
dau_plot = dau.copy()
dau_plot["date"] = pd.to_datetime(dau_plot["date"])
ax1.fill_between(dau_plot["date"], dau_plot["dau"], alpha=0.3, color="#2563A8")
ax1.plot(dau_plot["date"], dau_plot["dau"], color="#2563A8", linewidth=1.8)
ax1.set_title("Daily Active Users (DAU)", fontsize=11, fontweight="bold")
ax1.set_ylabel("Users", fontsize=9)
ax1.tick_params(axis="x", rotation=30, labelsize=7)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Panel 2: Platform split pie
ax2 = fig.add_subplot(2, 3, 2)
platform_data = events_df.groupby("platform")["user_id"].nunique()
ax2.pie(platform_data, labels=platform_data.index, autopct="%1.1f%%",
        colors=["#2563A8", "#6FA3E8"], startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2})
ax2.set_title("Users by Platform", fontsize=11, fontweight="bold")

# Panel 3: Onboarding funnel
ax3 = fig.add_subplot(2, 3, 3)
funnel_labels = [e.replace("_", " ").title() for e in funnel_counts.keys()]
funnel_vals   = list(funnel_counts.values())
colors_funnel = ["#2563A8", "#3B7DD8", "#5A95E0", "#7AACE8", "#A8C8F0"]
bars = ax3.barh(funnel_labels[::-1], funnel_vals[::-1], color=colors_funnel, height=0.55)
for bar, val in zip(bars, funnel_vals[::-1]):
    ax3.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
             f"{val:,}", va="center", fontsize=8)
ax3.set_title("Onboarding Funnel (Unique Users)", fontsize=11, fontweight="bold")
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)

# Panel 4: Feature adoption
ax4 = fig.add_subplot(2, 3, 4)
feat_labels  = [e.replace("_", " ").replace("connected", "conn.").title()
                for e in feature_events]
feat_vals    = [events_df[events_df["event_name"] == e]["user_id"].nunique()
                / total_active * 100 for e in feature_events]
bar_colors4  = ["#2563A8" if v >= np.mean(feat_vals) else "#A8C8F0" for v in feat_vals]
bars4 = ax4.bar(feat_labels, feat_vals, color=bar_colors4, width=0.55)
for bar, val in zip(bars4, feat_vals):
    ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
             f"{val:.1f}%", ha="center", va="bottom", fontsize=8)
ax4.set_ylabel("% of Active Users", fontsize=9)
ax4.set_title("Feature Adoption Rate", fontsize=11, fontweight="bold")
ax4.tick_params(axis="x", rotation=25, labelsize=7)
ax4.spines["top"].set_visible(False)
ax4.spines["right"].set_visible(False)

# Panel 5: Events by stage
ax5 = fig.add_subplot(2, 3, 5)
stage_counts = events_df.groupby("event_stage").size().sort_values(ascending=True)
stage_colors = {"acquisition": "#A8C8F0", "activation": "#6FA3E8",
                "engagement": "#3B7DD8", "expansion": "#2563A8",
                "monetization": "#1A3F6F"}
bar_colors5 = [stage_colors.get(s, "#888888") for s in stage_counts.index]
stage_counts.plot(kind="barh", ax=ax5, color=bar_colors5)
ax5.set_title("Event Volume by Funnel Stage", fontsize=11, fontweight="bold")
ax5.set_xlabel("Total Events", fontsize=9)
ax5.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax5.spines["top"].set_visible(False)
ax5.spines["right"].set_visible(False)

# Panel 6: KPI summary box
ax6 = fig.add_subplot(2, 3, 6)
ax6.axis("off")
kpis = [
    ("Total Active Users",      f"{total_active:,}"),
    ("Avg Daily Active Users",  f"{dau['dau'].mean():.0f}"),
    ("DAU/MAU Stickiness",      f"{stickiness:.1%}"),
    ("Onboarding Completion",   f"{funnel_counts['first_share_sent']/funnel_counts['app_opened']:.1%}"),
    ("iOS / Android Split",     f"{platform_data['iOS']/platform_data.sum():.0%} / {platform_data['Android']/platform_data.sum():.0%}"),
    ("Total Events Logged",     f"{len(events_df):,}"),
]
y_pos = 0.90
for label, value in kpis:
    ax6.text(0.05, y_pos, label, transform=ax6.transAxes,
             fontsize=10, color="#555555")
    ax6.text(0.95, y_pos, value, transform=ax6.transAxes,
             fontsize=11, fontweight="bold", color="#1A3F6F", ha="right")
    ax6.plot([0.02, 0.98], [y_pos - 0.06, y_pos - 0.06], color="#E0E8F0",
                linewidth=0.8, transform=ax6.transAxes)
    y_pos -= 0.14
ax6.set_title("Key Performance Indicators", fontsize=11, fontweight="bold")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("outputs/07_mobile_dashboard.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nDashboard saved: outputs/07_mobile_dashboard.png")

events_df.to_csv("outputs/mobile_event_log.csv", index=False)
print("Event log saved: outputs/mobile_event_log.csv")

print("\n" + "=" * 60)
print("Project complete. All outputs saved to outputs/")
print("=" * 60)
