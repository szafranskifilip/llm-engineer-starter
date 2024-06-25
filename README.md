# AI Temporally Aware Medical Documentation Representation

## Overview
This project aims to create a temporally aware representation of relevant data from medical documentation using large language models (LLMs). The current implementation leverages OpenAI's ChatGPT 3.5, Langchain, and various tools to parse and summarize medical documents into a structured CSV format.

## Prerequisites
- Python 3.7 or higher
- Git
- Google Cloud Platform (GCP) account with access to Document AI
- OpenAI API key

## Setup Instructions

### 1. Clone the Repository
Clone the repository `llm-engineer-starter` into your desired directory.

```bash
# Navigate to your repository directory
cd your_repository_directory_path

# Clone the repository using HTTPS
git clone https://github.com/szafranskifilip/llm-engineer-starter.git

# Or clone the repository using SSH
git clone git@github.com:szafranskifilip/llm-engineer-starter.git
```

### 2. Set Up the Python Environment
Navigate to the cloned repository and set up a Python virtual environment.

```bash
cd your_repository_directory_path/llm-engineer-starter

# Create a virtual environment
python3 -m venv anterior_venv

# Activate the virtual environment
source anterior_venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt

# Add the project directory to PYTHONPATH
echo "export PYTHONPATH=`pwd`/src" >> anterior_venv/bin/activate
```

### 3. Update Your Environment Variables
Update your `.env` file with the necessary credentials and configuration:

```env
GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
GCP_PROJECT_ID="your-gcp-project-id"
GCP_REGION="eu"
GCP_PROCESSOR_ID="your-gcp-document-ai-processor-id"
OPENAI_API_KEY="your-openai-api-key"
```

### 4. Generate Temporally Aware Representation
To generate a temporally aware representation of the provided medical documentation, follow these steps:

#### 4.1. Prepare the Input Data
Ensure your input PDF is available at the specified path.

#### 4.2. Run the Script
Run the script to generate a structured summarization as a CSV file:

```bash
python3 submission.py --path-to-case-pdf path-to-your-pdf/test.pdf
```

#### 4.3. Output
A CSV file `medical_docs_summary` will be generated with the following structure:
- Event type
- Date
- Summary
- Evaluation

The results will be saved in `data/medical_docs_summary.csv` and sorted by date.

Example of the output:

| Date       | Event Type             | Document Summary                                                                                                                                                                                                                                                                  | Evaluation                                                     | Page  |
|------------|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|-------|
| 2024-03-27 | Consultation           | Patient, a 49-year-old perimenopausal female, seen in consultation for newly diagnosed right breast cancer. History includes bilateral screening mammogram in July 2023, diagnostic imaging revealing a hypoechoic mass with subsequent biopsy showing invasive ductal carcinoma. Planned bilateral mastectomies and sentinel node biopsy. Family history of cancer. Past medical history includes abnormal Pap smear, cervical dysplasia, malignant melanoma, hypertension, sleep apnea, thyroid disease. Allergies to adhesive and Macrobid. Social history indicates marital status, no children, no smoking, alcohol a few times per week. Medication list reviewed.                  | Infiltrating ductal carcinoma of right breast (HCC)            | 2/060 |
| 2024-03-27 | Consultation           | The patient presented with normal physical examination findings including the neck, cardiovascular system, chest, abdomen, skin, and extremities. Bilateral mammogram and ultrasound results showed findings in the right breast including a suspicious mass in the 7:00 position and a benign cyst in the 9:00 position. BI-RADS category (4) was assigned for the suspicious mass, recommending an ultrasound-guided breast biopsy. A previous diagnostic mammogram with inconclusive findings was also discussed, leading to a canceled procedure and a plan for mammographic follow-up in 6 months. BI-RADS category (3) was assigned for this case.                                  | Bilateral mammogram and ultrasound findings, BI-RADS categories, and recommendations for breast imaging | 6/060 |
| 2024-03-27 | Medical exam results   | Patient with abnormal mammogram of the right breast underwent core biopsies showing benign breast tissue with no tumor present. Another biopsy on the right breast revealed invasive ductal carcinoma, Nottingham grade 1, measuring up to 9 mm with associated ductal carcinoma in situ (DCIS). Biomarker results indicated positive estrogen and progesterone receptors, approximately 10-20% Ki-67, and pending HER-2 by FISH. Pathology studies were reviewed and discussed with the patient.                                               | Invasive ductal carcinoma, Nottingham grade 1 with DCIS        | 9/060 |

## Future Work
### Enhancements and Improvements
- **Complex Summary Dataset:** The current implementation provides a basic representation of events. Future versions can enhance the dataset to comply with specific business requirements.
- **Multiple Tools Integration:** Instead of a single parsing tool, incorporate multiple tools to parse detailed patient information or specific data required by insurance providers.
- **Advanced Agent-Based Architecture:** Utilize LangGraph and agents to collect specific data according to requirements:
  - An agent to determine required data based on insurance provider information.
  - An agent to collect data from available patient documentation.
  - A "supervisor" agent to verify data sufficiency and manage the overall operation.
- **Model Upgrades:** Currently using OpenAI ChatGPT 3.5, which may miss relevant data due to technical limitations. Future versions could use more advanced models like ChatGPT 4 or Claude 3.5 Sonnet, potentially improving performance but increasing latency.

## Conclusion
This project lays the foundation for creating temporally aware representations of medical documentation using LLMs. With future enhancements, it aims to meet more complex business requirements and provide a robust solution for medical data summarization and analysis.