document.addEventListener('DOMContentLoaded', function() {
    // 좋아요 버튼 클릭
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const postId = this.dataset.postId;
            const likeCountSpan = this.querySelector('.like-count');
            fetch('/like/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `post_id=${postId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked !== undefined) {
                    likeCountSpan.innerText = data.like_count;
                }
            });
        });
    });

    // 댓글 작성
    document.querySelectorAll('.add-comment-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const content = this.querySelector('input[name="content"]').value;

            fetch('/comment/add/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `post_id=${postId}&content=${encodeURIComponent(content)}`
            })
            .then(response => response.json())
            .then(data => {
                const commentsDiv = this.previousElementSibling;
                const newComment = document.createElement('div');
                newComment.classList.add('comment');
                newComment.dataset.commentId = data.comment_id;
                newComment.innerHTML = `<strong>${data.username}</strong>: ${data.content} <button class="delete-comment-btn button is-small is-danger is-light" data-comment-id="${data.comment_id}">❌</button>`;
                commentsDiv.appendChild(newComment);
                this.querySelector('input[name="content"]').value = '';
            });
        });
    });

    // 댓글 삭제 (이벤트 위임)
    document.getElementById('post-list').addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-comment-btn')) {
            const commentId = e.target.dataset.commentId;
            fetch('/comment/delete/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `comment_id=${commentId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.deleted) {
                    e.target.closest('.comment').remove();
                }
            });
        }
    });

    function getCSRFToken() {
        const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }
});