from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .services import ask_shopmind_ai


@require_POST
def chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if not user_message:
            return JsonResponse(
                {"error": "Please enter a message."},
                status=400
            )

        reply = ask_shopmind_ai(user_message)

        return JsonResponse({
            "reply": reply
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid request."},
            status=400
        )

    except Exception as e:
     print("SHOPMIND AI ERROR:", repr(e))

     return JsonResponse(
          {"error": "AI assistant is temporarily unavailable."},
          status=500
     )