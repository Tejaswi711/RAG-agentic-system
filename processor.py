from typing import List, Dict

def process_documents(raw_docs: List[Dict]) -> List[Dict]:
    """Transform API data into database-ready format"""
    processed = []
    for doc in raw_docs:
        processed.append({
            'document_number': doc['document_number'],
            'title': doc['title'],
            'publication_date': doc['publication_date'],
            'type': doc['type'],
            'agencies': ', '.join([a['name'] for a in doc['agencies']]),
            'summary': doc.get('abstract', doc['title']),
            'full_text_url': doc['full_text_url']
        })
    return processed