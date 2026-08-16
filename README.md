# AC Transit Line 51A: GTFS-Realtime Delay & Headway Reliability Analysis

An empirical study evaluating transit reliability, bottleneck propagation, and schedule adherence along AC Transit's Line 51A corridor in Oakland, CA. By logging real-time GTFS prediction feeds, this project isolates physical traffic bottlenecks along Broadway from operational service gaps.

---

## Executive Summary

Line 51A is one of AC Transit's heaviest-ridership corridors, connecting Downtown Oakland, Alameda, and Rockridge. This study analyzes real-time arrival predictions logged at 5-minute intervals to evaluate two distinct failure modes:
1. **Physical Corridor Bottlenecks (Daytime):** Traffic signal congestion and high passenger dwell times along the Broadway corridor cause localized travel time spikes during peak hours.
2. **Operational Headway Variance (Evening):** Off-peak delays are driven primarily by schedule gap widening (bunching and gapping) rather than road congestion.

---

## Key Findings & Visualizations

### 1. Daytime Corridor Bottlenecks
During daytime peak hours, travel time variance concentrates along specific segments of Broadway. Real-time predictions indicate significant speed degradation around major signalized intersections and high-occupancy boardings.

![Daytime Bottlenecks]

* **Impact:** Signal delay and dwell variance accumulate sequentially along Broadway, creating localized travel time spikes that ripple down the line.
* **Policy Takeaway:** Targeted transit signal priority (TSP) and queue jumps along Broadway offer higher marginal performance gains than route-wide schedule padding.

### 2. Evening Arrival Headway Outliers
Analysis of evening arrivals demonstrates that off-peak delays transition from speed degradation to irregular headways.

![Evening Headways]

* **Impact:** Arrival interval distributions widen significantly in the evening, leading to long headway gaps followed by closely space arrivals (bus bunching).
* **Policy Takeaway:** Evening performance issues stem from dispatch recovery times and terminal departures rather than corridor traffic congestion.

---

## Data Pipeline & Methodology

Rather than relying purely on static schedules or raw, high-frequency GPS coordinate dumps, this project tracks real-time GTFS prediction updates to measure expected arrival times against polling timestamps.
