@router.get("/list")
def list_records(user_id: str = Query(..., description="User ID to fetch records for"), request: Request = None):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing authorization token")

    try:
        supabase.auth.set_auth(token.replace("Bearer ", ""))
        res = supabase.table("records").select("*").eq("user_id", user_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"data": res.data}
