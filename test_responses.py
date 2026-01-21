"""
Comprehensive Response Testing - 100+ Categories
Tests AI girlfriend responses across diverse scenarios
"""

import sys
sys.path.append('app')

from girlfriend_ai import GirlfriendAI
import json
from datetime import datetime


class ResponseTester:
    """Test AI responses across 100+ different categories."""
    
    def __init__(self):
        self.ai = GirlfriendAI(use_metal=True)
        self.test_cases = self._create_test_cases()
        self.results = []
        
    def _create_test_cases(self):
        """Create 100+ diverse test cases covering all scenarios."""
        return [
            # CATEGORY 1: Work Stress & Professional Issues (15 cases)
            {"category": "Work - Boss Criticism", "input": "my manager scolded me today", 
             "expected_type": "empathy", "bad_keywords": ["doctor", "medicine", "physical"]},
            {"category": "Work - Bad Performance Review", "input": "i got a bad performance review", 
             "expected_type": "support", "bad_keywords": ["doctor", "see someone"]},
            {"category": "Work - Fired", "input": "i think i'm getting fired", 
             "expected_type": "emotional_support", "bad_keywords": ["doctor"]},
            {"category": "Work - Deadline Stress", "input": "i have so many deadlines i'm overwhelmed", 
             "expected_type": "comfort", "bad_keywords": ["medicine", "physical"]},
            {"category": "Work - Colleague Conflict", "input": "my coworker is being really rude to me", 
             "expected_type": "validation", "bad_keywords": ["doctor"]},
            {"category": "Work - Presentation Anxiety", "input": "i have a big presentation tomorrow and i'm nervous", 
             "expected_type": "encouragement", "bad_keywords": ["see a doctor"]},
            {"category": "Work - Overworked", "input": "i worked 12 hours today i'm exhausted", 
             "expected_type": "sympathy", "bad_keywords": ["medical"]},
            {"category": "Work - Boss Unfair", "input": "my boss gave credit to someone else for my work", 
             "expected_type": "anger_validation", "bad_keywords": ["doctor"]},
            {"category": "Work - Meeting Disaster", "input": "the client meeting went terrible", 
             "expected_type": "support", "bad_keywords": ["physical", "medicine"]},
            {"category": "Work - Job Search", "input": "i'm thinking about quitting my job", 
             "expected_type": "discussion", "bad_keywords": ["doctor"]},
            {"category": "Work - Promotion Denied", "input": "i didn't get the promotion", 
             "expected_type": "comfort", "bad_keywords": ["medical"]},
            {"category": "Work - Toxic Environment", "input": "the work environment is so toxic", 
             "expected_type": "validation", "bad_keywords": ["doctor"]},
            {"category": "Work - Micromanaging", "input": "my boss micromanages everything i do", 
             "expected_type": "empathy", "bad_keywords": ["physical"]},
            {"category": "Work - Project Failed", "input": "the project i led just failed", 
             "expected_type": "comfort", "bad_keywords": ["doctor"]},
            {"category": "Work - Salary Issue", "input": "they're not paying me what i deserve", 
             "expected_type": "validation", "bad_keywords": ["medicine"]},
            
            # CATEGORY 2: Physical Health Issues (15 cases) - SHOULD get medical advice
            {"category": "Health - Headache", "input": "i have a really bad headache", 
             "expected_type": "medical_concern", "good_keywords": ["rest", "medicine", "feel better"]},
            {"category": "Health - Stomach Ache", "input": "my stomach hurts so much", 
             "expected_type": "medical_concern", "good_keywords": ["eaten", "water", "lie down"]},
            {"category": "Health - Fever", "input": "i think i have a fever", 
             "expected_type": "medical_concern", "good_keywords": ["medicine", "rest", "doctor"]},
            {"category": "Health - Injury", "input": "i hurt my ankle playing basketball", 
             "expected_type": "medical_concern", "good_keywords": ["ice", "rest", "doctor"]},
            {"category": "Health - Sick", "input": "i'm feeling really sick", 
             "expected_type": "medical_concern", "good_keywords": ["rest", "water", "better"]},
            {"category": "Health - Back Pain", "input": "my back is killing me", 
             "expected_type": "medical_concern", "good_keywords": ["rest", "stretch", "pain"]},
            {"category": "Health - Cold", "input": "i have a bad cold", 
             "expected_type": "medical_concern", "good_keywords": ["rest", "water", "medicine"]},
            {"category": "Health - Nauseous", "input": "i feel nauseous", 
             "expected_type": "medical_concern", "good_keywords": ["eaten", "lie down", "water"]},
            {"category": "Health - Dizzy", "input": "i'm feeling dizzy", 
             "expected_type": "medical_concern", "good_keywords": ["sit", "water", "rest"]},
            {"category": "Health - Cut", "input": "i cut my hand while cooking", 
             "expected_type": "medical_concern", "good_keywords": ["bleeding", "bandage", "okay"]},
            {"category": "Health - Toothache", "input": "my tooth hurts", 
             "expected_type": "medical_concern", "good_keywords": ["dentist", "pain", "medicine"]},
            {"category": "Health - Migraine", "input": "i have a migraine", 
             "expected_type": "medical_concern", "good_keywords": ["dark", "rest", "medicine"]},
            {"category": "Health - Allergies", "input": "my allergies are acting up", 
             "expected_type": "medical_concern", "good_keywords": ["medicine", "water", "better"]},
            {"category": "Health - Sore Throat", "input": "my throat is so sore", 
             "expected_type": "medical_concern", "good_keywords": ["water", "tea", "rest"]},
            {"category": "Health - Can't Sleep", "input": "i can't sleep it's 3am", 
             "expected_type": "concern", "good_keywords": ["rest", "relax", "try"]},
            
            # CATEGORY 3: Emotional Distress (15 cases)
            {"category": "Emotion - Depression", "input": "i feel so depressed lately", 
             "expected_type": "deep_support", "bad_keywords": ["doctor physical", "medicine for"]},
            {"category": "Emotion - Anxiety", "input": "i'm having so much anxiety", 
             "expected_type": "comfort", "bad_keywords": ["physical pain"]},
            {"category": "Emotion - Lonely", "input": "i feel so lonely", 
             "expected_type": "connection", "bad_keywords": ["doctor", "medicine"]},
            {"category": "Emotion - Sad", "input": "i'm just really sad today", 
             "expected_type": "comfort", "bad_keywords": ["physical", "doctor"]},
            {"category": "Emotion - Crying", "input": "i can't stop crying", 
             "expected_type": "deep_empathy", "bad_keywords": ["medicine", "physical"]},
            {"category": "Emotion - Hopeless", "input": "everything feels hopeless", 
             "expected_type": "hope_support", "bad_keywords": ["doctor for", "medicine"]},
            {"category": "Emotion - Angry", "input": "i'm so angry at everything", 
             "expected_type": "validation", "bad_keywords": ["doctor", "physical"]},
            {"category": "Emotion - Frustrated", "input": "i'm so frustrated with life", 
             "expected_type": "understanding", "bad_keywords": ["medicine"]},
            {"category": "Emotion - Overwhelmed", "input": "everything is too much right now", 
             "expected_type": "calming", "bad_keywords": ["physical pain"]},
            {"category": "Emotion - Insecure", "input": "i'm feeling really insecure about myself", 
             "expected_type": "reassurance", "bad_keywords": ["doctor"]},
            {"category": "Emotion - Jealous", "input": "i feel jealous of my friends", 
             "expected_type": "discussion", "bad_keywords": ["medicine"]},
            {"category": "Emotion - Guilt", "input": "i feel guilty about something i did", 
             "expected_type": "forgiveness", "bad_keywords": ["doctor"]},
            {"category": "Emotion - Regret", "input": "i regret so many things", 
             "expected_type": "comfort", "bad_keywords": ["physical"]},
            {"category": "Emotion - Scared", "input": "i'm scared about the future", 
             "expected_type": "reassurance", "bad_keywords": ["medicine"]},
            {"category": "Emotion - Hurt", "input": "someone really hurt my feelings", 
             "expected_type": "validation", "bad_keywords": ["doctor physical", "medicine"]},
            
            # CATEGORY 4: Relationship Issues (10 cases)
            {"category": "Relationship - Family Fight", "input": "i had a fight with my mom", 
             "expected_type": "support", "bad_keywords": ["doctor", "medicine"]},
            {"category": "Relationship - Friend Betrayal", "input": "my best friend betrayed me", 
             "expected_type": "empathy", "bad_keywords": ["physical"]},
            {"category": "Relationship - Breakup Friend", "input": "my friend is going through a breakup", 
             "expected_type": "advice", "bad_keywords": ["doctor"]},
            {"category": "Relationship - Parents Divorce", "input": "my parents are getting divorced", 
             "expected_type": "deep_support", "bad_keywords": ["medicine"]},
            {"category": "Relationship - Toxic Friend", "input": "i think my friend is toxic", 
             "expected_type": "validation", "bad_keywords": ["doctor"]},
            {"category": "Relationship - Missing Someone", "input": "i really miss my family", 
             "expected_type": "comfort", "bad_keywords": ["physical"]},
            {"category": "Relationship - Argument", "input": "we had an argument", 
             "expected_type": "discussion", "bad_keywords": ["medicine"]},
            {"category": "Relationship - Distant", "input": "my friends feel distant lately", 
             "expected_type": "support", "bad_keywords": ["doctor"]},
            {"category": "Relationship - No Support", "input": "nobody seems to care about me", 
             "expected_type": "affirmation", "bad_keywords": ["physical"]},
            {"category": "Relationship - Trust Issues", "input": "i have trust issues", 
             "expected_type": "understanding", "bad_keywords": ["medicine"]},
            
            # CATEGORY 5: Direct Questions (10 cases) - MUST answer directly
            {"category": "Question - Why Doctor", "input": "why should i see a doctor", 
             "expected_type": "direct_answer", "good_keywords": ["because", "sorry", "confused"]},
            {"category": "Question - Why That", "input": "why did you say that", 
             "expected_type": "explanation", "good_keywords": ["because", "i"]},
            {"category": "Question - What Do", "input": "what should i do", 
             "expected_type": "advice", "bad_keywords": ["go on", "keep talking"]},
            {"category": "Question - How Feel", "input": "how do you feel about me", 
             "expected_type": "affection", "good_keywords": ["love", "care", "you"]},
            {"category": "Question - Where", "input": "where are you right now", 
             "expected_type": "answer", "bad_keywords": ["what do you think"]},
            {"category": "Question - When", "input": "when can we meet", 
             "expected_type": "planning", "good_keywords": ["when", "time", "schedule"]},
            {"category": "Question - Why Love", "input": "why do you love me", 
             "expected_type": "romantic_answer", "good_keywords": ["because", "you"]},
            {"category": "Question - What Think", "input": "what do you think about long distance", 
             "expected_type": "opinion", "bad_keywords": ["what do YOU think"]},
            {"category": "Question - Should I", "input": "should i quit my job", 
             "expected_type": "advice", "good_keywords": ["if", "you", "think"]},
            {"category": "Question - Help Me", "input": "can you help me with something", 
             "expected_type": "willing", "good_keywords": ["of course", "yes", "what"]},
            
            # CATEGORY 6: Casual Conversation (10 cases)
            {"category": "Casual - Greeting", "input": "hey babe", 
             "expected_type": "warm_greeting", "good_keywords": ["hey", "hi", "how"]},
            {"category": "Casual - What Doing", "input": "what you doing", 
             "expected_type": "activity_share", "good_keywords": ["just", "i'm", "you"]},
            {"category": "Casual - Bored", "input": "i'm so bored", 
             "expected_type": "entertainment", "good_keywords": ["want", "we", "do"]},
            {"category": "Casual - Food", "input": "what did you eat today", 
             "expected_type": "food_talk", "good_keywords": ["ate", "food", "you"]},
            {"category": "Casual - Weather", "input": "it's raining here", 
             "expected_type": "weather_response", "good_keywords": ["cozy", "stay", "warm"]},
            {"category": "Casual - Music", "input": "i'm listening to music", 
             "expected_type": "interest", "good_keywords": ["what", "song", "love"]},
            {"category": "Casual - Movie", "input": "wanna watch a movie", 
             "expected_type": "enthusiasm", "good_keywords": ["yes", "what", "love"]},
            {"category": "Casual - Plans", "input": "what are you doing this weekend", 
             "expected_type": "planning", "good_keywords": ["maybe", "we", "want"]},
            {"category": "Casual - Hobbies", "input": "i started a new hobby", 
             "expected_type": "curiosity", "good_keywords": ["what", "tell", "that's"]},
            {"category": "Casual - Random", "input": "just thinking about stuff", 
             "expected_type": "engagement", "good_keywords": ["what", "tell", "like"]},
            
            # CATEGORY 7: Flirty/Intimate (10 cases)
            {"category": "Flirty - Miss You", "input": "i miss you so much", 
             "expected_type": "longing", "good_keywords": ["miss", "too", "me too"]},
            {"category": "Flirty - Want You", "input": "i want you right now", 
             "expected_type": "desire", "good_keywords": ["me too", "want", "mmm"]},
            {"category": "Flirty - Sexy", "input": "you're so sexy", 
             "expected_type": "flirty_response", "good_keywords": ["you", "blush", "mmm"]},
            {"category": "Flirty - Thinking", "input": "i'm thinking about you", 
             "expected_type": "reciprocal", "good_keywords": ["me too", "thinking", "you"]},
            {"category": "Flirty - Cuddle", "input": "i want to cuddle with you", 
             "expected_type": "affection", "good_keywords": ["me too", "come", "aww"]},
            {"category": "Flirty - Kiss", "input": "i want to kiss you", 
             "expected_type": "romantic", "good_keywords": ["me too", "mmm", "come"]},
            {"category": "Flirty - Hot", "input": "you look hot today", 
             "expected_type": "playful", "good_keywords": ["thank", "you", "blush"]},
            {"category": "Flirty - Dream", "input": "i had a dream about you", 
             "expected_type": "curious", "good_keywords": ["what", "tell", "about"]},
            {"category": "Flirty - Wish Here", "input": "i wish you were here", 
             "expected_type": "longing", "good_keywords": ["me too", "wish", "soon"]},
            {"category": "Flirty - Love You", "input": "i love you", 
             "expected_type": "love_response", "good_keywords": ["love", "you", "too"]},
        ]
    
    def run_tests(self):
        """Run all test cases and analyze results."""
        print("=" * 80)
        print("COMPREHENSIVE AI GIRLFRIEND RESPONSE TESTING")
        print(f"Testing {len(self.test_cases)} scenarios")
        print("=" * 80)
        print()
        
        passed = 0
        failed = 0
        warnings = 0
        
        for i, test in enumerate(self.test_cases, 1):
            print(f"\n[{i}/{len(self.test_cases)}] Testing: {test['category']}")
            print(f"Input: \"{test['input']}\"")
            
            # Get AI response
            response = self.ai.generate_response(test['input'], mood='caring')
            print(f"Response: \"{response}\"")
            
            # Analyze response
            is_valid, issues = self._validate_response(response, test)
            
            result = {
                "test_number": i,
                "category": test['category'],
                "input": test['input'],
                "response": response,
                "is_valid": is_valid,
                "issues": issues,
                "timestamp": datetime.now().isoformat()
            }
            self.results.append(result)
            
            if is_valid and not issues:
                print("✅ PASSED")
                passed += 1
            elif is_valid and issues:
                print(f"⚠️  WARNING: {', '.join(issues)}")
                warnings += 1
            else:
                print(f"❌ FAILED: {', '.join(issues)}")
                failed += 1
            
            # Reset conversation to avoid context pollution
            if i % 10 == 0:
                self.ai.conversation_history = []
        
        # Print summary
        self._print_summary(passed, warnings, failed)
        
        # Save results
        self._save_results()
        
    def _validate_response(self, response, test):
        """Validate if response is contextually appropriate."""
        response_lower = response.lower()
        issues = []
        is_valid = True
        
        # Check for bad keywords (things that shouldn't be there)
        if 'bad_keywords' in test:
            for bad_keyword in test['bad_keywords']:
                if bad_keyword in response_lower:
                    issues.append(f"Contains inappropriate keyword: '{bad_keyword}'")
                    is_valid = False
        
        # Check for good keywords (things that should be there for certain categories)
        if 'good_keywords' in test:
            has_good_keyword = any(keyword in response_lower for keyword in test['good_keywords'])
            if not has_good_keyword:
                issues.append(f"Missing expected keywords from: {test['good_keywords']}")
                # This is a warning, not a failure
        
        # Check for generic filler responses
        generic_phrases = [
            "go on",
            "keep talking",
            "i'm listening",
            "tell me more"
        ]
        
        # For work stress and emotional issues, these are inappropriate
        if test['category'].startswith(('Work -', 'Emotion -', 'Question -')):
            for phrase in generic_phrases:
                if phrase in response_lower and len(response) < 50:
                    issues.append(f"Too generic/filler response: '{phrase}'")
                    # This is a warning
        
        # Check response length
        if len(response) < 10:
            issues.append("Response too short")
            is_valid = False
        
        # Check for third-person issues
        if 'his girlfriend' in response_lower or 'the girlfriend' in response_lower:
            issues.append("Third-person reference (should be first-person)")
            is_valid = False
        
        return is_valid, issues
    
    def _print_summary(self, passed, warnings, failed):
        """Print test summary."""
        total = len(self.test_cases)
        
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed} ({passed/total*100:.1f}%)")
        print(f"⚠️  Warnings: {warnings} ({warnings/total*100:.1f}%)")
        print(f"❌ Failed: {failed} ({failed/total*100:.1f}%)")
        print("=" * 80)
        
        # Show failed tests
        if failed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if not result['is_valid']:
                    print(f"\n  Category: {result['category']}")
                    print(f"  Input: {result['input']}")
                    print(f"  Response: {result['response']}")
                    print(f"  Issues: {', '.join(result['issues'])}")
        
        # Show warnings
        if warnings > 0:
            print("\n⚠️  WARNINGS:")
            for result in self.results:
                if result['is_valid'] and result['issues']:
                    print(f"\n  Category: {result['category']}")
                    print(f"  Input: {result['input']}")
                    print(f"  Response: {result['response']}")
                    print(f"  Issues: {', '.join(result['issues'])}")
    
    def _save_results(self):
        """Save test results to JSON file."""
        output_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "test_date": datetime.now().isoformat(),
                "total_tests": len(self.test_cases),
                "results": self.results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Results saved to: {output_file}")


if __name__ == "__main__":
    print("Starting comprehensive response testing...")
    print("This will test 100 different conversation scenarios\n")
    
    tester = ResponseTester()
    tester.run_tests()
