from services.supabase import supabase

def create_notification(user_id: str, type: str, message: str, reference_id: str = None, meta_data: dict = None):
    """
    Utility function to create an in-app notification for a user.
    """
    # Insert notification record into Supabase
    data = {
        "user_id": user_id,
        "type": type,
        "message": message,
        "reference_id": reference_id,
        "meta_data": meta_data,
        "is_read": False
    }
    try:
        supabase.table("notifications").insert(data).execute()
        
        # Here we could also trigger a Socket.io event for real-time delivery
        # Example: await sio.emit('new_notification', data, room=user_id)
        # Note: If this function is sync, emitting requires careful handling of the event loop
    except Exception as e:
        print(f"Failed to create notification: {e}")
