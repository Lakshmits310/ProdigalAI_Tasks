# Project Summary – 7 Practical Tasks

This report highlights seven hands-on automation and data engineering tasks completed using modern tools and technologies. Each task focuses on solving a real-world problem using scalable, modular, and automation-friendly approaches.

## 🧠 Task 1: ML + LLM Pipeline Orchestration
Built a complete workflow using Airflow, MLflow, Spark, and Docker to orchestrate machine learning and large language model tasks. This setup automates data processing, model tracking, and inference scheduling in a modular way.

## 🛡 Task 2: Role-Based Access Control System (RBAC)
Designed a secure RBAC system with organizations, departments, user roles (Admin, Manager, Contributor, Viewer), and guests. The system ensures proper access levels to files and actions, and supports multi-user collaboration.

## ⚙️ Task 3: Kafka-Based High-Throughput API Ingestion
Created a high-performance API ingestion pipeline using Kafka and Flask. Simulated 10,000+ API requests being sent and processed in real time. Ensured reliability through Kafka consumers, retry logic, and structured logging.

## ☁️ Task 4: Kubernetes Pod Scaling with HPA
Deployed a Flask app in Kubernetes and implemented auto-scaling using Horizontal Pod Autoscaler. The app scaled automatically based on CPU usage, demonstrating cloud-native microservice management in action.

## 📈 Task 5: Binance WebSocket Price Tracker
Streamed live prices of Bitcoin and Ethereum using Binance WebSocket and stored them precisely in a PostgreSQL database. Built a web interface to query latest prices, historical prices, and high/low ranges per minute.

## 📰 Task 6: Web Scraper + Dashboard (Articles & Schemes)
Scraped article data from Microsoft’s Research blog and government schemes from MyScheme portal. Summarized and visualized the results through a simple web dashboard that shows insights, summaries, and downloadable data.

## 🤖 Task 7: Web3 Newsletter Bot with LangChain
Built an automated Telegram newsletter bot that:
* Scrapes articles from 5 top Web3 news sites
* Deduplicates similar news
* Summarizes key content using LLMs (LangChain + OpenAI)
* Sends a clean daily digest to Telegram

