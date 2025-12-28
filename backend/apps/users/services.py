from .models import HistorySearch
from django.db.models import QuerySet

def save_user_search_history(user, query, results):
    if not user.is_authenticated or not query:
        return
    count = 0
    if isinstance(results, QuerySet):
        count = results.count()
    elif isinstance(results, list):
        count = len(results)
    try:
        HistorySearch.objects.create(
            user=user,
            content=query,
            result_count=count
        )
    except Exception as e:
        print(f"Error logging search: {e}")