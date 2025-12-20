from googleapiclient.errors import HttpError
from jayden_marketing_assistant.tools.auth_marketing import get_blogger_service

def get_blog_id(service):
    """Helper to find the primary blog ID."""
    # User might have multiple blogs. We'll pick the first one or search by name logic later.
    try:
        # 'self' refers to the authenticated user's blogs
        blogs = service.blogs().listByUser(userId='self').execute()
        items = blogs.get('items', [])
        if not items:
            return None
        return items[0]['id']
    except Exception:
        return None

def post_to_blogger(title: str, content: str, is_draft: bool = True) -> str:
    """Creates a post on the user's Blogger account.
    is_draft: If True, saves as draft. If False, publishes immediately.
    """
    try:
        service = get_blogger_service()
        blog_id = get_blog_id(service)
        
        if not blog_id:
            return "Error: No Blogger blog found for this account."

        body = {
            'kind': 'blogger#post',
            'blog': {'id': blog_id},
            'title': title,
            'content': content
        }
        
        # insert(blogId, body, isDraft=bool)
        posts = service.posts()
        result = posts.insert(blogId=blog_id, body=body, isDraft=is_draft).execute()
        
        status = "DRAFT" if is_draft else "PUBLISHED"
        return f"Blogger Post '{result['title']}' created ({status}). URL: {result.get('url', 'N/A')}"

    except HttpError as error:
        return f'An error occurred posting to Blogger: {error}'
