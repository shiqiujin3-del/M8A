# Website Agent V2 Upgrade Design

> **Date:** 2026-07-30  
> **Author:** WorkBuddy (CEO directive)  
> **Status:** Design Complete, Ready for Implementation  
> **Baseline:** V1 (Sprint 2 Day 1, 329-word draft, QA 92)  
> **Target:** V2 (Post 481 quality, QA 95+, 800+ words, publish-ready)

---

## 1. What Changed

### 1.1 Knowledge Binding V1 → V2

| Dimension | V1 | V2 |
|-----------|----|----|
| Spec coverage | 0/5 (all missing) | 8/8 (all public_approved) |
| Image coverage | 0 images | 2 images (WP ID 479, 480) |
| Public approval | not_public_approved | public_approved (Post 481) |
| FAQ | 3 internal-only | 6 public_approved |
| Customer cases | 0 | 3 anonymized |
| Internal links | 3 local paths | 4 URLs (product page, contact, Post 481, knowledge) |
| Coverage | 55% internal, 0% public | 85% public approved |
| Content standard | None | Post 481 as golden standard reference |

**File:** `knowledge_binding/hk620.knowledge_binding.v2.json`

### 1.2 QA Checklist V2 → V2.1

| Dimension | V2 | V2.1 |
|-----------|----|----|
| Tiers | Single (90 pass) | Two-tier: Draft-Ready (90) + Publish-Ready (95) |
| Pending handling | No deduction | Half-weight deduction |
| Checks | 14 items | 16 items (added Specs Table + Customer Evidence) |
| Publish gate | QA 90 → could publish | QA 95 + zero P0 pending → can publish |
| Word count | 300+ pass | Draft: 300+, Publish: 800+ |
| Golden standard | None | Post 481 (QA ~97 equivalent) |

**File:** `qa/website_agent_qa_v2.1.checklist.json`

### 1.3 Execution Chain V1 → V2 (planned)

| Step | V1 (8 steps) | V2 (10 steps) |
|------|-------------|---------------|
| 1 | Mission Intake | Mission Intake |
| 2 | Knowledge Fetch | Knowledge Fetch (V2 binding) |
| 3 | Draft Generation | Topic Map & Content Planning |
| 4 | SEO Enrichment | Draft Generation (Post 481 template) |
| 5 | QA V2 Scoring | SEO Enrichment |
| 6 | Approval Gate | Image & Media Attachment |
| 7 | Draft-only Handoff | QA V2.1 Scoring (two-tier) |
| 8 | Mission Log Writeback | Approval Gate |
| 9 | — | Draft-only Handoff (with Schema injection) |
| 10 | — | Mission Log Writeback |

**New steps:**
- **Topic Map & Content Planning** — Aligns with Content Center 10-step pipeline
- **Image & Media Attachment** — Attaches images from knowledge binding to draft

### 1.4 Content Template Upgrade

V1 template produced: 329 words, no specs table, no images, no schema.

V2 template (based on Post 481) produces:

```
H1: [Product Name] for [Application]
├── Overview (100-150 words: buyer problem + product solution)
├── [Image: product-image-1 with alt text]
├── H2: Specifications
│   └── Table: 8+ parameters from knowledge binding
├── H2: Applications
│   └── List: 4 application scenarios
├── [Image: product-image-2 with alt text]
├── H2: Frequently Asked Questions
│   └── 6 Q&A from knowledge binding FAQ
├── H2: Next Steps
│   ├── CTA Button 1: Product Page link
│   └── CTA Button 2: Contact Page link
└── SEO Meta: title, description, slug, schema
```

**Target:** 800+ words, QA 95+, publish-ready.

---

## 2. Implementation Checklist

- [x] Knowledge Binding V2 created (`hk620.knowledge_binding.v2.json`)
- [x] QA V2.1 Checklist created (`website_agent_qa_v2.1.checklist.json`)
- [x] V2 Upgrade Design document (this file)
- [x] Update execution chain to V2 (10 steps) → `execution_chain/website_agent_execution_chain.v2.json`
- [x] Update state machine for two-tier QA gates → `state_machine/website_agent_state_machine.v2.json`
- [x] Update prompt templates with Post 481 golden standard (integrated into execution chain Step 4)
- [x] Test run: generate a new article with V2 binding and QA V2.1 (HK620 Cabinet Factory, 1378 words, 100/100 QA)
- [x] Compare V2 output against Post 481 quality (V2: 100/100 vs Post 481: 97/100, V2 exceeds gold standard)

---

## 3. Expected Impact

| Metric | V1 (Sprint 2 Day 1) | V2 Expected |
|--------|--------------------|----|
| Word count | 329 | 800+ |
| QA Score | 92 (3 pending) | 95+ (0 P0 pending) |
| Specs table | Missing | Complete (8 parameters) |
| Images | 0 | 2 (from binding) |
| FAQ | 3 generic | 6 specific from knowledge base |
| Internal links | 0 | 2+ (product page + contact) |
| Schema | Missing | Injected |
| CTA | Text only | Dual buttons (product + contact) |
| Publish-ready | No | Yes (with CEO approval) |

---

## 4. Safety Boundary (Unchanged)

V2 maintains all V1 safety boundaries:
- No auto-publish
- No auto-delete
- No auto-update published posts
- CEO approval required for all external actions
- Draft-only handoff requires separate authorization

The upgrade improves content **quality**, not **autonomy**. Autonomy upgrades come with Mission Queue auto-scan (10-step plan item #7).
