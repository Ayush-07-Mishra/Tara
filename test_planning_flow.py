"""
Test the specific "yep fine" conversation flow issue
"""

import sys
sys.path.append('app')

from girlfriend_ai import GirlfriendAI

def test_planning_conversation():
    """Test the exact conversation that was failing."""
    
    print("=" * 80)
    print("TESTING: Planning Conversation Flow")
    print("=" * 80)
    print()
    
    ai = GirlfriendAI(use_metal=True)
    
    # The conversation flow that was failing
    conversation = [
        ("I can't stop thinking about you", "Expected: Reciprocal romantic"),
        ("miss u", "Expected: Miss you too / Come over"),
        ("when?", "Expected: Time suggestion or clarification"),
        ("when should i come over?", "Expected: Suggest a time"),
        ("but like time", "Expected: Specific time like 7pm"),
        ("yep fine", "Expected: Excitement/confirmation, NOT 'tell me more'")
    ]
    
    print("🎭 CONVERSATION SIMULATION:\n")
    
    for i, (user_input, expected) in enumerate(conversation, 1):
        print(f"[{i}] User: \"{user_input}\"")
        print(f"    Expected: {expected}")
        
        response = ai.generate_response(user_input, mood='flirty')
        
        print(f"    AI: \"{response}\"")
        
        # Check for the critical failure
        if i == 6:  # The "yep fine" response
            response_lower = response.lower()
            
            # FAIL conditions
            if 'tell me more' in response_lower or 'ooh tell' in response_lower:
                print(f"    ❌ FAILED: Used 'tell me more' on agreement!")
                print(f"    Issue: AI didn't recognize plan finalization")
                return False
            elif 'interesting' in response_lower and len(response) < 40:
                print(f"    ❌ FAILED: Generic 'interesting' response")
                return False
            elif 'go on' in response_lower or 'keep talking' in response_lower:
                print(f"    ❌ FAILED: Asked to continue on agreement")
                return False
            
            # PASS conditions
            elif any(word in response_lower for word in ['perfect', 'great', 'awesome', 'yay', "can't wait", 'excited', 'see you']):
                print(f"    ✅ PASSED: Proper plan confirmation!")
                print(f"    AI correctly recognized agreement and closed the plan")
                print()
                return True
            else:
                print(f"    ⚠️  WARNING: Unexpected response type")
                print(f"    Not 'tell me more' but also not clear confirmation")
                print()
                return None
        
        print()
    
    return True

def test_various_agreement_scenarios():
    """Test different types of short agreements in different contexts."""
    
    print("\n" + "=" * 80)
    print("TESTING: Various Short Agreement Scenarios")
    print("=" * 80)
    print()
    
    ai = GirlfriendAI(use_metal=True)
    
    test_cases = [
        {
            "setup": [
                ("wanna watch a movie tonight?", "Expected: Yes/time question"),
                ("sure! what time?", "Expected: Time suggestion"),
                ("How about 8pm?", "Expected: Confirmation")
            ],
            "critical": ("okay sounds good", "Should: Confirm plan, NOT 'tell me more'")
        },
        {
            "setup": [
                ("miss you", "Expected: Miss too"),
                ("when can we meet?", "Expected: Time/date suggestion"),
                ("tomorrow evening work?", "Expected: Agreement question")
            ],
            "critical": ("yep perfect", "Should: Excitement, NOT 'tell me more'")
        },
        {
            "setup": [
                ("what are you doing later?", "Expected: Activity/availability"),
                ("wanna come over?", "Expected: Time question"),
                ("7pm?", "Expected: Confirmation")
            ],
            "critical": ("sure", "Should: Plan confirmation, NOT 'tell me more'")
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Scenario {i} ---")
        
        # Reset AI for fresh conversation
        ai.conversation_history = []
        
        # Setup conversation
        for user_input, expected in test_case['setup']:
            response = ai.generate_response(user_input, mood='playful')
            print(f"User: \"{user_input}\"")
            print(f"AI: \"{response}\"")
        
        # Critical test
        user_input, expected = test_case['critical']
        print(f"\n🎯 CRITICAL:")
        print(f"User: \"{user_input}\"")
        print(f"Expected: {expected}")
        
        response = ai.generate_response(user_input, mood='playful')
        print(f"AI: \"{response}\"")
        
        # Evaluate
        response_lower = response.lower()
        
        if 'tell me more' in response_lower or 'ooh tell' in response_lower:
            print("❌ FAILED: 'Tell me more' trap")
            results.append(False)
        elif 'go on' in response_lower or 'keep talking' in response_lower:
            print("❌ FAILED: Generic filler")
            results.append(False)
        elif any(word in response_lower for word in ['perfect', 'great', 'awesome', 'yay', "can't wait", 'excited', 'see you']):
            print("✅ PASSED: Proper confirmation")
            results.append(True)
        elif any(word in response_lower for word in ['okay?', 'you okay', 'alright?', 'quiet']):
            print("⚠️  WARNING: Concerned check-in (acceptable if no plan context detected)")
            results.append(None)
        else:
            print("⚠️  WARNING: Unclear response type")
            results.append(None)
    
    # Summary
    passed = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False)
    warnings = sum(1 for r in results if r is None)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {passed}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")
    print(f"⚠️  Warnings: {warnings}/{len(results)}")
    print()
    
    if failed == 0:
        print("🎉 SUCCESS! Short answer trap is fixed!")
        return True
    else:
        print("⚠️  Issues remain with short answer handling")
        return False

if __name__ == "__main__":
    print("Testing the 'yep fine' conversation flow issue...\n")
    
    # Test the exact failing scenario
    result1 = test_planning_conversation()
    
    # Test variations
    result2 = test_various_agreement_scenarios()
    
    if result1 and result2:
        print("\n" + "=" * 80)
        print("🏆 ALL TESTS PASSED!")
        print("=" * 80)
        print("✅ Short answer trap fixed")
        print("✅ Plan finalization works correctly")
        print("✅ Context-aware agreement handling active")
    else:
        print("\n" + "=" * 80)
        print("⚠️  SOME ISSUES DETECTED")
        print("=" * 80)
        print("Review the outputs above for details")
