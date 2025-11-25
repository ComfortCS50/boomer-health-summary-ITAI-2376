"""
Agent 1: Extractor
Extracts key medical information from clinical notes

Team: Oyinade Balogun, Hilary C Bruton, Glen Sam, Kaleb
Course: ITAI 2376 - Boomer Health Summary Project
"""

import re
from typing import Dict, List, Optional

class MedicalExtractor:
    """
    Agent 1: Extracts diagnoses, medications, symptoms, instructions, 
    and follow-up needs from clinical notes.
    """
    
    def __init__(self):
        """Initialize the extractor with medical keyword patterns"""
        
        # Common diagnosis keywords
        self.diagnosis_keywords = [
            'hypertension', 'diabetes', 'hyperlipidemia', 'copd', 
            'asthma', 'arthritis', 'depression', 'anxiety',
            'heart disease', 'coronary artery disease', 'cad',
            'chronic kidney disease', 'ckd', 'obesity', 'anemia',
            'pneumonia', 'bronchitis', 'infection', 'fracture'
        ]
        
        # Common medication patterns
        self.medication_patterns = [
            r'\b(metformin|lisinopril|atorvastatin|amlodipine|metoprolol)\b',
            r'\b(omeprazole|levothyroxine|albuterol|gabapentin|losartan)\b',
            r'\b(hydrochlorothiazide|sertraline|ibuprofen|aspirin|warfarin)\b',
            r'\b(\w+)\s*\d+\s*mg\b',  # Matches "drugname 50 mg"
            r'\b(\w+)\s*tablet\b',     # Matches "drugname tablet"
        ]
        
        # Symptom keywords
        self.symptom_keywords = [
            'pain', 'fever', 'cough', 'fatigue', 'weakness',
            'shortness of breath', 'sob', 'chest pain', 'headache',
            'nausea', 'vomiting', 'dizziness', 'swelling', 'rash',
            'difficulty breathing', 'confusion', 'bleeding'
        ]
        
        # Instruction indicators
        self.instruction_indicators = [
            'take', 'continue', 'stop', 'increase', 'decrease',
            'monitor', 'check', 'follow up', 'return', 'call',
            'avoid', 'exercise', 'diet', 'rest'
        ]
        
        # Follow-up indicators
        self.followup_indicators = [
            'follow up', 'return', 'appointment', 'see doctor',
            'recheck', 'monitor', 'call if', 'seek care',
            'emergency', 'schedule'
        ]
    
    def extract_all(self, clinical_note: str) -> Dict[str, List[str]]:
        """
        Main extraction method - extracts all medical information
        
        Args:
            clinical_note: Raw clinical note text
            
        Returns:
            Dictionary with extracted diagnoses, medications, symptoms,
            instructions, and follow-ups
        """
        
        # Clean the note
        note_lower = clinical_note.lower()
        
        # Extract each category
        extracted_data = {
            'diagnoses': self.extract_diagnoses(note_lower),
            'medications': self.extract_medications(clinical_note),  # Use original for case sensitivity
            'symptoms': self.extract_symptoms(note_lower),
            'instructions': self.extract_instructions(note_lower),
            'followups': self.extract_followups(note_lower),
            'flagged_terms': self.flag_ambiguous_terms(note_lower)
        }
        
        return extracted_data
    
    def extract_diagnoses(self, note: str) -> List[str]:
        """Extract diagnoses from clinical note"""
        diagnoses = []
        
        for diagnosis in self.diagnosis_keywords:
            if diagnosis in note:
                # Capitalize first letter for readability
                diagnoses.append(diagnosis.title())
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(diagnoses))
    
    def extract_medications(self, note: str) -> List[str]:
        """Extract medications from clinical note"""
        medications = []
        note_lower = note.lower()
        
        # Check each medication pattern
        for pattern in self.medication_patterns:
            matches = re.findall(pattern, note_lower, re.IGNORECASE)
            medications.extend(matches)
        
        # Clean up and capitalize
        medications = [med.strip().title() for med in medications if med.strip()]
        
        # Remove duplicates and common false positives
        medications = [med for med in medications if len(med) > 2]
        return list(dict.fromkeys(medications))
    
    def extract_symptoms(self, note: str) -> List[str]:
        """Extract symptoms from clinical note"""
        symptoms = []
        
        for symptom in self.symptom_keywords:
            if symptom in note:
                symptoms.append(symptom.title())
        
        return list(dict.fromkeys(symptoms))
    
    def extract_instructions(self, note: str) -> List[str]:
        """Extract patient instructions from clinical note"""
        instructions = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]', note)
        
        # Find sentences with instruction indicators
        for sentence in sentences:
            for indicator in self.instruction_indicators:
                if indicator in sentence.lower():
                    cleaned = sentence.strip()
                    if len(cleaned) > 10:  # Avoid very short fragments
                        instructions.append(cleaned.capitalize())
                    break  # Only add sentence once
        
        return list(dict.fromkeys(instructions))
    
    def extract_followups(self, note: str) -> List[str]:
        """Extract follow-up instructions"""
        followups = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]', note)
        
        # Find sentences with follow-up indicators
        for sentence in sentences:
            for indicator in self.followup_indicators:
                if indicator in sentence.lower():
                    cleaned = sentence.strip()
                    if len(cleaned) > 10:
                        followups.append(cleaned.capitalize())
                    break
        
        return list(dict.fromkeys(followups))
    
    def flag_ambiguous_terms(self, note: str) -> List[str]:
        """
        Flag medical abbreviations or terms that might need clarification
        This helps Agent 2 know what to explain more carefully
        """
        ambiguous_patterns = [
            r'\b[A-Z]{2,}\b',  # All-caps abbreviations (e.g., COPD, CAD)
            r'\b\d+/\d+\b',     # Ratios like blood pressure
        ]
        
        flagged = []
        for pattern in ambiguous_patterns:
            matches = re.findall(pattern, note)
            flagged.extend(matches)
        
        return list(dict.fromkeys(flagged))[:5]  # Limit to top 5
    
    def format_output(self, extracted_data: Dict[str, List[str]]) -> str:
        """
        Format extracted data into readable text for Agent 2
        
        Args:
            extracted_data: Dictionary from extract_all()
            
        Returns:
            Formatted string summary
        """
        output = []
        output.append("=" * 50)
        output.append("AGENT 1: EXTRACTED MEDICAL INFORMATION")
        output.append("=" * 50)
        output.append("")
        
        # Diagnoses
        if extracted_data['diagnoses']:
            output.append("DIAGNOSES:")
            for dx in extracted_data['diagnoses']:
                output.append(f"  - {dx}")
            output.append("")
        
        # Medications
        if extracted_data['medications']:
            output.append("MEDICATIONS:")
            for med in extracted_data['medications']:
                output.append(f"  - {med}")
            output.append("")
        
        # Symptoms
        if extracted_data['symptoms']:
            output.append("SYMPTOMS:")
            for symptom in extracted_data['symptoms']:
                output.append(f"  - {symptom}")
            output.append("")
        
        # Instructions
        if extracted_data['instructions']:
            output.append("INSTRUCTIONS:")
            for instruction in extracted_data['instructions']:
                output.append(f"  - {instruction}")
            output.append("")
        
        # Follow-ups
        if extracted_data['followups']:
            output.append("FOLLOW-UP NEEDS:")
            for followup in extracted_data['followups']:
                output.append(f"  - {followup}")
            output.append("")
        
        # Flagged terms
        if extracted_data['flagged_terms']:
            output.append("TERMS NEEDING CLARIFICATION:")
            for term in extracted_data['flagged_terms']:
                output.append(f"  - {term}")
            output.append("")
        
        output.append("=" * 50)
        
        return "\n".join(output)


# Example usage and testing
if __name__ == "__main__":
    # Create extractor instance
    extractor = MedicalExtractor()
    
    # Test with sample clinical note
    sample_note = """
    Patient presents with hypertension and type 2 diabetes. 
    Chief complaints include chest pain and shortness of breath.
    Current medications: Lisinopril 10mg daily, Metformin 500mg twice daily.
    Blood pressure: 145/92. A1C: 7.8%.
    
    Assessment: Poorly controlled hypertension and diabetes.
    
    Plan:
    - Increase Lisinopril to 20mg daily
    - Continue Metformin
    - Monitor blood pressure daily
    - Follow up in 2 weeks
    - Call if chest pain worsens
    - Schedule appointment with cardiologist
    """
    
    # Extract information
    print("Testing Agent 1: Medical Extractor\n")
    extracted = extractor.extract_all(sample_note)
    
    # Display formatted output
    print(extractor.format_output(extracted))
    
    # Also show raw dictionary (useful for Agent 2)
    print("\nRaw extracted data (for Agent 2):")
    for key, values in extracted.items():
        print(f"{key}: {values}")
