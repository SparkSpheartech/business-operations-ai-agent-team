import os
import requests
import json

def post_to_facebook(content: str) -> str:
    """Posts content to Facebook Page (via Business Suite logic).
    Uses 'FACEBOOK_ACCESS_TOKEN' from .env.
    Attempts to find a Page linked to the user and post there.
    """
    user_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
    
    if not user_token:
        return "Action Failed: No FACEBOOK_ACCESS_TOKEN found in .env."
    
    # 1. Fetch Pages this user manages
    try:
        pages_url = "https://graph.facebook.com/v19.0/me/accounts"
        resp = requests.get(pages_url, params={'access_token': user_token})
        data = resp.json()
        
        if 'error' in data:
            return f"Facebook API Error fetching pages: {data['error']['message']}"
            
        pages = data.get('data', [])
        target_page = None
        target_token = None
        
        if pages:
            # Logic: Prefer 'SparkSphear' if exists, else first page
            for p in pages:
                if 'spark' in p.get('name', '').lower():
                    target_page = p
                    break
            
            if not target_page:
                target_page = pages[0] # Fallback to first
            
            target_token = target_page.get('access_token') # Page Token
            page_id = target_page.get('id')
            page_name = target_page.get('name')
            
            # 2. Post to the Page
            post_url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
            post_resp = requests.post(post_url, params={
                'message': content,
                'access_token': target_token
            })
            post_data = post_resp.json()
            
            if 'id' in post_data:
                return f"Success: Posted to Page '{page_name}'. ID: {post_data['id']}"
            else:
                return f"Error posting to Page '{page_name}': {post_data.get('error', {}).get('message')}"
        
        else:
            # No pages found? Try posting to User Profile as fallback
            # (Note: modern FB API restricts user profile posting, might fail)
            fallback_url = "https://graph.facebook.com/v19.0/me/feed"
            fb_resp = requests.post(fallback_url, params={'message': content, 'access_token': user_token})
            fb_data = fb_resp.json()
            if 'id' in fb_data:
                 return f"Success: Posted to User Profile. ID: {fb_data['id']}"
            return "Failed: No Pages found and User Profile posting failed."

    except Exception as e:
        return f"Network Error posting to Facebook: {e}"

def post_to_instagram(caption: str, image_url: str) -> str:
    return "Instagram posting is currently unimplemented."
