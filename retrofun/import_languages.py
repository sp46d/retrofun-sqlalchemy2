import os
import csv
from sqlalchemy import select, delete
from retrofun.db import Session
from retrofun.models import BlogArticle, Language
from datetime import datetime


def main():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'articles.csv')

    with Session() as session:
        with session.begin():
            all_articles: dict[str, BlogArticle | None] = {}
            all_languages: dict[str, Language | None] = {}
            
            with open(data_path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    article = all_articles.get(row['title'])
                    if article is None:
                        article = session.scalar(select(BlogArticle).where(BlogArticle.title == row['title']))
                        all_articles[row['title']] = article

                    language = all_languages.get(row['language'])
                    if language is None:
                        language = session.scalar(select(Language).where(Language.name == row['language']))
                        if language is None:
                            language = Language(name=row['language'])
                            session.add(language)
                        all_languages[row['language']] = language
                    article.language = language
                    
                    if row['translation_of'] and article is not None:
                        translation_of = all_articles.get(row['translation_of'])
                        if translation_of is None:
                            translation_of = session.scalar(select(BlogArticle).where(BlogArticle.title == row['translation_of']))
                            all_articles[row['translation_of']] = translation_of
                        article.translation_of = translation_of
                    
                    
if __name__ == '__main__':
    main()
                            
        
                    
                        
                    