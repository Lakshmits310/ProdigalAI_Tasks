from typing import List, Dict
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

class Summarizer:
    def __init__(self):
        self.llm = Ollama(model="mistral")
        self.prompt = PromptTemplate(
            input_variables=["title", "source"],
            template="""
Create a clear and concise 2–3 sentence summary of the following Web3 news article.
Write professionally and avoid fluff.

Title: {title}
Source: {source}

Summary:
"""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def summarize_article(self, article: Dict) -> str:
        try:
            response = self.chain.invoke({
                'title': article['title'],
                'source': article['source']
            })
            summary = response.get("text", "").strip()
            print("🔍 Raw LLM response:", summary)

            if not summary or len(summary.split()) < 5:
                raise ValueError("Too short or empty summary")

            return summary

        except Exception as e:
            print(f"❌ Error summarizing article: {e}")
            return "Summary unavailable"

    def summarize_articles(self, articles: List[Dict]) -> List[Dict]:
        summarized = []
        for article in articles:
            article['summary'] = self.summarize_article(article)
            summarized.append(article)
        return summarized
