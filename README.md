# Blog_Post_CMS

**CMS API**
This project is an API for a Content Management System (CMS) built to manage users, blog posts, and likes. It includes a RESTful API with endpoints for account management, blog creation, retrieval, updates, deletion, and liking/unliking blogs. The system uses a relational database with three main tables: User, Post, and Like.

**Features**
User account creation, login, update, and deletion.
Blog post creation, retrieval, updating, and deletion with ownership-based access control.
Like/unlike functionality for blog posts.
Token-based authentication for secure access.
Single-query retrieval of posts and their associated likes.

**API Endpoints**
• /accounts [POST]: Create account
• /accounts/login: Perform login and return a token for user authentica-
tion
• /accounts/update [PUT] : Update account
• /accounts/delete [DELETE] : Delete account
/me [GET]: Get information of the logged-in user
• /blog [POST]: Create blog
• /blog [GET]: Get all blogs
• /blog/id [GET]: Get blog details
• /blog/id [PUT]: Update blog
• /blog/id [DELETE]: Delete blog
• /like/<blog_id> [POST]: Like the blog
• /like/<blog_id> [DELETE]: Unlike the blog

