"""
Agent 3: Lifestyle & Action Coach
Provides actionable lifestyle recommendations and questions for the doctor

Team: Oyinade Balogun, Hilary C Bruton, Glen Sam, Kaleb
Course: ITAI 2376 - Boomer Health Summary Project
"""

import json
from typing import Dict, List

class LifestyleCoach:
    """
    Agent 3: Provides non-medical-advice actionable guidance including:
    - Diet and nutrition tips
    - Exercise suggestions
    - Daily habits to monitor
    - Questions to ask the doctor
    - Warning signs to watch for
    """
    
    def __init__(self):
        """Initialize with condition-specific lifestyle recommendations"""
        
        # Lifestyle recommendations by diagnosis
        self.lifestyle_recommendations = {
            'hypertension': {
                'diet': [
                    "Reduce sodium (salt) to less than 2,300mg per day",
                    "Eat more fruits, vegetables, and whole grains (DASH diet)",
                    "Limit alcohol to 1-2 drinks per day maximum",
                    "Avoid processed foods, canned soups, and deli meats (high sodium)",
                    "Choose fresh or frozen vegetables over canned"
                ],
                'exercise': [
                    "Aim for 30 minutes of walking most days of the week",
                    "Start slow - even 10 minutes helps",
                    "Try activities you enjoy: gardening, dancing, swimming",
                    "Check with your doctor before starting intense exercise"
                ],
                'daily_habits': [
                    "Check blood pressure at home at the same time each day",
                    "Keep a blood pressure log to share with your doctor",
                    "Take medications at the same time daily",
                    "Manage stress through deep breathing or meditation"
                ],
                'warning_signs': [
                    "Severe headache with confusion or vision changes",
                    "Chest pain or pressure",
                    "Severe shortness of breath",
                    "Blood pressure reading consistently over 180/120"
                ]
            },
            'high blood pressure': {
                'diet': [
                    "Cut back on salt - read food labels for sodium content",
                    "Eat more potassium-rich foods: bananas, potatoes, spinach",
                    "Choose whole grains over white bread and rice",
                    "Limit caffeine if it raises your blood pressure"
                ],
                'exercise': [
                    "Walk for 30 minutes most days - split into 10-minute walks if needed",
                    "Take stairs instead of elevator when possible",
                    "Do chair exercises if walking is difficult"
                ],
                'daily_habits': [
                    "Monitor your blood pressure regularly",
                    "Keep a medication schedule",
                    "Reduce stress with hobbies you enjoy"
                ],
                'warning_signs': [
                    "Sudden severe headache",
                    "Nosebleeds with high BP reading",
                    "Chest discomfort",
                    "Vision problems"
                ]
            },
            'diabetes': {
                'diet': [
                    "Eat regular meals - don't skip breakfast",
                    "Choose whole grains: brown rice, whole wheat bread, oatmeal",
                    "Fill half your plate with non-starchy vegetables",
                    "Limit sugary drinks - choose water, unsweetened tea, or coffee",
                    "Watch portion sizes - use smaller plates",
                    "Include lean protein: chicken, fish, beans, tofu"
                ],
                'exercise': [
                    "Walk after meals to help lower blood sugar",
                    "Aim for 150 minutes of activity per week (30 min x 5 days)",
                    "Check blood sugar before and after exercise",
                    "Carry a fast-acting sugar source during exercise (juice, glucose tabs)"
                ],
                'daily_habits': [
                    "Check blood sugar as your doctor recommends",
                    "Log your blood sugar readings, meals, and how you feel",
                    "Inspect your feet daily for cuts, blisters, or redness",
                    "Take medications with meals as directed",
                    "Carry diabetes identification"
                ],
                'warning_signs': [
                    "Blood sugar below 70 or above 300",
                    "Extreme thirst or frequent urination",
                    "Blurred vision",
                    "Confusion, dizziness, or shakiness (low blood sugar)",
                    "Fruity-smelling breath (very high blood sugar)"
                ]
            },
            'type 2 diabetes': {
                'diet': [
                    "Count carbohydrates or use the plate method (1/2 veggies, 1/4 protein, 1/4 carbs)",
                    "Avoid sugary desserts and sweetened beverages",
                    "Choose high-fiber foods: beans, vegetables, whole grains",
                    "Eat consistent amounts of carbs at each meal",
                    "Read nutrition labels for total carbohydrates"
                ],
                'exercise': [
                    "Be active after meals to lower blood sugar naturally",
                    "Strength training 2x per week helps muscles use insulin better",
                    "Find an exercise buddy for motivation"
                ],
                'daily_habits': [
                    "Test blood sugar as recommended by your doctor",
                    "Keep a food and blood sugar diary",
                    "Take medications on schedule",
                    "Check your feet daily"
                ],
                'warning_signs': [
                    "Blood sugar consistently over 250",
                    "Blood sugar below 70 (shakiness, sweating, confusion)",
                    "Increased thirst and urination",
                    "Unexplained weight loss",
                    "Slow-healing sores"
                ]
            },
            'high cholesterol': {
                'diet': [
                    "Eat more fiber: oatmeal, beans, apples, berries",
                    "Choose healthy fats: olive oil, avocados, nuts, fatty fish",
                    "Limit saturated fats: red meat, butter, cheese, fried foods",
                    "Avoid trans fats: many packaged baked goods",
                    "Add fatty fish twice a week: salmon, mackerel, sardines"
                ],
                'exercise': [
                    "30 minutes of moderate exercise most days",
                    "Any movement helps: walking, biking, swimming",
                    "Exercise raises 'good' HDL cholesterol"
                ],
                'daily_habits': [
                    "Take cholesterol medication as prescribed (usually at bedtime)",
                    "Read food labels for saturated and trans fats",
                    "Keep track of when you need cholesterol rechecks"
                ],
                'warning_signs': [
                    "Chest pain or pressure (possible heart attack)",
                    "Sudden weakness on one side (possible stroke)",
                    "Severe leg pain when walking (circulation problem)"
                ]
            },
            'hyperlipidemia': {
                'diet': [
                    "Increase soluble fiber: oats, barley, beans, lentils, apples",
                    "Eat omega-3 rich foods: walnuts, flaxseed, fatty fish",
                    "Replace butter with olive oil or plant-based spreads",
                    "Choose lean meats and remove skin from poultry"
                ],
                'exercise': [
                    "Aerobic exercise helps lower triglycerides",
                    "Even modest weight loss improves cholesterol levels"
                ],
                'daily_habits': [
                    "Take statin medication consistently",
                    "Don't skip doses - effectiveness decreases",
                    "Report muscle pain to your doctor immediately"
                ],
                'warning_signs': [
                    "Muscle pain, tenderness, or weakness (statin side effect)",
                    "Dark-colored urine",
                    "Chest pain or pressure"
                ]
            },
            'congestive heart failure': {
                'diet': [
                    "Limit sodium to 2,000mg or less per day",
                    "Limit fluids to what your doctor recommends (often 1.5-2 liters)",
                    "Avoid adding salt - use herbs and spices instead",
                    "Read ALL food labels for sodium content",
                    "Avoid salty snacks, pickles, olives, processed cheese"
                ],
                'exercise': [
                    "Walk or exercise as approved by your doctor",
                    "Stop if you feel short of breath or dizzy",
                    "Build up slowly - even 5 minutes helps",
                    "Cardiac rehabilitation programs can help"
                ],
                'daily_habits': [
                    "Weigh yourself every morning after using bathroom, before eating",
                    "Call doctor if you gain 2-3 pounds in one day or 5 pounds in a week",
                    "Keep legs elevated when sitting",
                    "Take diuretics (water pills) early in day",
                    "Track your daily weight"
                ],
                'warning_signs': [
                    "Sudden weight gain (3+ pounds in a day)",
                    "Increased swelling in legs, ankles, or abdomen",
                    "Worsening shortness of breath",
                    "Difficulty breathing when lying flat",
                    "Persistent cough or wheezing",
                    "Chest pain"
                ]
            },
            'chf': {
                'diet': [
                    "Strict low-sodium diet (under 2000mg daily)",
                    "Measure and limit fluids as your doctor directs",
                    "Avoid high-sodium foods: canned soups, frozen dinners, fast food"
                ],
                'exercise': [
                    "Short walks as tolerated - stop if short of breath",
                    "Rest when needed",
                    "Ask about cardiac rehab programs"
                ],
                'daily_habits': [
                    "Daily morning weigh-ins are critical",
                    "Record your weight in a log",
                    "Elevate your feet when sitting",
                    "Take water pills in the morning"
                ],
                'warning_signs': [
                    "Rapid weight gain",
                    "Cannot breathe lying down",
                    "Severe leg swelling",
                    "Extreme fatigue or weakness"
                ]
            },
            'copd': {
                'diet': [
                    "Eat smaller, more frequent meals (large meals make breathing harder)",
                    "Include protein at each meal to maintain muscle strength",
                    "Stay hydrated to thin mucus"
                ],
                'exercise': [
                    "Pulmonary rehabilitation can teach breathing exercises",
                    "Walk at your own pace - every step counts",
                    "Use pursed-lip breathing during activity"
                ],
                'daily_habits': [
                    "Use inhalers exactly as prescribed",
                    "Avoid smoke, dust, fumes, and air pollution",
                    "Get flu and pneumonia vaccines",
                    "Practice breathing exercises daily"
                ],
                'warning_signs': [
                    "Increased shortness of breath",
                    "Change in mucus color (yellow, green) or amount",
                    "Fever",
                    "Confusion or extreme fatigue",
                    "Blue lips or fingernails"
                ]
            },
            'asthma': {
                'diet': [
                    "Identify and avoid food triggers if you have any",
                    "Maintain healthy weight - obesity worsens asthma"
                ],
                'exercise': [
                    "Exercise is good for asthma control",
                    "Use inhaler 15 minutes before exercise if recommended",
                    "Warm up slowly",
                    "Swimming is often well-tolerated"
                ],
                'daily_habits': [
                    "Use controller inhaler daily even when feeling good",
                    "Keep rescue inhaler with you always",
                    "Avoid triggers: smoke, strong odors, cold air, allergens",
                    "Track symptoms and peak flow if recommended"
                ],
                'warning_signs': [
                    "Using rescue inhaler more than 2x per week",
                    "Waking at night with symptoms",
                    "Difficulty speaking full sentences",
                    "Lips or nails turning blue",
                    "No improvement after using rescue inhaler"
                ]
            },
            'arthritis': {
                'diet': [
                    "Anti-inflammatory foods: fatty fish, berries, leafy greens",
                    "Limit inflammatory foods: fried foods, refined carbs, red meat",
                    "Consider Mediterranean diet pattern",
                    "Stay hydrated"
                ],
                'exercise': [
                    "Low-impact activities: swimming, water aerobics, tai chi, cycling",
                    "Move joints through full range of motion daily",
                    "Strengthen muscles around joints",
                    "Exercise reduces pain long-term even if it's uncomfortable at first"
                ],
                'daily_habits': [
                    "Use heat before activity, ice after",
                    "Pace yourself - alternate activity with rest",
                    "Use assistive devices if helpful: cane, jar opener, reaching tools",
                    "Maintain healthy weight to reduce joint stress"
                ],
                'warning_signs': [
                    "Joint becomes hot, red, and very swollen",
                    "Sudden severe pain",
                    "Fever with joint pain",
                    "Joint pain that doesn't improve with rest"
                ]
            }
        }
        
        # Generic questions for doctor
        self.general_doctor_questions = [
            "What is my main diagnosis and what caused it?",
            "What are my treatment options?",
            "What should I do if my symptoms get worse?",
            "When should I schedule my next appointment?",
            "Are there any side effects I should watch for with my medications?",
            "What lifestyle changes are most important for my condition?",
            "When should I call your office versus going to the ER?"
        ]
    
    def generate_action_plan(self, explained_data: Dict) -> Dict:
        """
        Main method: Creates personalized action plan based on diagnoses
        
        Args:
            explained_data: Output from Agent 2
            
        Returns:
            Action plan with lifestyle tips, questions, warning signs
        """
        
        # Get diagnoses from Agent 2's output
        diagnoses = explained_data.get('original_extraction', {}).get('diagnoses', [])
        medications = explained_data.get('original_extraction', {}).get('medications', [])
        
        action_plan = {
            'diet_recommendations': self.compile_diet_tips(diagnoses),
            'exercise_recommendations': self.compile_exercise_tips(diagnoses),
            'daily_habits': self.compile_daily_habits(diagnoses),
            'warning_signs': self.compile_warning_signs(diagnoses),
            'questions_for_doctor': self.generate_doctor_questions(diagnoses, medications),
            'medication_reminders': self.generate_medication_reminders(medications),
            'encouragement': self.get_encouragement_message()
        }
        
        return action_plan
    
    def compile_diet_tips(self, diagnoses: List[str]) -> List[str]:
        """Compile relevant diet recommendations"""
        all_tips = []
        
        for diagnosis in diagnoses:
            dx_lower = diagnosis.lower()
            if dx_lower in self.lifestyle_recommendations:
                tips = self.lifestyle_recommendations[dx_lower].get('diet', [])
                all_tips.extend(tips)
        
        # Remove duplicates while preserving order
        unique_tips = list(dict.fromkeys(all_tips))
        
        # Return top 8 most important tips
        return unique_tips[:8] if unique_tips else [
            "Eat a balanced diet with plenty of vegetables and fruits",
            "Drink plenty of water throughout the day",
            "Limit processed and fast foods"
        ]
    
    def compile_exercise_tips(self, diagnoses: List[str]) -> List[str]:
        """Compile exercise recommendations"""
        all_tips = []
        
        for diagnosis in diagnoses:
            dx_lower = diagnosis.lower()
            if dx_lower in self.lifestyle_recommendations:
                tips = self.lifestyle_recommendations[dx_lower].get('exercise', [])
                all_tips.extend(tips)
        
        unique_tips = list(dict.fromkeys(all_tips))
        
        return unique_tips[:6] if unique_tips else [
            "Start with short walks and gradually increase",
            "Aim for 30 minutes of activity most days",
            "Choose activities you enjoy",
            "Always check with your doctor before starting new exercise"
        ]
    
    def compile_daily_habits(self, diagnoses: List[str]) -> List[str]:
        """Compile daily monitoring habits"""
        all_habits = []
        
        for diagnosis in diagnoses:
            dx_lower = diagnosis.lower()
            if dx_lower in self.lifestyle_recommendations:
                habits = self.lifestyle_recommendations[dx_lower].get('daily_habits', [])
                all_habits.extend(habits)
        
        unique_habits = list(dict.fromkeys(all_habits))
        
        return unique_habits[:7] if unique_habits else [
            "Take medications at the same time each day",
            "Keep a health journal",
            "Get adequate sleep (7-8 hours)",
            "Manage stress through relaxation techniques"
        ]
    
    def compile_warning_signs(self, diagnoses: List[str]) -> List[str]:
        """Compile warning signs to watch for"""
        all_signs = []
        
        for diagnosis in diagnoses:
            dx_lower = diagnosis.lower()
            if dx_lower in self.lifestyle_recommendations:
                signs = self.lifestyle_recommendations[dx_lower].get('warning_signs', [])
                all_signs.extend(signs)
        
        unique_signs = list(dict.fromkeys(all_signs))
        
        # Always include general emergency signs
        general_emergencies = [
            "⚠️ CALL 911 for: Severe chest pain, difficulty breathing, sudden weakness, severe bleeding"
        ]
        
        return general_emergencies + unique_signs[:6]
    
    def generate_doctor_questions(self, diagnoses: List[str], medications: List[Dict]) -> List[str]:
        """Generate personalized questions to ask the doctor"""
        questions = []
        
        # Diagnosis-specific questions
        if diagnoses:
            questions.append(f"Can you explain more about my {diagnoses[0].lower()} and what caused it?")
            questions.append(f"What can I do to prevent my {diagnoses[0].lower()} from getting worse?")
            
            if len(diagnoses) > 1:
                questions.append(f"How do my different conditions ({', '.join([d.lower() for d in diagnoses[:2]])}) affect each other?")
        
        # Medication questions
        if medications:
            questions.append("What should I do if I miss a dose of my medication?")
            questions.append("Are there any foods or other medications I should avoid?")
        
        # Add general questions
        questions.extend([
            "What numbers or measurements should I be tracking at home?",
            "When do I need to come back for a follow-up?",
            "What symptoms mean I should call you versus going to the ER?",
            "Are there any support groups or resources you recommend?"
        ])
        
        return questions[:10]  # Limit to top 10
    
    def generate_medication_reminders(self, medications: List[Dict]) -> List[str]:
        """Generate medication reminders and tips"""
        if not medications:
            return []
        
        reminders = [
            "Take all medications exactly as prescribed",
            "Don't stop taking medications without talking to your doctor first",
            "Use a pill organizer to help remember doses",
            "Set phone alarms for medication times",
            "Keep a list of all medications with you",
            "Tell all your doctors about ALL medications you take (including over-the-counter)",
            "Report any side effects to your doctor promptly",
            "Get refills before you run out"
        ]
        
        return reminders[:6]
    
    def get_encouragement_message(self) -> str:
        """Provide encouraging message"""
        return """
💪 Remember: Small changes add up! You don't have to do everything perfectly right away.
Pick 1-2 changes to start with, make them habits, then add more. You've got this!

Managing chronic conditions is a marathon, not a sprint. Be patient with yourself and
celebrate small victories. Your healthcare team is here to support you.
        """.strip()
    
    def format_for_display(self, action_plan: Dict) -> str:
        """Format action plan for human-readable output"""
        output = []
        output.append("=" * 60)
        output.append("AGENT 3: YOUR PERSONALIZED ACTION PLAN")
        output.append("=" * 60)
        output.append("")
        
        # Diet
        if action_plan['diet_recommendations']:
            output.append("🥗 DIET & NUTRITION TIPS:")
            for i, tip in enumerate(action_plan['diet_recommendations'], 1):
                output.append(f"   {i}. {tip}")
            output.append("")
        
        # Exercise
        if action_plan['exercise_recommendations']:
            output.append("🏃 EXERCISE & ACTIVITY:")
            for i, tip in enumerate(action_plan['exercise_recommendations'], 1):
                output.append(f"   {i}. {tip}")
            output.append("")
        
        # Daily habits
        if action_plan['daily_habits']:
            output.append("📅 DAILY HABITS TO TRACK:")
            for i, habit in enumerate(action_plan['daily_habits'], 1):
                output.append(f"   {i}. {habit}")
            output.append("")
        
        # Medication reminders
        if action_plan['medication_reminders']:
            output.append("💊 MEDICATION REMINDERS:")
            for i, reminder in enumerate(action_plan['medication_reminders'], 1):
                output.append(f"   {i}. {reminder}")
            output.append("")
        
        # Warning signs
        if action_plan['warning_signs']:
            output.append("⚠️  WARNING SIGNS - WHEN TO GET HELP:")
            for sign in action_plan['warning_signs']:
                output.append(f"   • {sign}")
            output.append("")
        
        # Questions for doctor
        if action_plan['questions_for_doctor']:
            output.append("QUESTIONS TO ASK YOUR DOCTOR:")
            for i, question in enumerate(action_plan['questions_for_doctor'], 1):
                output.append(f"   {i}. {question}")
            output.append("")
        
        # Encouragement
        output.append("💙 " + action_plan['encouragement'])
        output.append("")
        output.append("=" * 60)
        output.append("Ready for final assembly by Agent 4 (Report Builder)")
        output.append("=" * 60)
        
        return "\n".join(output)


# Example usage and testing
if __name__ == "__main__":
    # Simulate Agent 2's output
    sample_agent2_output = {
        'diagnoses_explained': [
            {
                'diagnosis': 'Congestive Heart Failure',
                'simple_name': 'Heart Not Pumping Efficiently',
                'explanation': 'Your heart muscle has become weakened...'
            },
            {
                'diagnosis': 'Hypertension',
                'simple_name': 'High Blood Pressure',
                'explanation': 'Your blood pressure is higher than it should be...'
            }
        ],
        'original_extraction': {
            'diagnoses': ['Congestive Heart Failure', 'Hypertension', 'Type 2 Diabetes'],
            'medications': [
                {'name': 'Furosemide', 'dosage': '40mg'},
                {'name': 'Lisinopril', 'dosage': '20mg'}
            ]
        }
    }
    
    # Create lifestyle coach
    coach = LifestyleCoach()
    
    # Generate action plan
    print("Testing Agent 3: Lifestyle & Action Coach\n")
    action_plan = coach.generate_action_plan(sample_agent2_output)
    
    # Display formatted output
    print(coach.format_for_display(action_plan))
    
    # Show JSON for Agent 4
    print("\n\nJSON FORMAT (sent to Agent 4):")
    print(json.dumps(action_plan, indent=2))
