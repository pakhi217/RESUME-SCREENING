"""
utils/sample_data.py
────────────────────
Sample job descriptions bundled with the app so users can try the
analysis flow without needing their own JD text.
"""

SAMPLE_JOBS: dict[str, str] = {
    "Senior Python Backend Engineer": """
We are looking for a Senior Python Backend Engineer to join our platform team.

Responsibilities:
- Design and build scalable REST and GraphQL APIs using Python, Django, and FastAPI
- Architect microservices deployed on AWS (EC2, Lambda, S3) using Docker and Kubernetes
- Optimize PostgreSQL and Redis data layers for high-throughput workloads
- Implement CI/CD pipelines with Jenkins and GitHub Actions
- Collaborate with frontend engineers using React and TypeScript
- Mentor junior engineers and participate in agile/scrum ceremonies

Requirements:
- 5+ years of professional experience with Python
- Strong knowledge of Django, FastAPI, or Flask
- Experience with Docker, Kubernetes, and CI/CD pipelines
- Solid understanding of PostgreSQL, MongoDB, or Redis
- Familiarity with AWS or GCP cloud infrastructure
- Bachelor's degree in Computer Science or related field
- Excellent communication and problem-solving skills
- Experience with Git, Jira, and agile methodologies
""",

    "Machine Learning Engineer": """
Join our AI team as a Machine Learning Engineer building production-grade ML systems.

Responsibilities:
- Design, train, and deploy machine learning and deep learning models
- Build NLP pipelines using Transformers, BERT, and Hugging Face
- Implement computer vision models using PyTorch and TensorFlow
- Develop scalable ML pipelines with scikit-learn, XGBoost, and LightGBM
- Deploy models to production using Docker, Kubernetes, and AWS SageMaker
- Collaborate with data engineers to build robust data pipelines
- Stay current with the latest research in deep learning and LLMs

Requirements:
- 3+ years of experience in machine learning engineering
- Proficiency in Python, TensorFlow, PyTorch, and scikit-learn
- Experience with NLP, computer vision, or LLM-based systems
- Strong understanding of statistics and applied machine learning
- Experience with cloud platforms (AWS, GCP, Azure)
- Master's degree in Computer Science, Statistics, or related field preferred
- Strong analytical and critical thinking skills
""",

    "Full Stack JavaScript Developer": """
We're hiring a Full Stack Developer to build modern web applications.

Responsibilities:
- Build responsive frontend interfaces using React, Next.js, and TypeScript
- Develop backend services using Node.js, Express, and GraphQL
- Design and maintain MongoDB and PostgreSQL database schemas
- Implement CI/CD workflows using GitHub Actions and Docker
- Write clean, maintainable, well-tested code
- Collaborate closely with designers using Figma
- Participate in code reviews and agile sprint planning

Requirements:
- 3+ years of experience with JavaScript/TypeScript
- Strong experience with React, Next.js, or Vue
- Backend experience with Node.js, Express, or NestJS
- Familiarity with REST and GraphQL APIs
- Experience with MongoDB, PostgreSQL, or MySQL
- Bachelor's degree in Computer Science or equivalent experience
- Strong teamwork and communication skills
""",

    "Cloud DevOps Engineer": """
We are seeking a Cloud DevOps Engineer to manage and scale our infrastructure.

Responsibilities:
- Manage AWS and Azure cloud infrastructure using Terraform and CloudFormation
- Build and maintain Kubernetes clusters and Helm charts
- Implement CI/CD pipelines using Jenkins, GitHub Actions, and ArgoCD
- Monitor systems using Prometheus, Grafana, and ELK stack
- Automate infrastructure provisioning with Ansible
- Ensure high availability, security, and disaster recovery
- Collaborate with development teams on deployment strategies

Requirements:
- 4+ years of experience in DevOps or Site Reliability Engineering
- Strong expertise in AWS, Docker, and Kubernetes
- Experience with Terraform, Ansible, or CloudFormation
- Proficiency in Bash, Python, or Go scripting
- Experience with CI/CD tools (Jenkins, GitHub Actions, GitLab CI)
- Relevant certifications (AWS Solutions Architect, CKA) preferred
- Strong problem-solving and communication skills
""",

    "Data Scientist": """
We are looking for a Data Scientist to drive data-informed decision making.

Responsibilities:
- Analyze large datasets using Python, Pandas, and NumPy
- Build predictive models using scikit-learn and XGBoost
- Create data visualizations and dashboards using Plotly and Tableau
- Design A/B tests and statistical experiments
- Communicate insights to stakeholders through clear reporting
- Collaborate with engineering teams to deploy models to production
- Work with SQL and BigQuery for large-scale data analysis

Requirements:
- 3+ years of experience in data science or analytics
- Strong proficiency in Python, SQL, and statistics
- Experience with scikit-learn, pandas, and data visualization tools
- Knowledge of machine learning algorithms and model evaluation
- Master's degree in Statistics, Computer Science, or related field
- Strong analytical thinking and communication skills
- Experience with cloud data warehouses (BigQuery, Snowflake) is a plus
""",
}


def get_sample_titles() -> list[str]:
    return list(SAMPLE_JOBS.keys())


def get_sample_jd(title: str) -> str:
    return SAMPLE_JOBS.get(title, "").strip()
