from fastapi import APIRouter

comments_router = APIRouter(prefix="/comments")


@comments_router.post("/add-comment")
async def add_comment(post_id, comment):
    ...


@comments_router.post("/delete-comment")
async def delete_comment(comment_id):
    ...


@comments_router.get("/{post_id}")
def get_comment_for_post(post_id):
    return {"message": post_id}
