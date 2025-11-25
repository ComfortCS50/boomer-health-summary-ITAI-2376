"""
Agent 1: Medical Extractor
Extracts key medical information from discharge papers, prescriptions, and after-visit summaries

Team:Oyinade Balogun, Hilary C Bruton, Glen Sam, Kaleb
Course: ITAI 2376 - Boomer Health Summary Project
"""

import re
from typing import Dict, List, Optional
import json

class MedicalExtractor:
    """
    Agent 1: Extracts diagnoses, medications, symptoms, instructions, 
    and follow-up needs from patient medical documents.
    
    Designed for: Discharge papers, after-visit summaries, prescriptions
    """
    
    def __init__(self):
        """Initialize the extractor with medical keyword patterns"""
        
        # Common diagnoses that appear in discharge papers
        self.diagnosis_keywords = [
            'hypertension', 'high blood pressure', 'diabetes', 'type 2 diabetes',
            'hyperlipidemia', 'high cholesterol', 'copd', 'asthma', 'arthritis',
            'depression', 'anxiety', 'heart disease', 'coronary artery disease', 'cad',
            'chronic kidney disease', 'ckd', 'obesity', 'anemia', 'pneumonia',
            'congestive heart failure', 'chf', 'atrial fibrillation', 'afib',
            'stroke', 'heart attack', 'myocardial infarction', 'bronchitis',
            'infection', 'fracture', 'osteoporosis', 'gerd', 'reflux'
        ]
        
        # Medication name patterns
        self.medication_patterns = [
            # Common medications by name
            r'\b(metformin|lisinopril|atorvastatin|amlodipine|metoprolol)\b',
            r'\b(omeprazole|levothyroxine|albuterol|gabapentin|losartan)\b',
            r'\b(hydrochlorothiazide|sertraline|ibuprofen|aspirin|warfarin)\b',
            r'\b(furosemide|lasix|prednisone|insulin|lantus|humalog)\b',
            # Pattern: "drugname dosage" (e.g., "Lisinopril 10mg")
            r'\b([A-Z][a-z]+)\s+\d+\s*mg\b',
            # Pattern: "drugname tablet/capsule"
            r'\b([A-Z][a-z]+)\s+(tablet|capsule|pill)\b',
        ]
        
        # Symptom keywords
        self.symptom_keywords = [
            'pain', 'chest pain', 'back pain', 'abdominal pain',
            'fever', 'cough', 'fatigue', 'weakness', 'tired',
            'shortness of breath', 'sob', 'difficulty breathing',
            'headache', 'dizziness', 'nausea', 'vomiting',
            'swelling', 'edema', 'rash', 'confusion', 'bleeding',
            'numbness', 'tingling', 'constipation', 'diarrhea'
        ]
        
        # Instruction indicators (what patient should DO)
        self.instruction_indicators = [
            'take', 'continue', 'stop', 'discontinue', 'increase', 'decrease',
            'monitor', 'check', 'measure', 'weigh', 'record',
            'follow up', 'return', 'call', 'contact',
            'avoid', 'limit', 'reduce', 'restrict',
            'exercise', 'walk', 'diet', 'eat', 'drink', 'rest', 'elevate'
        ]
        
        # Follow-up and appointment indicators
        self.followup_indicators = [
            'follow up', 'follow-up', 'return', 'appointment', 'see doctor',
            'see your doctor', 'visit', 'schedule', 'recheck', 'monitor',
            'call if', 'contact if', 'seek care', 'emergency', 'urgent',
            'in 1 week', 'in 2 weeks', 'in one month', 'next week'
        ]
    
    def extract_all(self, document_text: str, input_method: str = "unknown") -> Dict:
        """
        Main extraction method - extracts all medical information
        
        Args:
            document_text: Raw text from discharge paper, prescription, or user input
            input_method: "photo_ocr", "free_text", or "guided_form"
            
        Returns:
            Dictionary with extracted information ready for Agent 2
        """
        
        # Clean the document
        text_lower = document_text.lower()
        
        # Extract each category
        extracted_data = {
            'input_method': input_method,
            'diagnoses': self.extract_diagnoses(text_lower),
            'medications': self.extract_medications(document_text),
            'symptoms': self.extract_symptoms(text_lower),
            'instructions': self.extract_instructions(text_lower),
            'followups': self.extract_followups(text_lower),
            'test_results': self.extract_test_results(document_text),
            'flagged_terms': self.flag_medical_abbreviations(document_text),
            'raw_text_preview': document_text[:200] + "..." if len(document_text) > 200 else document_text
        }
        
        # Add quality score
        extracted_data['extraction_quality'] = self.assess_extraction_quality(extracted_data)
        
        return extracted_data
    
    def extract_diagnoses(self, text: str) -> List[str]:
        """Extract diagnoses from document"""
        diagnoses = []
        
        for diagnosis in self.diagnosis_keywords:
            if diagnosis in text:
                # Capitalize for readability
                diagnoses.append(diagnosis.title())
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(diagnoses))
    
    def extract_medications(self, text: str) -> List[Dict[str, str]]:
        """
        Extract medications with dosages
        Returns list of dicts with 'name' and 'dosage' keys
        """
        medications = []
        text_lower = text.lower()
        
        # Find medication names and dosages
        for pattern in self.medication_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            
            for match in matches:
                if isinstance(match, tuple):
                    med_name = match[0] if match[0] else match
                else:
                    med_name = match
                
                # Try to find dosage near this medication
                dosage = self.find_dosage_for_medication(med_name, text)
                
                medications.append({
                    'name': med_name.strip().title(),
                    'dosage': dosage
                })
        
        # Remove duplicates
        seen = set()
        unique_meds = []
        for med in medications:
            med_key = med['name'].lower()
            if med_key not in seen and len(med['name']) > 2:
                seen.add(med_key)
                unique_meds.append(med)
        
        return unique_meds
    
    def find_dosage_for_medication(self, med_name: str, text: str) -> str:
        """Try to find dosage information for a medication"""
        # Look for dosage pattern near the medication name
        pattern = rf'{med_name}[:\s]+(\d+\s*mg|\d+\s*mcg|\d+\s*units?)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            return match.group(1)
        
        return "See prescription"
    
    def extract_symptoms(self, text: str) -> List[str]:
        """Extract symptoms patient experienced"""
        symptoms = []
        
        for symptom in self.symptom_keywords:
            if symptom in text:
                symptoms.append(symptom.title())
        
        return list(dict.fromkeys(symptoms))
    
    def extract_instructions(self, text: str) -> List[str]:
        """Extract patient instructions from document"""
        instructions = []
        
        # Split into sentences
        sentences = re.split(r'[.!?\n]', text)
        
        # Find sentences with instruction indicators
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short fragments
                continue
                
            for indicator in self.instruction_indicators:
                if indicator in sentence.lower():
                    # Capitalize first letter
                    cleaned = sentence[0].upper() + sentence[1:] if sentence else sentence
                    instructions.append(cleaned)
                    break  # Only add sentence once
        
        return list(dict.fromkeys(instructions))
    
    def extract_followups(self, text: str) -> List[str]:
        """Extract follow-up appointment information"""
        followups = []
        
        # Split into sentences
        sentences = re.split(r'[.!?\n]', text)
        
        # Find sentences with follow-up indicators
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
                
            for indicator in self.followup_indicators:
                if indicator in sentence.lower():
                    cleaned = sentence[0].upper() + sentence[1:] if sentence else sentence
                    followups.append(cleaned)
                    break
        
        return list(dict.fromkeys(followups))
    
    def extract_test_results(self, text: str) -> List[Dict[str, str]]:
        """
        Extract test results (blood pressure, lab values, etc.)
        """
        results = []
        
        # Blood pressure pattern (e.g., "BP: 140/90" or "Blood pressure 130/85")
        bp_pattern = r'(?:BP|blood pressure)[:\s]+(\d{2,3}/\d{2,3})'
        bp_matches = re.findall(bp_pattern, text, re.IGNORECASE)
        for bp in bp_matches:
            results.append({'test': 'Blood Pressure', 'value': bp})
        
        # A1C pattern (e.g., "A1C: 7.5%" or "HbA1c 6.8")
        a1c_pattern = r'(?:A1C|HbA1c)[:\s]+(\d+\.?\d*)\s*%?'
        a1c_matches = re.findall(a1c_pattern, text, re.IGNORECASE)
        for a1c in a1c_matches:
            results.append({'test': 'A1C (Diabetes)', 'value': f"{a1c}%"})
        
        # Weight pattern
        weight_pattern = r'(?:weight|wt)[:\s]+(\d+)\s*(?:lbs?|pounds?)'
        weight_matches = re.findall(weight_pattern, text, re.IGNORECASE)
        for weight in weight_matches:
            results.append({'test': 'Weight', 'value': f"{weight} lbs"})
        
        return results
    
    def flag_medical_abbreviations(self, text: str) -> List[str]:
        """
        Flag medical abbreviations that Agent 2 should explain
        """
        # Common medical abbreviations
        abbreviations = [
            'BP', 'HR', 'RR', 'O2', 'SpO2', 'CHF', 'COPD', 'CAD', 'MI', 
            'CVA', 'TIA', 'DM', 'HTN', 'CKD', 'GERD', 'AFIB', 'UTI',
            'SOB', 'DOE', 'CP', 'HA', 'N/V', 'BM', 'PRN', 'QD', 'BID', 'TID'
        ]
        
        found = []
        for abbrev in abbreviations:
            # Look for abbreviation as whole word
            pattern = rf'\b{abbrev}\b'
            if re.search(pattern, text):
                found.append(abbrev)
        
        return found[:8]  # Limit to top 8
    
    def assess_extraction_quality(self, extracted_data: Dict) -> str:
        """
        Assess how complete the extraction was
        Returns: "high", "medium", or "low"
        """
        score = 0
        
        # Check what we found
        if extracted_data['diagnoses']:
            score += 2
        if extracted_data['medications']:
            score += 2
        if extracted_data['instructions']:
            score += 1
        if extracted_data['followups']:
            score += 1
        
        if score >= 5:
            return "high"
        elif score >= 3:
            return "medium"
        else:
            return "low"
    
    def to_json(self, extracted_data: Dict) -> str:
        """Convert extracted data to JSON for Agent 2"""
        return json.dumps(extracted_data, indent=2)
    
    def format_for_display(self, extracted_data: Dict) -> str:
        """
        Format extracted data for human-readable display
        """
        output = []
        output.append("=" * 60)
        output.append("AGENT 1: MEDICAL INFORMATION EXTRACTED")
        output.append("=" * 60)
        output.append(f"Input Method: {extracted_data['input_method']}")
        output.append(f"Extraction Quality: {extracted_data['extraction_quality'].upper()}")
        output.append("")
        
        # Diagnoses
        if extracted_data['diagnoses']:
            output.append("📋 DIAGNOSES FOUND:")
            for dx in extracted_data['diagnoses']:
                output.append(f"   • {dx}")
            output.append("")
        
        # Medications
        if extracted_data['medications']:
            output.append("💊 MEDICATIONS:")
            for med in extracted_data['medications']:
                output.append(f"   • {med['name']} - {med['dosage']}")
            output.append("")
        
        # Test Results
        if extracted_data['test_results']:
            output.append("🔬 TEST RESULTS:")
            for test in extracted_data['test_results']:
                output.append(f"   • {test['test']}: {test['value']}")
            output.append("")
        
        # Symptoms
        if extracted_data['symptoms']:
            output.append("🤒 SYMPTOMS NOTED:")
            for symptom in extracted_data['symptoms']:
                output.append(f"   • {symptom}")
            output.append("")
        
        # Instructions
        if extracted_data['instructions']:
            output.append("📝 INSTRUCTIONS:")
            for instruction in extracted_data['instructions'][:5]:  # Limit to 5
                output.append(f"   • {instruction}")
            output.append("")
        
        # Follow-ups
        if extracted_data['followups']:
            output.append("📅 FOLLOW-UP NEEDED:")
            for followup in extracted_data['followups']:
                output.append(f"   • {followup}")
            output.append("")
        
        # Flagged abbreviations
        if extracted_data['flagged_terms']:
            output.append("⚠️  MEDICAL TERMS TO EXPLAIN (for Agent 2):")
            output.append(f"   {', '.join(extracted_data['flagged_terms'])}")
            output.append("")
        
        output.append("=" * 60)
        output.append("Ready to send to Agent 2 (Health Explainer)")
        output.append("=" * 60)
        
        return "\n".join(output)


# Example usage and testing
if __name__ == "__main__":
    # Create extractor instance
    extractor = MedicalExtractor()
    
    # Test with sample discharge paper
    sample_discharge_paper = """
    DISCHARGE SUMMARY
    Patient: John Smith | Age: 68 | Date: Nov 24, 2025
    
    DIAGNOSES:
    1. Congestive Heart Failure (CHF)
    2. Hypertension
    3. Type 2 Diabetes
    
    VITAL SIGNS:
    Blood Pressure: 145/92
    Weight: 215 lbs
    A1C: 7.8%
    
    MEDICATIONS PRESCRIBED:
    - Furosemide 40mg - Take once daily in the morning
    - Lisinopril 20mg - Take once daily
    - Metformin 500mg - Take twice daily with meals
    
    SYMPTOMS ON ADMISSION:
    - Shortness of breath
    - Swelling in legs
    - Fatigue
    
    INSTRUCTIONS:
    - Weigh yourself every morning before breakfast
    - Call doctor if weight increases by 3 pounds in one day
    - Limit sodium to 2000mg per day
    - Avoid salty foods like chips, canned soup, deli meats
    - Walk 10-15 minutes daily if able
    - Monitor blood pressure at home daily
    
    FOLLOW-UP:
    - Schedule appointment with cardiologist within 1 week
    - Return to primary care in 2 weeks
    - Call office if shortness of breath worsens or chest pain develops
    
    EMERGENCY SIGNS:
    Seek immediate care for: severe chest pain, extreme shortness of breath,
    confusion, or sudden weight gain of 5+ pounds.
    """
    
    # Extract information
    print("Testing Agent 1: Medical Extractor")
    print("Input: Sample Discharge Paper\n")
    
    extracted = extractor.extract_all(sample_discharge_paper, input_method="photo_ocr")
    
    # Display formatted output
    print(extractor.format_for_display(extracted))
    
    # Show JSON format (what gets sent to Agent 2)
    print("\n\nJSON FORMAT (sent to Agent 2):")
    print(extractor.to_json(extracted))
