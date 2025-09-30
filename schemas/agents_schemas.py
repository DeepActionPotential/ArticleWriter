from pydantic import BaseModel, Field
from typing import List



class WritingStyleInput(BaseModel):
    topic: str = Field(
        description="The main subject of the blog post, typically an AI-related topic like 'transformer architecture' or 'ethical risks of AGI'."
    )




class WritingStyleOutput(BaseModel):
    topic: str = Field(description="The topic of the article.")
    style: str = Field(
        description=(
            "A natural-language description of the most appropriate writing style "
            "for this topic. Examples: 'formal and technical', 'opinionated editorial', "
            "'informal tutorial style', 'reflective essay', 'clear explanatory tone', etc."
        )
    )
    reason: str = Field(
        description="A concise explanation of why this writing style is appropriate for the given topic."
    )



class SearchResult(BaseModel):
    url: str = Field(description="The URL of the search result.")
    content: str = Field(description="The visible extracted text content from the page.")


class SearchAndScrapeOutput(BaseModel):
    keyword: str = Field(description="The original keyword used for searching.")
    urls: List[str] = Field(description="A list of URLs returned from the search.")
    results: List[SearchResult] = Field(description="A list of search results with URLs and scraped content.")


class ArticleStructureInput(BaseModel):
    topic: str = Field(description="The main subject of the blog post.")
    style: WritingStyleOutput = Field(
        description="The selected writing style and reasoning for the article.")
    
    scraped_content: SearchAndScrapeOutput = Field(
        description="The content scraped from the top search results, used to inform the article structure."
    )
    



class ArticleSection(BaseModel):
    title: str = Field(description="The title of the section.")
    length: str = Field(description="The minimum length (in words) that the section should cover, e.g., 'at least 500 words'.")
    subsections: List[str] = Field(
        default_factory=list, description="Optional subsections within the section."
    )
    code_examples: str = Field(
        description="Optional code examples or explanations required in this section. Specify the type of code if applicable."
    )

    code_explanations: str = Field(
        description="Optional explanations for any code examples provided in this section.")



class ArticleStructureOutput(BaseModel):
    sections: List[ArticleSection] = Field(
        description="A list of sections that make up the article, each with a title, content, subsections, and code requirements.")
    tone: str = Field(description="A natural-language description of the tone the article should maintain.")
    writing_tips: List[str] = Field(description="Suggestions on how to maintain the selected tone and style throughout the article.")



class ArticleContent(BaseModel):
    
    article_markdown: str = Field(description="The complete article formatted in Markdown.")