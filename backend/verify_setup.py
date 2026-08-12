import os
import sys

# Ensure backend root is in sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def verify():
    print("=== PHARMALYX ENVIRONMENT & GEMINI SDK VERIFICATION ===")

    # 1. Check Python packages
    try:
        import fastapi
        import uvicorn
        import httpx
        import pydantic
        import dotenv
        from google import genai
        print("[SUCCESS] Essential Python packages (fastapi, httpx, pydantic, google-genai) are installed.")
    except ImportError as e:
        print(f"[FAIL] Missing Python package: {e}")
        print("Run: pip install -r backend/requirements.txt")
        sys.exit(1)

    # 2. Check configuration and API Key
    from app.core.config import settings
    api_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")

    if not api_key or api_key == "your_gemini_api_key_here":
        print("[WARNING] GEMINI_API_KEY is missing or set to default placeholder in .env.local.")
        print("Please update .env.local with a valid key from Google AI Studio.")
        sys.exit(1)
    else:
        print(f"[SUCCESS] GEMINI_API_KEY detected (Length: {len(api_key)} chars).")
        print(f"[INFO] Using Gemini Model: {settings.GEMINI_MODEL}")

    # 3. Test Gemini API Connectivity using official google-genai SDK
    try:
        from app.services.gemini_service import GeminiService
        gemini = GeminiService()
        print("[INFO] Sending verification prompt to Google Gemini API via official google-genai SDK...")
        response_text = gemini.generate_text("Reply with exactly five words: 'Pharmalyx GenAI SDK connection successful.'")
        print(f"[SUCCESS] Gemini API Response: {response_text.strip()}")
    except Exception as e:
        print(f"[FAIL] Gemini API call failed: {e}")
        sys.exit(1)

    print("\n=== STEP 1 VERIFICATION PASSED ===")

if __name__ == "__main__":
    verify()
