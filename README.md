# Boomer Health Summary Multi-Agent System

**Course:** ITAI 2376 - Deep Learning  
**Team Members:** Oyinade Balogun, Hilary C Bruton, Glen Sam, Kaleb  
**Project Option:** Option 3 - Multi-Agent Collaborative System

## Project Overview

A patient-facing multi-agent system that helps older adults ("Boomers") understand their medical paperwork by transforming complex discharge summaries, prescriptions, and after-visit notes into simple, actionable health guidance.

### The Problem We're Solving

Many patients;especially older adults, struggle to understand:
- Discharge paperwork
- After-visit summaries  
- Prescription instructions
- Medical portal notes

This leads to:
- Confusion about diagnoses
- Missed medication instructions
- Failure to follow treatment plans
- Not knowing what to ask at follow-up appointments

### Our Solution

An intelligent system that accepts medical documents through **three input methods**:
1. **Photo Upload** - Take a picture of discharge papers (OCR extracts text)
2. **Free Text Entry** - Type what you remember from the visit
3. **Guided Form** - Fill in structured fields

Then our multi-agent system transforms this into:
-  Plain-language explanations
-  Actionable lifestyle recommendations
-  Questions to ask your doctor
-  Warning signs to watch for

## Multi-Agent Architecture

### Agent 1: Medical Extractor
**Role:** Extracts key medical information from documents

**Extracts:**
- Diagnoses
- Medications (with dosages)
- Symptoms
- Doctor's instructions
- Follow-up appointments
- Test results

**Output:** Structured JSON data for other agents

---

### Agent 2: Health Explainer
**Role:** Converts medical terminology into patient-friendly language

**Examples:**
- "Hyperlipidemia" → "High cholesterol - your body has too much fat in the blood, which can increase heart risk. It's very manageable with lifestyle changes and medication."
- "Hypertension" → "High blood pressure - your heart is working harder than it should. Think of it like a garden hose with too much pressure."

**Output:** Plain-language explanations with context

---

### Agent 3: Lifestyle & Action Coach
**Role:** Provides actionable, non-medical-advice guidance

**Provides:**
- **Diet Tips:** "For high cholesterol, try adding more vegetables, fish, and oats to your meals"
- **Exercise Suggestions:** "Start with 10-minute walks, gradually building up"
- **Questions for Doctor:** "Ask: What should my cholesterol target be? When should I recheck?"
- **Warning Signs:** "Call your doctor if: chest pain, severe dizziness, shortness of breath"

**Important:** Does NOT provide medical diagnosis or treatment advice - only educational guidance

---

### Agent 4: Report Builder (Optional)
**Role:** Assembles everything into a clean, organized final summary

**Output Sections:**
1. What the Doctor Said (extracted info)
2. What It Means (plain language)
3. What You Should Do (action items)
4. Questions for Next Visit
5. Warning Signs
6. Medical Terms Glossary

## Input Processing Methods

### Method 1: Photo Upload (OCR)
```
User uploads photo of:
├── Discharge summary
├── After-visit notes
├── Prescription printout
└── Medical portal screenshot

→ OCR extracts text
→ Agent 1 processes
```

### Method 2: Free Text Entry
```
User types in their own words:
"Doctor said I have high blood pressure and gave me lisinopril 10mg..."

→ Agent 1 extracts key info
```

### Method 3: Guided Form
```
Structured fields:
├── Diagnosis: [____]
├── Medications: [____]
├── Instructions: [____]
└── Follow-up: [____]

→ Pre-structured for Agent 1
```

## Tool Integration

### Tool 1: OCR (Document Processing)
- **Library:** Tesseract OCR / Google Cloud Vision API
- **Purpose:** Extract text from uploaded photos
- **Error Handling:** If OCR fails → ask user to re-upload or use text entry

### Tool 2: Vector Database (Optional)
- **Purpose:** Store medical term definitions and explanations
- **Benefit:** Fast lookup for common conditions

### Tool 3: Web Search (Optional Enhancement)
- **Purpose:** Verify standard medical explanations
- **Usage:** Agent 2 searches for credible health information when needed

## Reinforcement Learning Elements

### Feedback Mechanism
After receiving their summary, users rate:
- **Clarity** (1-5 stars)
- **Helpfulness** (1-5 stars)  
- **Completeness** (Yes/No)

### Reward System
- **Positive feedback** → System saves successful explanation patterns
- **Negative feedback** → System adjusts wording/formatting and regenerates

### Policy Improvement
Over multiple uses:
- Agent 2 learns which explanations are clearest
- Agent 3 learns which action items are most helpful
- System improves summary formatting based on user preferences

## Safety & Security Measures

### Input Validation
 Detects missing critical information  
 Flags potentially harmful queries  
 Recognizes unsupported medical content  

### Boundary Enforcement
**The system will NOT:**
-  Provide medical diagnosis
-  Recommend specific treatments
-  Replace doctor consultations
-  Handle emergency situations

**The system WILL:**
-  Explain medical terms in plain language
-  Provide general educational information
-  Suggest lifestyle tips (diet, exercise)
-  Help prepare questions for doctors

### Fallback Strategies
- **Image unreadable** → Suggest text entry or guided form
- **Missing information** → Ask clarifying questions
- **Tool failure** → Continue with available information
- **Emergency keywords detected** → Display "Call 911" message

### Transparency
Every output includes disclaimers:
> "This information is educational only and does not replace medical advice. Always consult your healthcare provider for medical decisions."

## Development Timeline

| Date | Task |
|------|------|
| Nov 24-26 | Create system skeleton, implement input methods, build Agent 1 |
| Nov 27-29 | Implement Agent 2 (Health Explainer) and Agent 3 (Lifestyle Coach) |
| Nov 30-Dec 1 | Add user feedback loop, integrate all agents |
| Dec 2-3 | Add safety measures, create test cases, produce sample outputs |
| Dec 4-5 | Write final report, record demonstration video |
| Dec 6 | **Final submission** |

## Testing Approach

### Test Cases
We will create fake medical documents representing:
1. Diabetes discharge summary
2. Hypertension after-visit notes
3. Post-surgery instructions
4. Multiple medication prescriptions

### Evaluation Metrics
- **Extraction Accuracy:** Did Agent 1 correctly identify all key information?
- **Explanation Clarity:** Are medical terms explained in understandable language?
- **Actionability:** Do users know what to do next?
- **Safety Compliance:** Does system maintain appropriate boundaries?

## Technical Stack

- **Language:** Python 3.8+
- **OCR:** Tesseract / pytesseract (or Google Cloud Vision)
- **NLP:** Basic regex and keyword extraction (Phase 1)
- **Optional:** spaCy for enhanced extraction (Phase 2)
- **Development:** Google Colab
- **Version Control:** Git/GitHub

## Sample Use Case

**Scenario:** 75-year-old patient receives discharge papers after hospital visit

**Input:** Patient's daughter uploads photo of discharge summary

**Agent 1 Extracts:**
- Diagnosis: Congestive Heart Failure (CHF)
- Medication: Furosemide 40mg daily
- Instructions: Low sodium diet, daily weight checks
- Follow-up: Cardiologist in 1 week

**Agent 2 Explains:**
- "CHF means your heart isn't pumping as efficiently as it should. This causes fluid to build up in your body."

**Agent 3 Provides Actions:**
- "Weigh yourself every morning. Call doctor if you gain 3+ pounds in a day."
- "Avoid salty foods like chips, canned soup, deli meats."
- "Questions to ask: What weight change should worry me? What are signs of worsening?"

**Final Output:** Clean, organized summary the patient can understand and act on

## Project Status

- [x] Proposal submitted
- [ ] Agent 1 (Extractor) - In Progress
- [ ] Agent 2 (Health Explainer) - Not Started  
- [ ] Agent 3 (Lifestyle Coach) - Not Started
- [ ] OCR Integration - Not Started
- [ ] User Feedback Loop - Not Started
- [ ] Final Testing - Not Started
- [ ] Documentation - Not Started
- [ ] Demo Video - Not Started

**Target Completion:** December 6, 2025

## Disclaimers

**Important Medical Disclaimer:**

This system provides **educational information only**. It does NOT:
- Diagnose medical conditions
- Prescribe treatments
- Replace professional medical advice
- Handle medical emergencies

**Always consult your healthcare provider for medical decisions.**

## License

Educational project for ITAI 2376. Not intended for commercial use or actual medical deployment without proper regulatory approval.

## Contact

For questions about this project, contact team members through the course portal.

---

**Built with ❤️ to help patients better understand their healthcare**
