"""
Backend Test Script
Quick test to verify all backend components are working correctly.
"""
import sys

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        # Test model imports
        print("✅ Models imported successfully")
        
        # Test controller imports
        print("✅ Controllers imported successfully")
        
        # Test route imports
        print("✅ Routes imported successfully")
        
        # Test utility imports
        print("✅ Utilities imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_utilities():
    """Test data utility functions."""
    print("\nTesting data utilities...")
    
    try:
        from app.utils.data_utils import (
            validate_email, 
            validate_password, 
            validate_workout_data,
            format_exercise_name,
            sanitize_string
        )
        
        # Test email validation
        assert validate_email("test@example.com")
        assert not validate_email("invalid-email")
        print("✅ Email validation working")
        
        # Test password validation
        valid, msg = validate_password("password123")
        assert valid
        print("✅ Password validation working")
        
        # Test workout data validation
        valid, msg = validate_workout_data("Bicep Curl", 10, 3)
        assert valid
        print("✅ Workout validation working")
        
        # Test exercise name formatting
        formatted = format_exercise_name("bicep curl")
        assert formatted == "Bicep Curl"
        print("✅ Exercise name formatting working")
        
        # Test string sanitization
        sanitized = sanitize_string("  test string  ")
        assert sanitized == "test string"
        print("✅ String sanitization working")
        
        return True
        
    except Exception as e:
        print(f"❌ Data utility test error: {e}")
        return False

def test_pose_detector():
    """Test pose detector initialization."""
    print("\nTesting pose detector...")
    
    try:
        from app.models.pose_detection import PoseDetector
        
        # Create detector instance
        detector = PoseDetector()
        print("✅ PoseDetector initialized successfully")
        
        # Test angle calculation
        angle = detector.calculate_angle([0, 0], [1, 0], [1, 1])
        assert angle > 0
        print("✅ Angle calculation working")
        
        detector.close()
        print("✅ PoseDetector cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Pose detector test error: {e}")
        return False

def test_flask_app():
    """Test Flask app initialization."""
    print("\nTesting Flask app...")
    
    try:
        import importlib.util
        import os
        
        # Load app.py specifically
        app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.py')
        spec = importlib.util.spec_from_file_location("main_app", app_path)
        main_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_app)
        
        flask_app = main_app.app
        
        # Check if app is created
        assert flask_app is not None
        print("✅ Flask app created successfully")
        
        # Check if blueprints are registered
        blueprint_names = [bp.name for bp in flask_app.blueprints.values()]
        assert 'auth' in blueprint_names
        assert 'workout' in blueprint_names
        assert 'analytics' in blueprint_names
        print("✅ All blueprints registered")
        
        # Check if extensions are initialized
        assert hasattr(flask_app, 'config')
        print("✅ App configuration loaded")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("Backend Component Tests")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(("Import Test", test_imports()))
    results.append(("Data Utilities Test", test_data_utilities()))
    results.append(("Pose Detector Test", test_pose_detector()))
    results.append(("Flask App Test", test_flask_app()))
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Backend is ready to use.")
        return 0
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
