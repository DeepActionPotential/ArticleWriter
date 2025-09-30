from crewai import Crew, Task
from agents.agents import (
    WritingStyleDecisionAgent,
    ArticleStructureAgent,
    SearchAndScrapeAgent,
    WriterAgent
)
from schemas.agents_schemas import (
    WritingStyleInput,
    WritingStyleOutput,
    ArticleStructureInput,
    ArticleStructureOutput,
    SearchAndScrapeOutput,
    ArticleContent
)

from utils import filter_article

import os

class ArticleMaker:
    def __init__(self, llm):
        self.llm = llm
        self.writing_style_agent = WritingStyleDecisionAgent(llm=llm).make_agent()
        self.article_structure_agent = ArticleStructureAgent(llm=llm).make_agent()
        self.search_scrape_agent = SearchAndScrapeAgent(llm=llm).make_agent()
        self.writer_agent = WriterAgent(llm=llm).make_agent()

    def make(self, topic, article_writing_task_description:str = None):
        

        # Define tasks
        search_scrape_task = Task(
            description=(
                f"Use the keyword '{topic}' to search online and extract content from the top 5 most credible and high-traffic sources, prioritize recent articles or official sites, and summarize key points in each. Ensure you capture diverse perspectives, quotes, and data examples where available."
            ),
            expected_output=(
                "A list of cleaned, structured summaries from the top 5 URLs, each including page title, URL, publication date, author (if available), key quotes or data, and a short paragraph contextualizing its relevance."
            ),
            input_pydantic=None,
            output_pydantic=SearchAndScrapeOutput,
            agent=self.search_scrape_agent
        )

        writing_style_task = Task(
            description=(
                f"Analyze the topic '{topic}' and determine the most appropriate writing style for a blog post that reads like a knowledgeable human expert. Consider audience expertise, tone (e.g., witty, authoritative, conversational), structure, and emotional engagement."
            ),
            expected_output=(
                "A detailed WritingStyleOutput with fields: style (e.g., 'witty conversational tutorial'), and a reason explaining how it aligns with the topic, audience needs, and desired emotional impact."
            ),
            input_pydantic=WritingStyleInput,
            output_pydantic=WritingStyleOutput,
            agent=self.writing_style_agent
        )

        article_structure_task = Task(
            description=(
                "Using the scraped summaries and chosen writing style, design a well-structured blog article outline. Include 5–7 sections with catchy, concise titles and specify for each: minimum word count, key bullet points or subsections, whether code examples or visuals are needed, and tone reminders."
            ),
            expected_output=(
                "An ArticleStructureOutput containing a list of sections; for each: title, min_word_count, bullet_points, code_or_visual flag, and brief notes on tone or style cues."
            ),
            input_pydantic=ArticleStructureInput,
            output_pydantic=ArticleStructureOutput,
            agent=self.article_structure_agent,
            context=[writing_style_task, search_scrape_task]
        )

        article_writing_task_description = article_writing_task_description or (
            "Write a complete blog article in markdown, using the provided outline and scraped content. Adopt a fun yet informative tone, with engaging hooks, concise technical explanations, and humanoid section titles. Include code blocks where specified, relevant visuals (as markdown image links), real-world analogies, and short, snappy sentences."
        )

        article_writing_task = Task(
            description=article_writing_task_description,
            expected_output=(
                "A fully formatted Markdown article: sections with level-2 headings, subheadings/bullets, `code snippets` as needed, embedded image placeholders with REAL urls, NOT examples urls, and an engaging narrative voice that feels human. Ensure each section meets its specified word count."
            ),
            input_pydantic=ArticleStructureOutput,
            agent=self.writer_agent,
            context=[article_structure_task, search_scrape_task],
            output_file='temp.txt'
        )

        crew = Crew(
            agents=[
                self.search_scrape_agent,
                self.writing_style_agent,
                self.article_structure_agent,
                self.writer_agent
            ],
            tasks=[
                search_scrape_task,
                writing_style_task,
                article_structure_task,
                article_writing_task
            ],
            verbose=True,
            memory=True,
            embedder={
                "provider": "google",
                "config": {
                    "api_key": "<YOUR_API_KEY>",
                    "model": "text-embedding-004"
                }
            }
        )

        crew.kickoff(inputs={"topic": topic})
        
        with open('./temp.txt', 'r') as file:
            content = filter_article(file.read())
        
        os.remove('./temp.txt')  # Clean up temporary file

        return content