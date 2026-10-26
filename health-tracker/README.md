# AI Height & Weight Health Tracker App

A full-stack, deploy-everywhere biometric health diagnostics & anthropometric machine learning application.

---

## 🎯 What's Inside

1. **Fixed Google Colab Python Script (`health_tracker_colab.py`)**:
   - Fixed data leakage and unit conversion timing.
   - Fixed model serialization bug (`dump(data)` → `dump(model)`).
   - Added stratified `train_test_split` with 80/20 train/test evaluation.
   - Evaluates Linear Regression ($R^2$, RMSE) and Logistic Regression (Accuracy, Confusion Matrix, Classification Report).
   - Exports `.pkl` model binaries AND `health_tracker_model_params.json` for zero-server client-side web deployment.

2. **Zero-Server Interactive Web App (`index.html` & `public/health-tracker.html`)**:
   - **BMI Gauge**: Dynamic interactive meter with WHO classifications (Underweight, Normal, Overweight, Obese Class I, Class II/III).
   - **Healthy Target Weight Range**: WHO benchmark (18.5 – 24.9 kg/m²) & Devine formula.
   - **Metabolic Engine (BMR & TDEE)**: Mifflin-St Jeor equation with 4 caloric targets (Aggressive Cut, Mild Cut, Maintenance, Lean Bulk).
   - **Body Fat %**: Deurenberg formula based on BMI, age, and sex.
   - **Hydration Tracker**: Daily water intake calculated at 35ml/kg body weight.
   - **Machine Learning Integration**:
     - Anthropometric Frame Probability (Logistic Regression).
     - Population Baseline Weight Regression (Linear Regression).
   - **Metric & Imperial Toggle**: Instant bi-directional conversion between cm/kg and ft-in/lbs.
   - **Snapshot History**: Stored locally in `localStorage` with clearable log table.
   - **One-Click Export**: Printable/PDF-ready health report.

3. **Backend API (`server_api.py`)**:
   - Production FastAPI REST API with CORS enabled.
   - Ready to deploy to Render, Railway, AWS, or Fly.io.

4. **Universal Embed Snippet (`embed-snippet.html`)**:
   - One-line responsive iframe for WordPress, Squarespace, Webflow, Wix, or custom websites.

---

## 🚀 Quick Start

### 1. Run in Google Colab
1. Open Google Colab and upload `weight-height.csv`.
2. Copy and paste the code from `health_tracker_colab.py`.
3. Run the notebook to train models, inspect evaluation metrics, and download the `.pkl` and `.json` artifacts.

### 2. Open the Web App Directly
- Open `health-tracker/index.html` in any web browser (no installation or server needed!).
- Or, if running the Vite dev server in this portfolio (`npm run dev`), visit:
  `http://localhost:5173/health-tracker.html`

### 3. Deploy to Web (Free & 1-Click)
- **Vercel / Netlify / GitHub Pages**:
  Drag and drop the `health-tracker` folder into Netlify Drop or push to a GitHub repository and turn on GitHub Pages.
- **Embed in WordPress / Any CMS**:
  Paste the snippet from `embed-snippet.html` into a Custom HTML block.

### 4. Run the Python Backend API (Optional)
```bash
cd health-tracker
pip install fastapi uvicorn pydantic numpy
uvicorn server_api:app --reload --port 8000
```
Visit `http://localhost:8000/docs` to test interactive Swagger endpoints.
