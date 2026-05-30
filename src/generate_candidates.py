import csv
import os

def generate_dataset():
    candidates = [
        # --- EXCELLENT FIT (12 candidates) ---
        {
            "candidate_id": "CAN-001",
            "name": "Dr. Emily Chen",
            "current_title": "Senior Research Scientist (AI)",
            "years_experience": "7.5",
            "skills": "Python, PyTorch, Transformers, Large Language Models (LLMs), JAX, MLOps, Docker, AWS, SQL",
            "education": "PhD in Computer Science (Deep Learning focus) - Stanford University",
            "summary": "AI researcher and engineer with over 7 years of experience developing state-of-the-art transformer architectures. Expert in LLM fine-tuning, retrieval-augmented generation (RAG), and custom neural networks. Contributor to PyTorch-lightning.",
            "github_url": "https://github.com/emilychen-ai",
            "linkedin_activity": "Active contributor. Frequently posts about LLM evaluation, custom tokenizer optimizations, and distributed training techniques. 12k followers.",
            "projects": "Led the development of a domain-specific 13B parameter LLM from scratch. Optimized model training pipelines reducing carbon footprint and latency by 35%."
        },
        {
            "candidate_id": "CAN-002",
            "name": "Rajesh Sharma",
            "current_title": "Lead Machine Learning Engineer",
            "years_experience": "8.0",
            "skills": "Python, PyTorch, TensorFlow, MLOps, Docker, Kubernetes, AWS, Triton Inference Server, MLflow, Pinecone, TensorRT, CI/CD",
            "education": "MS in Computer Science - IIT Bombay",
            "summary": "Hands-on engineering leader specializing in scaling machine learning models in production environments. Passionate about MLOps, model quantization, and sub-millisecond inference speeds. Active open source contributor.",
            "github_url": "https://github.com/rajesh-mlops",
            "linkedin_activity": "Shares practical tutorials on setting up Kubernetes clusters for GPU-accelerated deep learning workloads and Triton inference servers.",
            "projects": "Built and deployed a real-time recommendation engine handling 100k requests per second. Created an open-source model quantization toolkit with 400+ GitHub stars."
        },
        {
            "candidate_id": "CAN-003",
            "name": "Sarah Jenkins",
            "current_title": "Senior ML Engineer",
            "years_experience": "6.0",
            "skills": "Python, PyTorch, Transformers, NLP, HuggingFace, AWS, Pinecone, LangChain, Git, Docker",
            "education": "MS in Data Science - Carnegie Mellon University",
            "summary": "Deep learning engineer with 6 years of industry experience building NLP solutions. Strong expertise in pre-training and fine-tuning Transformer models. Experienced with vector databases and semantic search architectures.",
            "github_url": "https://github.com/sjenk-nlp",
            "linkedin_activity": "Shares deep-dive articles on LLM prompt engineering, RAG pipelines, and vector embeddings. Active in NLP research groups.",
            "projects": "Designed a hybrid search engine combining sparse and dense embeddings, boosting retrieval accuracy by 25%. Built an enterprise chatbot using LangChain and PyTorch."
        },
        {
            "candidate_id": "CAN-004",
            "name": "Marcus Vance",
            "current_title": "Senior Deep Learning Engineer",
            "years_experience": "5.5",
            "skills": "Python, PyTorch, Computer Vision, Transformers, Triton, TensorRT, OpenCV, Docker, AWS, Git",
            "education": "BS in Computer Science - Georgia Institute of Technology",
            "summary": "ML Engineer focused on high-performance deep learning models for computer vision and multimodal applications. Expert in model optimization (quantization, pruning) and Triton deployment.",
            "github_url": "https://github.com/mvance-cv",
            "linkedin_activity": "Posts bi-weekly updates comparing TensorRT performance vs ONNX runtime on edge devices.",
            "projects": "Developed a real-time multimodal model that aligns video and text. Optimized the inference pipeline using TensorRT, reducing latency on T4 GPUs by 50%."
        },
        {
            "candidate_id": "CAN-005",
            "name": "Amina Yusuf",
            "current_title": "Principal AI Architect",
            "years_experience": "9.0",
            "skills": "Python, PyTorch, Transformers, LLMs, MLOps, Kubernetes, AWS, SQL, Vector DBs, MLflow, CI/CD",
            "education": "MS in Software Engineering - University of Oxford",
            "summary": "AI architect with nearly a decade of experience designing enterprise-scale machine learning systems. Expert in multi-agent LLM systems, MLOps orchestration, and model governance.",
            "github_url": "https://github.com/amina-ai-arch",
            "linkedin_activity": "Active speaker at AI conferences. Writes extensively on scalable machine learning infrastructure and LLM governance. 15k followers.",
            "projects": "Architected the enterprise AI core platform for a Fortune 500 company, integrating over 30 ML models. Authored custom LLM guardrails library."
        },
        {
            "candidate_id": "CAN-006",
            "name": "Arjun Nair",
            "current_title": "Senior ML Infrastructure Engineer",
            "years_experience": "6.5",
            "skills": "Python, PyTorch, MLOps, Kubernetes, Docker, AWS (SageMaker, S3), Prefect, Prometheus, Grafana, MLflow, SQL, Git",
            "education": "B.Tech in Computer Science - NIT Trichy",
            "summary": "MLOps expert focused on the reliability, observability, and scaling of deep learning training and inference infrastructure. Proven track record in orchestrating multi-node GPU clusters.",
            "github_url": "https://github.com/arjun-nair-infra",
            "linkedin_activity": "Shares insights on scaling SageMaker pipelines, monitoring drift in production, and optimizing cloud GPU spend.",
            "projects": "Built custom monitoring tools for distributed model training, cutting infrastructure failure detection time from hours to seconds. Deployed automated CD pipelines for 50+ models."
        },
        {
            "candidate_id": "CAN-007",
            "name": "Elena Rostova",
            "current_title": "Senior Machine Learning Engineer",
            "years_experience": "7.0",
            "skills": "Python, PyTorch, Transformers, NLP, Deep Learning, HuggingFace, Milvus, Docker, AWS, Git",
            "education": "MS in Applied Mathematics - Moscow State University",
            "summary": "NLP specialist with 7 years of industry experience. Deep theoretical knowledge of attention mechanisms, tokenization, and transfer learning. Practical expert in implementing custom attention layers.",
            "github_url": "https://github.com/elena-rost-nlp",
            "linkedin_activity": "Writes technical articles on mathematical underpinnings of transformers and attention mechanisms. Moderates local NLP meetups.",
            "projects": "Implemented a high-performance custom transformer layer in C++/CUDA. Fine-tuned multi-lingual models for semantic search across 15 languages."
        },
        {
            "candidate_id": "CAN-008",
            "name": "David Miller",
            "current_title": "Lead AI Engineer",
            "years_experience": "8.5",
            "skills": "Python, PyTorch, TensorFlow, LLMs, HuggingFace, LangChain, Docker, Kubernetes, AWS, Pinecone, MLflow, Git",
            "education": "MS in Intelligent Systems - UT Austin",
            "summary": "Software engineer turned ML practitioner. Specializes in building end-to-end applications using generative AI, complex LangChain systems, and scalable deep learning architectures.",
            "github_url": "https://github.com/dmiller-ai",
            "linkedin_activity": "Regularly posts comparisons of different LLM routing strategies and prompt templates. 8k followers.",
            "projects": "Created a generative AI platform for automated medical coding, achieving 98% accuracy. Contributor to LangChain repository."
        },
        {
            "candidate_id": "CAN-009",
            "name": "Mei-Ling Zhou",
            "current_title": "Senior ML Engineer - NLP",
            "years_experience": "5.0",
            "skills": "Python, PyTorch, Transformers, Deep Learning, NLP, AWS, Docker, Git, SQL, Pandas, HuggingFace",
            "education": "MS in Computer Science - Tsinghua University",
            "summary": "Research-driven software engineer with 5 years of industry experience. Expert in neural text generation, reinforcement learning from human feedback (RLHF), and parameter-efficient fine-tuning (PEFT).",
            "github_url": "https://github.com/mlzhou-nlp",
            "linkedin_activity": "Occasionally posts links to her publications in ACL and EMNLP. Shares advice on implementing LoRA and QLoRA.",
            "projects": "Developed a parameter-efficient fine-tuning pipeline using QLoRA that reduced training VRAM requirements by 60%. Deployed a custom dialog manager."
        },
        {
            "candidate_id": "CAN-010",
            "name": "Carlos Gomez",
            "current_title": "Senior ML & Deep Learning Engineer",
            "years_experience": "6.0",
            "skills": "Python, PyTorch, JAX, Transformers, MLOps, AWS, Docker, Kubernetes, Triton, TensorRT, Git",
            "education": "BS in Software Engineering - Universidad de Chile",
            "summary": "Experienced engineer with a strong focus on distributed deep learning and model compilation. Expert in compiling PyTorch models using ONNX and TensorRT for deployment at the edge and cloud.",
            "github_url": "https://github.com/cgomez-dl",
            "linkedin_activity": "Shares tips on debugging PyTorch memory leaks and utilizing JAX for rapid custom gradient modeling.",
            "projects": "Built a high-throughput, low-latency text embeddings API serving 50M daily calls. Ported custom legacy TensorFlow layers to PyTorch."
        },
        {
            "candidate_id": "CAN-011",
            "name": "Sophia Rodriguez",
            "current_title": "Senior Machine Learning Engineer",
            "years_experience": "7.0",
            "skills": "Python, PyTorch, Transformers, LLMs, MLOps, Pinecone, Docker, AWS, MLflow, SQL, Git",
            "education": "MS in Data Science - UC Berkeley",
            "summary": "ML Engineer specializing in conversational agents, vector search engines, and prompt engineering frameworks. Strong experience in fine-tuning open-weight models (Llama, Mistral) on proprietary data.",
            "github_url": "https://github.com/sophia-rod-ml",
            "linkedin_activity": "Posts detailed performance benchmarks comparing various open-source LLMs against proprietary models on custom enterprise tasks.",
            "projects": "Led the development of a real-time semantic search system across 10M documents. Developed automated prompt optimization framework."
        },
        {
            "candidate_id": "CAN-012",
            "name": "Devon Harris",
            "current_title": "Senior AI Platforms Engineer",
            "years_experience": "9.5",
            "skills": "Python, PyTorch, MLOps, Kubernetes, Docker, AWS, MLflow, Triton, Kubeflow, Pinecone, SQL, Git",
            "education": "BS in Computer Science - University of Michigan",
            "summary": "Infrastructure-focused ML Engineer with a decade of experience. Expert in designing Kubeflow workflows, managing massive GPU clusters, and setting up automated model evaluation pipelines.",
            "github_url": "https://github.com/dharris-ai-infra",
            "linkedin_activity": "Writes comprehensive guides on setting up Kubeflow on AWS and optimizing model registry workflows. 6k followers.",
            "projects": "Built and managed an enterprise-wide model registry and deployment platform supporting 200+ active ML developers. Cut cloud infrastructure costs by 40%."
        },

        # --- MID-LEVEL & DECENT FIT (18 candidates) ---
        {
            "candidate_id": "CAN-013",
            "name": "Leo Mercer",
            "current_title": "Machine Learning Engineer",
            "years_experience": "3.5",
            "skills": "Python, PyTorch, Scikit-learn, Pandas, NumPy, Docker, AWS, Git, SQL",
            "education": "BS in Computer Science - University of Washington",
            "summary": "ML Engineer with 3.5 years of experience. Strong foundational knowledge in supervised learning and classical machine learning. Now transition to deep learning and neural networks. Good PyTorch basics.",
            "github_url": "https://github.com/leomercer-ml",
            "linkedin_activity": "Shares simple coding snippets, pandas tips, and summaries of online deep learning courses he's completing.",
            "projects": "Built a predictive churn model using XGBoost that improved retention by 8%. Developed a simple image classification app using PyTorch."
        },
        {
            "candidate_id": "CAN-014",
            "name": "Priya Patel",
            "current_title": "Data Scientist",
            "years_experience": "4.0",
            "skills": "Python, R, Scikit-learn, Pandas, SQL, NumPy, Tableau, Git, Docker",
            "education": "MS in Business Analytics - Columbia University",
            "summary": "Data Scientist with strong analytical background. Highly skilled in feature engineering, statistical analysis, and classical ML. Good experience building scikit-learn models and SQL queries.",
            "github_url": "https://github.com/priyapatel-ds",
            "linkedin_activity": "Writes posts on statistical pitfalls in A/B testing and effective data storytelling. Active in women-in-tech groups.",
            "projects": "Built an automated credit-scoring model using scikit-learn. Designed the experiment framework and dashboard for global product rollouts."
        },
        {
            "candidate_id": "CAN-015",
            "name": "Daniel Kim",
            "current_title": "Software Engineer (Machine Learning)",
            "years_experience": "4.0",
            "skills": "Python, PyTorch, Docker, AWS, SQL, Git, FastAPI, Pandas, NumPy",
            "education": "BS in Computer Science - UCLA",
            "summary": "Backend software engineer with 4 years of experience who transitioned to ML engineering. Strong software engineering skills. Experienced with model wrapping, API design, and cloud deployments.",
            "github_url": "https://github.com/dkim-swe-ml",
            "linkedin_activity": "Shares guides on integrating FastAPI with deep learning inference, containerizing apps with Docker.",
            "projects": "Designed a high-performance REST API for deep learning model predictions using FastAPI and Docker. Deployed models on AWS ECS."
        },
        {
            "candidate_id": "CAN-016",
            "name": "Fatima Zahra",
            "current_title": "Machine Learning Engineer",
            "years_experience": "3.0",
            "skills": "Python, PyTorch, Transformers, HuggingFace, NLP, Git, SQL, Pandas",
            "education": "MS in Artificial Intelligence - Edinburgh University",
            "summary": "Junior/mid ML engineer with 3 years of experience. Specialized in NLP. Good hands-on experience using HuggingFace models and implementing BERT-like architectures for classification.",
            "github_url": "https://github.com/fatimazahra-ai",
            "linkedin_activity": "Shares summaries of new NLP research papers and notes on fine-tuning BERT models.",
            "projects": "Fine-tuned BERT-based sentiment classifier for customer service emails, improving response routing efficiency by 30%."
        },
        {
            "candidate_id": "CAN-017",
            "name": "Oliver Hansen",
            "current_title": "Data Scientist / ML Developer",
            "years_experience": "4.5",
            "skills": "Python, TensorFlow, Keras, Scikit-learn, Pandas, NumPy, SQL, Git, AWS",
            "education": "BS in Statistics - Copenhagen University",
            "summary": "Applied data scientist with 4.5 years of experience. Experienced in statistical modeling, forecasting, and deep learning using TensorFlow/Keras. Well-versed in data cleaning and SQL data pipelines.",
            "github_url": "https://github.com/ohansen-ds",
            "linkedin_activity": "Shares guides on time-series forecasting, LSTM models, and cleaning complex datasets. Moderately active.",
            "projects": "Developed an LSTM-based demand forecasting model that reduced supply chain overhead by 12%. Created automated data pipelines."
        },
        {
            "candidate_id": "CAN-018",
            "name": "Vikram Malhotra",
            "current_title": "Senior Software Engineer (Data)",
            "years_experience": "7.0",
            "skills": "Python, SQL, Spark, Scala, AWS (S3, EMR), Docker, Airflow, Git, Pandas, NumPy",
            "education": "MS in Computer Science - USC",
            "summary": "Experienced Data Engineer. Expert in building big data pipelines, ETL workflows, and Spark streaming applications. Looking to apply data engineering expertise to MLOps and ML platform roles.",
            "github_url": "https://github.com/vikram-data",
            "linkedin_activity": "Writes about tuning Spark cluster performance, scaling data lakes on AWS, and designing clean database schemas.",
            "projects": "Designed an enterprise data warehouse scaling to 100+ Terabytes. Automated massive nightly batch processing pipelines using Airflow."
        },
        {
            "candidate_id": "CAN-019",
            "name": "Jessica Taylor",
            "current_title": "Machine Learning Engineer",
            "years_experience": "3.0",
            "skills": "Python, PyTorch, Transformers, Computer Vision, OpenCV, Docker, Git, Pandas",
            "education": "MS in Robotics - University of Pennsylvania",
            "summary": "Robotics graduate and ML Engineer. Strong focus on vision models, object detection, and reinforcement learning. Solid hands-on experience implementing computer vision pipelines.",
            "github_url": "https://github.com/jtaylor-vision",
            "linkedin_activity": "Shares updates on his latest robotics and vision projects. Active in the ROS and PyTorch communities.",
            "projects": "Built a vision-based obstacle avoidance system for a robotic arm using PyTorch. Deployed real-time YOLOv8 models on Jetson Nano."
        },
        {
            "candidate_id": "CAN-020",
            "name": "Yuki Tanaka",
            "current_title": "AI Research Engineer",
            "years_experience": "4.0",
            "skills": "Python, PyTorch, JAX, Reinforcement Learning, Transformers, Deep Learning, Git",
            "education": "MS in Machine Learning - Kyoto University",
            "summary": "Deep learning engineer focused on reinforcement learning and policy gradient methods. Proficient in PyTorch and JAX. Experienced in implementing custom training loops.",
            "github_url": "https://github.com/yuki-tanaka-rl",
            "linkedin_activity": "Infrequently posts. Shares links to his publications on deep RL and JAX tutorials.",
            "projects": "Built a custom reinforcement learning simulation environment. Implemented parallel PPO in JAX, speeding up training by 4x."
        },
        {
            "candidate_id": "CAN-021",
            "name": "Kofi Mensah",
            "current_title": "Data Scientist",
            "years_experience": "5.0",
            "skills": "Python, Scikit-learn, Pandas, NumPy, SQL, R, Docker, AWS, Git",
            "education": "BS in Mathematics - Kwame Nkrumah University",
            "summary": "Applied mathematician and Data Scientist with 5 years of industry experience. Excellent knowledge of probability, statistics, regression, and tree-based models. Strong SQL and Python developer.",
            "github_url": "https://github.com/kofi-ds",
            "linkedin_activity": "Shares visual guides on mathematical concepts in ML (linear algebra, bayesian inference). Highly engaged audience.",
            "projects": "Developed a credit scoring framework that reduced default rates by 15%. Automated monthly reporting pipeline using Python."
        },
        {
            "candidate_id": "CAN-022",
            "name": "Emma Watson",
            "current_title": "NLP Engineer",
            "years_experience": "3.5",
            "skills": "Python, PyTorch, Transformers, HuggingFace, NLP, Git, Docker, SQL, Pandas",
            "education": "BS in Cognitive Science - UCSD",
            "summary": "NLP developer with 3.5 years of industry experience. Focuses on information extraction, named entity recognition, and text summarization using transformer models. Proficient with HuggingFace.",
            "github_url": "https://github.com/emawatson-nlp",
            "linkedin_activity": "Posts summaries of new LLM frameworks, tokenizer benchmarks, and prompt-tuning methodologies.",
            "projects": "Built an information extraction pipeline that parses medical records with 92% F1 score. Deployed BERT-based models in Docker."
        },
        {
            "candidate_id": "CAN-023",
            "name": "Mateo Silva",
            "current_title": "Machine Learning Engineer",
            "years_experience": "4.0",
            "skills": "Python, PyTorch, TensorFlow, Scikit-learn, MLOps, AWS, Docker, Git, SQL",
            "education": "BS in Computer Science - University of Sao Paulo",
            "summary": "ML Engineer with 4 years of experience. Experienced in building and serving models using PyTorch and TensorFlow. Good understanding of Docker containerization and AWS SageMaker.",
            "github_url": "https://github.com/msilva-ml",
            "linkedin_activity": "Shares quick guides on using Docker for local ML development and deploying models on SageMaker.",
            "projects": "Deployed a computer vision classification model on SageMaker endpoint. Reduced local testing setup time by containerizing environment."
        },
        {
            "candidate_id": "CAN-024",
            "name": "Chloe Lefebvre",
            "current_title": "Data Scientist / ML Engineer",
            "years_experience": "3.0",
            "skills": "Python, PyTorch, Scikit-learn, Transformers, HuggingFace, SQL, Git, Pandas",
            "education": "MS in Data Science - Ecole Polytechnique",
            "summary": "ML Engineer with 3 years of experience. Highly skilled in classical machine learning, feature selection, and basic deep learning using PyTorch. Solid foundation in linear algebra and statistics.",
            "github_url": "https://github.com/chloe-ml-ds",
            "linkedin_activity": "Shares posts about mathematical fundamentals of ML algorithms and data preprocessing techniques.",
            "projects": "Developed a recommendation system for e-commerce website using PyTorch collaborative filtering. Engineered high-quality features."
        },
        {
            "candidate_id": "CAN-025",
            "name": "Zhang Wei",
            "current_title": "Software Engineer (AI Integration)",
            "years_experience": "5.0",
            "skills": "Python, Java, Git, SQL, Docker, AWS, REST APIs, Pandas, Scikit-learn",
            "education": "BS in Computer Science - Zhejiang University",
            "summary": "Backend software engineer who builds APIs and integrates AI services. Highly proficient in Java, Python, and RESTful web services. Familiar with loading pre-trained PyTorch and scikit-learn models.",
            "github_url": "https://github.com/zwei-swe",
            "linkedin_activity": "Writes posts about clean backend code architecture, API design, and microservices. Active in developer forums.",
            "projects": "Designed an enterprise API gateway that handles token routing and model scoring. Containerized backend microservices using Docker."
        },
        {
            "candidate_id": "CAN-026",
            "name": "Ryan Gallagher",
            "current_title": "Machine Learning Engineer",
            "years_experience": "3.5",
            "skills": "Python, PyTorch, MLOps, MLflow, AWS, Docker, SQL, Git, Pandas",
            "education": "BS in Computer Engineering - University of Toronto",
            "summary": "ML Engineer with 3.5 years of experience. Passionate about model tracking, experiment management, and setting up MLOps pipelines. Good foundational knowledge of PyTorch and cloud services.",
            "github_url": "https://github.com/ryangallagher-ml",
            "linkedin_activity": "Shares updates on using MLflow for tracking parameters and metrics in training runs.",
            "projects": "Established a unified model registry using MLflow, reducing deployment errors by 15%. Automated daily model training runs."
        },
        {
            "candidate_id": "CAN-027",
            "name": "Simran Kaur",
            "current_title": "Data Scientist",
            "years_experience": "4.5",
            "skills": "Python, Scikit-learn, Pandas, SQL, Tableau, AWS, Git, NumPy",
            "education": "MS in Information Systems - University of Maryland",
            "summary": "Data Scientist with 4.5 years of experience. Experienced in regression, clustering, classification, and exploratory data analysis. Proficient in SQL, Python, and cloud storage.",
            "github_url": "https://github.com/simran-ds",
            "linkedin_activity": "Writes guides on data cleaning best practices and creating interactive Tableau dashboards.",
            "projects": "Created a customer segmentation model using K-means clustering. Deployed models on AWS Lambda for scheduled predictions."
        },
        {
            "candidate_id": "CAN-028",
            "name": "Tariq Mahmood",
            "current_title": "AI Developer",
            "years_experience": "3.0",
            "skills": "Python, PyTorch, Transformers, HuggingFace, NLP, Git, Docker, SQL",
            "education": "BS in Computer Science - FAST NUCES Karachi",
            "summary": "AI developer with 3 years of experience. Enthusiastic about generative AI, prompt engineering, and fine-tuning lightweight transformer models. Good foundation in PyTorch and HuggingFace.",
            "github_url": "https://github.com/tariq-ai",
            "linkedin_activity": "Frequently posts about testing new open source LLMs and prompt optimization hacks.",
            "projects": "Fine-tuned a T5 model for SQL query generation from natural language description. Deployed model using FastAPI and Docker."
        },
        {
            "candidate_id": "CAN-029",
            "name": "Isabella Rossi",
            "current_title": "Machine Learning Engineer",
            "years_experience": "3.5",
            "skills": "Python, PyTorch, Scikit-learn, Pandas, Docker, Git, SQL, AWS",
            "education": "MS in Data Science - Sapienza University of Rome",
            "summary": "ML Engineer with 3.5 years of experience. Solid understanding of neural networks, gradient descent, and deep learning architectures. Experienced in building model APIs using Python.",
            "github_url": "https://github.com/isa-rossi-ml",
            "linkedin_activity": "Shares educational posts explaining optimization algorithms (Adam, SGD) and regularization techniques.",
            "projects": "Developed a neural network classifier using PyTorch to predict customer churn. Containerized application for deployment."
        },
        {
            "candidate_id": "CAN-030",
            "name": "Lucas Dubois",
            "current_title": "Software Engineer (ML Team)",
            "years_experience": "4.0",
            "skills": "Python, PyTorch, C++, Git, SQL, Docker, AWS, CMake",
            "education": "BS in Computer Engineering - McGill University",
            "summary": "Software engineer in an ML team. Bridges the gap between research and production. Experienced in writing efficient C++ code and translating PyTorch models for optimized execution.",
            "github_url": "https://github.com/lucasdubois-swe",
            "linkedin_activity": "Writes about combining Python with C++ for high performance computing and PyTorch JIT compilation.",
            "projects": "Implemented high-performance feature preprocessing steps in C++, achieving a 5x speedup over pure Python implementations."
        },

        # --- POOR/WEAK FIT (20 candidates) ---
        {
            "candidate_id": "CAN-031",
            "name": "Alice Wonderland",
            "current_title": "Frontend React Developer",
            "years_experience": "4.0",
            "skills": "React, HTML, CSS, Javascript, TypeScript, Redux, Webpack, Git, Tailwind",
            "education": "BS in Web Design - Boston University",
            "summary": "Vibrant frontend developer with 4 years of experience building beautiful user interfaces using React and Tailwind CSS. Focuses on responsiveness, accessibility, and smooth UI animations.",
            "github_url": "https://github.com/alice-ui-designer",
            "linkedin_activity": "Active user. Shares UI designs, React tips, CSS tricks, and accessibility guides. 10k followers.",
            "projects": "Redesigned the checkout flow for an e-commerce platform, boosting conversion by 18%. Built a custom design system component library in React."
        },
        {
            "candidate_id": "CAN-032",
            "name": "Bob Builder",
            "current_title": "Civil Engineer / Project Coordinator",
            "years_experience": "6.0",
            "skills": "AutoCAD, Excel, Project Management, Civil Engineering, Construction Safety",
            "education": "BS in Civil Engineering - Penn State",
            "summary": "Professional civil engineer and project coordinator. 6 years of experience managing infrastructure projects, site safety, and contractor schedules. Proficient in AutoCAD and advanced Excel modeling.",
            "github_url": "https://github.com/bob-builder-civil",
            "linkedin_activity": "Shares updates from construction sites, civil safety guidelines, and infrastructure engineering trends.",
            "projects": "Coordinated the structural renovation of a historic bridge on time and under budget. Managed AutoCAD draft pipeline."
        },
        {
            "candidate_id": "CAN-033",
            "name": "Charlie Chaplin",
            "current_title": "Junior Python Developer",
            "years_experience": "1.5",
            "skills": "Python, Django, HTML, CSS, SQL, Git, Basic Pandas",
            "education": "Self-taught, 6-month Coding Bootcamp",
            "summary": "Enthusiastic bootcamp graduate and junior python developer. Skilled in web development using Django. Looking for my first full-time role to grow my software engineering skills.",
            "github_url": "https://github.com/cchaplin-bootcamp",
            "linkedin_activity": "Posts daily logs of his coding progress (100 days of code), bootcamp assignments, and thoughts on web dev.",
            "projects": "Built a simple web-based library catalog application using Django and SQLite. Created a script to automate email scheduling."
        },
        {
            "candidate_id": "CAN-034",
            "name": "Diana Prince",
            "current_title": "Product Marketing Manager",
            "years_experience": "5.0",
            "skills": "Digital Marketing, SEO, Google Analytics, Copywriting, Strategy, Excel",
            "education": "BA in Communications - NYU",
            "summary": "Results-oriented Marketing Manager with 5 years of experience leading digital campaigns, SEO optimizations, and product launch copywriting. Skilled in analytics and data-driven strategy.",
            "github_url": "https://github.com/dianaprince-mktg",
            "linkedin_activity": "Highly active. Posts about growth marketing, SEO strategies, copy benchmarks, and leadership. 15k followers.",
            "projects": "Launched a SaaS marketing campaign that generated 5,000 qualified leads in 3 months. Boosted SEO organic traffic by 40%."
        },
        {
            "candidate_id": "CAN-035",
            "name": "Evan Hansen",
            "current_title": "Technical Writer",
            "years_experience": "3.0",
            "skills": "Markdown, Technical Writing, Git, Documentation, API Documentation, HTML",
            "education": "BA in English Literature - University of Chicago",
            "summary": "Technical writer with 3 years of experience. Experienced in document editing, API references, user guides, and markdown files. Passionate about translating complex jargon into clear instructions.",
            "github_url": "https://github.com/ehansen-writer",
            "linkedin_activity": "Writes about technical communication, documentation-as-code, and markdown styles.",
            "projects": "Wrote comprehensive API documentation for a major cloud provider. Restructured the developer portal layout, reducing support tickets."
        },
        {
            "candidate_id": "CAN-036",
            "name": "Fiona Gallagher",
            "current_title": "HR Specialist / Recruiting Coordinator",
            "years_experience": "4.0",
            "skills": "Recruiter, Talent Acquisition, ATS, HR Operations, Excel, Communication",
            "education": "BA in Psychology - DePaul University",
            "summary": "Human Resources professional specializing in full-cycle recruitment coordination, ATS management, and employee onboarding. Strong communication and Excel organization.",
            "github_url": "https://github.com/fiona-gall-hr",
            "linkedin_activity": "Shares advice on resume writing, job interview preparation, and workplace culture. 5k followers.",
            "projects": "Coordinated high-volume hiring drive, onboarding 40 new employees in one month. Audited company-wide ATS."
        },
        {
            "candidate_id": "CAN-037",
            "name": "George Costanza",
            "current_title": "Assistant to the General Manager",
            "years_experience": "6.0",
            "skills": "Office Administration, Sales, Scheduling, Excel, Customer Relations",
            "education": "BA in History - Queens College",
            "summary": "Experienced administrator with a diverse background in sales, scheduling, and general office coordination. Excellent customer service skills and expert in advanced Excel formatting.",
            "github_url": "https://github.com/george-costanza-admin",
            "linkedin_activity": "Rarely active. Posts occasional thoughts about office etiquette and sales strategies.",
            "projects": "Managed general office scheduling and travel logistics for a sports franchise, cutting booking costs by 15%."
        },
        {
            "candidate_id": "CAN-038",
            "name": "Harley Quinn",
            "current_title": "Graphic Designer",
            "years_experience": "3.0",
            "skills": "Adobe Photoshop, Illustrator, Figma, Graphic Design, Brand Identity, UI Design",
            "education": "BFA in Graphic Design - Pratt Institute",
            "summary": "Creative graphic designer specializing in brand identity, typography, visual graphics, and marketing materials. Highly proficient in Adobe Suite and Figma mockup designs.",
            "github_url": "https://github.com/hquinn-design",
            "linkedin_activity": "Highly active. Shares custom illustrations, design system prototypes, and typography concepts.",
            "projects": "Designed complete rebrand for a boutique agency. Created high-fidelity Figma mockups for mobile app user interfaces."
        },
        {
            "candidate_id": "CAN-039",
            "name": "Ian Malcolm",
            "current_title": "Database Administrator",
            "years_experience": "8.0",
            "skills": "SQL, PostgreSQL, MySQL, Database Administration, Backup Recovery, Linux",
            "education": "BS in Information Technology - Texas A&M",
            "summary": "Senior Database Administrator with 8 years of experience. Expert in SQL tuning, index optimization, database security, backup-recovery workflows, and managing server clusters in Linux.",
            "github_url": "https://github.com/imalcolm-dba",
            "linkedin_activity": "Shares insights on database partitioning, index optimizations, and SQL query tuning tips.",
            "projects": "Migrated a legacy MySQL database containing 500 million records to PostgreSQL with zero downtime. Optimized slow queries."
        },
        {
            "candidate_id": "CAN-040",
            "name": "Julia Roberts",
            "current_title": "Customer Success Manager",
            "years_experience": "5.0",
            "skills": "Customer Success, CRM, Salesforce, Communication, Relationship Building, Excel",
            "education": "BA in Sociology - Boston College",
            "summary": "CSM with 5 years of experience managing enterprise customer relations, onboarding processes, and retention campaigns. Proficient in Salesforce and advanced Excel reports.",
            "github_url": "https://github.com/jroberts-csm",
            "linkedin_activity": "Active. Posts tips on building customer trust, reducing churn, and enterprise account management.",
            "projects": "Increased customer retention rate by 15% across a portfolio of 50 high-value enterprise accounts. Managed CRM integrations."
        },
        {
            "candidate_id": "CAN-041",
            "name": "Kevin Bacon",
            "current_title": "Junior QA Automation Engineer",
            "years_experience": "2.0",
            "skills": "Python, Selenium, PyTest, QA Testing, Test Automation, Git, Jenkins",
            "education": "BS in Information Systems - University of Denver",
            "summary": "QA Automation engineer with 2 years of experience. Experienced in writing automated test scripts in Python using Selenium and PyTest. Familiar with Jenkins CI/CD pipelines.",
            "github_url": "https://github.com/kbacon-qa",
            "linkedin_activity": "Shares QA automation tutorials and tips on using PyTest fixtures. Moderately active.",
            "projects": "Automated regression testing suite for web application, reducing manual test execution time by 70%."
        },
        {
            "candidate_id": "CAN-042",
            "name": "Lois Lane",
            "current_title": "Investigative Journalist / Copywriter",
            "years_experience": "7.0",
            "skills": "Copywriting, Content Writing, Research, Editing, Interviewing, Social Media",
            "education": "BA in Journalism - Northwestern University",
            "summary": "Award-winning journalist with a strong background in copywriting, editing, public records research, and interviewing. Expert in delivering clear, engaging narratives under tight deadlines.",
            "github_url": "https://github.com/llane-writer",
            "linkedin_activity": "Writes extensively about media integrity, public records requests, and copywriting trends. 20k followers.",
            "projects": "Investigated and wrote high-impact series on municipal budgeting. Authored high-conversion landing page copy."
        },
        {
            "candidate_id": "CAN-043",
            "name": "Michael Scott",
            "current_title": "Regional Sales Manager",
            "years_experience": "10.0",
            "skills": "Sales Management, Negotiation, Client Relations, Public Speaking, Leadership",
            "education": "High School Diploma",
            "summary": "Dedicated sales manager with 10 years of experience leading sales teams, closing high-value accounts, and designing local client relation programs. Awarded Top Salesman multiple times.",
            "github_url": "https://github.com/mscott-dmp",
            "linkedin_activity": "Active. Shares motivational quotes, sales advice, and stories about client satisfaction.",
            "projects": "Led regional branch to record-breaking sales numbers for three consecutive quarters. Established new client accounts."
        },
        {
            "candidate_id": "CAN-044",
            "name": "Nancy Drew",
            "current_title": "Junior Business Analyst",
            "years_experience": "1.5",
            "skills": "Excel, SQL, PowerBI, Business Analysis, Agile, Scrum, Communication",
            "education": "BS in Finance - Rutgers University",
            "summary": "Detail-oriented junior business analyst. Experienced in gathering requirements, creating user stories, building PowerBI reports, and querying databases using SQL. Strong analytical mindset.",
            "github_url": "https://github.com/ndrew-analyst",
            "linkedin_activity": "Posts updates about her journey learning advanced SQL and Excel dashboard tips.",
            "projects": "Built interactive PowerBI sales dashboard used by executive team. Translated business requests to developer specs."
        },
        {
            "candidate_id": "CAN-045",
            "name": "Oscar Martinez",
            "current_title": "Senior Accountant",
            "years_experience": "8.0",
            "skills": "Accounting, Excel, Financial Analysis, Tax Compliance, Bookkeeping, SAP",
            "education": "BS in Accounting - University of Scranton",
            "summary": "Certified Public Accountant with 8 years of experience. Expert in corporate accounting, financial analysis, tax compliance, ledger audits, and advanced financial modeling in Excel.",
            "github_url": "https://github.com/omartinez-cpa",
            "linkedin_activity": "Rarely active. Shares updates about tax regulations and financial audit best practices.",
            "projects": "Managed year-end corporate tax compliance audits, saving $30k in filing fees. Designed automated accounting ledger."
        },
        {
            "candidate_id": "CAN-046",
            "name": "Peter Parker",
            "current_title": "Freelance Photographer",
            "years_experience": "3.0",
            "skills": "Photography, Photo Editing, Photoshop, Social Media, Creative Writing",
            "education": "BS in Biophysics - Empire State University",
            "summary": "Freelance photographer specializing in action photography, photojournalism, and digital photo editing using Adobe Photoshop. Passionate about storytelling and visual media.",
            "github_url": "https://github.com/pparker-photo",
            "linkedin_activity": "Active. Posts high-resolution photos, camera gear reviews, and tips on street photography.",
            "projects": "Photographed multiple local sporting and cultural events for national publications. Built digital media portfolio site."
        },
        {
            "candidate_id": "CAN-047",
            "name": "Quinn Fabray",
            "current_title": "Social Media Coordinator",
            "years_experience": "2.0",
            "skills": "Social Media, Content Creation, Instagram, TikTok, Canva, Copywriting",
            "education": "BA in Marketing - Ohio State University",
            "summary": "Creative marketing coordinator focusing on social media management, organic audience growth, TikTok content creation, and brand graphics in Canva. Strong digital marketing instincts.",
            "github_url": "https://github.com/qfabray-mktg",
            "linkedin_activity": "Highly active. Writes about TikTok marketing trends, video engagement strategies, and organic reach. 8k followers.",
            "projects": "Grew company Instagram account from 1k to 15k organic followers in 6 months. Created viral TikTok campaigns."
        },
        {
            "candidate_id": "CAN-048",
            "name": "Rachel Green",
            "current_title": "Fashion Merchandiser / Buyer",
            "years_experience": "5.0",
            "skills": "Fashion Merchandising, Buying, Inventory Management, Trend Analysis, Excel",
            "education": "BA in Art History - NYU",
            "summary": "Experienced fashion merchandiser and buyer with 5 years in retail. Skilled in inventory management, analyzing consumer trends, catalog curation, and Excel spreadsheets.",
            "github_url": "https://github.com/rgreen-fashion",
            "linkedin_activity": "Writes about retail fashion trends, luxury catalog strategies, and seasonal buying benchmarks.",
            "projects": "Managed $500k inventory buy for seasonal rollout, exceeding sales targets by 12%. Designed retail layout concept."
        },
        {
            "candidate_id": "CAN-049",
            "name": "Steve Rogers",
            "current_title": "Security Supervisor / Logistics Lead",
            "years_experience": "9.0",
            "skills": "Logistics, Security Operations, Leadership, Emergency Response, Excel",
            "education": "High School Diploma",
            "summary": "Dedicated supervisor with 9 years of experience leading security teams, crisis management response, and logistics operations. Known for leadership, integrity, and operational execution.",
            "github_url": "https://github.com/srogers-logistics",
            "linkedin_activity": "Rarely posts. Shares links to security training certifications and operational leadership books.",
            "projects": "Supervised logistics and site security for regional industrial facility with zero safety incidents over 4 years."
        },
        {
            "candidate_id": "CAN-050",
            "name": "Tony Stark",
            "current_title": "Embedded Systems Hobbyist / Junior HW Engineer",
            "years_experience": "2.0",
            "skills": "C, C++, Arduino, Embedded Systems, Circuit Design, Basic Python, Git",
            "education": "BS in Electrical Engineering - MIT",
            "summary": "EE graduate and embedded systems enthusiast. Skilled in C, microcontroller programming (Arduino, STM32), and basic circuit board design. Eager to learn high-performance hardware-software co-design.",
            "github_url": "https://github.com/tstark-embedded",
            "linkedin_activity": "Shares videos of custom hardware builds, robotics sensors, and soldering workshops.",
            "projects": "Built a custom home-automation hub using Raspberry Pi and C++. Designed multi-layered sensor shield PCB."
        }
    ]

    os.makedirs("data", exist_ok=True)
    with open("data/candidates.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "candidate_id", "name", "current_title", "years_experience", 
            "skills", "education", "summary", "github_url", "linkedin_activity", "projects"
        ])
        writer.writeheader()
        for cand in candidates:
            writer.writerow(cand)
    print(f"Generated data/candidates.csv with {len(candidates)} candidates.")

if __name__ == "__main__":
    generate_dataset()
