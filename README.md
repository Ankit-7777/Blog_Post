# Django Blog Post Application

## Summary

This is a **Django REST framework** based blog post application that allows users to create, update, edit, and share their blog posts. Users can upload media content (images and videos), comment on posts, like comments, tag posts, and perform full-text searches. The application features user authentication and authorization to ensure that only authorized users can perform specific actions.

The application is designed to provide a seamless experience for users looking to express themselves through blog posts while engaging with the community via comments and likes.

## Features

### 1. Post Management (CRUD)

- **Create**: Users can create new blog posts with titles, content, images, and videos.
- **Read**: Users can view a list of all posts or the details of a specific post.
- **Update**: Users can edit their own posts.
- **Delete**: Users can delete their own posts.

### 2. Media Upload

- Users can upload **image** and **video** content in their blog posts, allowing for rich multimedia experiences.

### 3. Commenting

- Authenticated users can add comments to posts, fostering interaction and discussion.

### 4. Comment Liking

- Users can like and unlike comments on posts, enabling them to express appreciation for specific comments.

### 5. Tagging

- Blog posts can be tagged, and users can filter posts by tags to discover related content easily.

### 6. Search Functionality

- Users can perform **full-text search** on post titles and content, making it easier to find specific posts.

### 7. User Authentication

- Users can **sign up**, **log in**, and manage their profiles. This includes functionality for password management and account verification.

### 8. Post Sharing via Email

- Users can share blog posts via email, enhancing the reach of their content.

### 9. Pagination

- Blog posts are paginated, displaying a limited number of posts per page (e.g., 5 posts), improving load times and user experience.

### 10. User Authorization

- Only the **post author** can edit or delete their posts, ensuring that content ownership is respected.

### 11. Video Processing

- Video files are processed using `InMemoryUploadedFile` and `VideoFileClip` to handle video uploads and ensure compatibility.

## Requirements

To run this project, you will need the following dependencies:

```bash
asgiref==3.8.1
certifi==2024.8.30
charset-normalizer==3.3.2
colorama==0.4.6
decorator==4.4.2
Django==5.1.1
django-taggit==6.1.0
idna==3.10
imageio==2.35.1
imageio-ffmpeg==0.5.1
moviepy==1.0.3
mysqlclient==2.2.4
numpy==2.1.1
pillow==10.4.0
proglog==0.1.10
requests==2.32.3
setuptools==75.1.0
sqlparse==0.5.1
tqdm==4.66.5
tzdata==2024.2
urllib3==2.2.3
Python==3.12.5



## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ankit-7777/Blog_Post.git
   cd Blog_Post


2. Create a virtual environment and activate it:
   python -m venv myenv
   source myenv/bin/activate and  On Windows: myenv\Scripts\activate

3. Install the dependencies:
   pip install -r requirements.txt

4. Apply migrations:
   python manage.py migrate

5. Run the development server:
   python manage.py runserver


## API Endpoints

/signup/ : User signup page.
/accounts/profile/ : User profile page.
/logout/ : Log out the user.
/ : Homepage listing posts.
/post/new/ : Create a new post.
/post/<int:pk>/ : View the details of a post.
/post/<int:pk>/edit/ : Update an existing post.
/post/<int:pk>/delete/ : Delete a post.
/post/<int:pk>/share/ : Share a post via email.
/post/<int:pk>/comment/ : Add a comment to a post.
/comment/<int:pk>/like/ : Like or unlike a comment.
/search/ : Search for posts.
