# HK620 Public Claim Boundary

Title: HK620 Public Claim Boundary
Knowledge Type: Compliance / QA Rule
Product: HK620
Source: Gap Task hk620_gap_010 + Post 481 Publication Process
Review Status: approved
Approval Date: 2026-07-29
Approved By: CEO

## Summary

HK620 公开宣传边界文档。Website Agent 和 Content Operator 在生成公开内容时必须遵守此清单。QA Agent 用此清单拦截违规内容。

## Prohibited Public Claims

The following claims are NOT allowed in any public-facing content:

### 1. Customer Identity

- **Prohibited:** Real customer company names
- **Allowed:** Anonymized references (e.g., "a Dongguan door factory")
- **Reason:** Customer names not authorized for public disclosure

### 2. Market Position Claims

- **Prohibited:** "Industry first" / "industry only" / "absolute best" / "number one" / "唯一" / "第一"
- **Allowed:** Factual product descriptions (e.g., "dedicated skeleton-line edge banding machine")
- **Reason:** Cannot substantiate market position claims

### 3. Quantified Efficiency Claims

- **Prohibited:** Specific efficiency improvement percentages (e.g., "increases efficiency by 30%")
- **Allowed:** Qualitative descriptions (e.g., "improved batch repeatability," "reduced manual repair")
- **Reason:** No verified benchmark data

### 4. ROI / Profit / Revenue Claims

- **Prohibited:** ROI figures, profit margins, revenue impact, cost savings percentages
- **Allowed:** Qualitative value descriptions (e.g., "reduce rework," "improve customer confidence")
- **Reason:** No financial data approved for public use

### 5. Pricing

- **Prohibited:** Specific prices, price ranges, discounts
- **Allowed:** "Contact for quotation" / "Request a configuration review"
- **Reason:** Pricing is case-by-case based on configuration

### 6. Unvalidated Technical Parameters

- **Prohibited:** 38-45 degree angle specifications (not validated)
- **Prohibited:** Servo upgrade timeline or roadmap details (internal only)
- **Allowed:** Only parameters listed in 02_Technical_Specifications/hk620_technical_specifications_v1.md
- **Reason:** Unvalidated parameters may mislead buyers

### 7. Warranty Claims

- **Prohibited:** Specific warranty terms, durations, or coverage without service team review
- **Allowed:** General statement that HK620 has entered batch production
- **Reason:** Warranty policy not yet documented for public use

### 8. Competitive Comparison

- **Prohibited:** Direct competitor naming or comparison claims
- **Allowed:** General category comparison (e.g., "unlike standard panel edge banding machines")
- **Reason:** Cannot substantiate competitive claims without verified data

## Allowed Public Claims (Quick Reference)

| Claim | Allowed? | Source |
|---|---|---|
| HK620 uses PUR glue | Yes | Post 481 |
| Feed speed 18 m/min | Yes | Post 481 |
| Min workpiece width 70mm | Yes | Post 481 |
| Packaging 8.3m x 0.9m x 1.6m | Yes | Post 481 |
| Approx. 3 months development + 3 months testing | Yes | Post 481 |
| Entered batch production | Yes | Post 481 |
| 3 anonymized customer references | Yes | Post 481 |
| Delta control system | Yes | Post 481 |
| 380V / 20kW / 0.6 MPa | Yes | Post 481 |
| Machine length approx. 7.5m, weight approx. 3 tons | Yes | Post 481 |
| Delivery cycle approx. 30 days | Yes | Post 481 |
| Real customer names | **No** | CEO directive |
| Efficiency percentages | **No** | No verified data |
| ROI / profit claims | **No** | No financial data |
| 38-45 degree specs | **No** | Not validated |
| Servo roadmap details | **No** | Internal only |

## QA Agent Usage

QA Agent should check all generated content against this boundary before allowing publication. Any violation should block the content and flag it for review.

## Source References

- Gap Task: hk620_gap_010_public_claim_boundary
- Published Article: Post 481
- CEO Directives: 2026-07-29 (customer names anonymized, specs confirmed)
