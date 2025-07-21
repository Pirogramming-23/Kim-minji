function getCSRFToken() {
    const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

// 좋아요 버튼
document.querySelectorAll('.like-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const postDiv = this.closest('.post');
        const postId = postDiv ? postDiv.dataset.postId : null;
        const likeCountSpan = postDiv ? postDiv.querySelector('.like-count') : null;
        const likeIcon = this;

        if (!postId) {
            console.error('postId not found!');
            return;
        }

        fetch('/like/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `post_id=${postId}`
        })
        .then(res => res.json())
        .then(data => {
            if (likeCountSpan) likeCountSpan.textContent = data.like_count;
            if (data.liked) {
                likeIcon.classList.remove('fa-regular');
                likeIcon.classList.add('fa-solid');
            } else {
                likeIcon.classList.remove('fa-solid');
                likeIcon.classList.add('fa-regular');
            }
        })
        .catch(err => console.error('Like error:', err));
    });
});

// 댓글 작성
document.querySelectorAll('.add-comment-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const postDiv = this.closest('.post');
        const postId = postDiv ? postDiv.dataset.postId : null;
        const commentsDiv = postDiv ? postDiv.querySelector('.post-comments') : null;
        const content = this.querySelector('input[name="content"]').value;

        if (!postId) {
            console.error('postId not found for comment!');
            return;
        }

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
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.dataset.commentId = data.comment_id;
            newComment.innerHTML = `<strong>${data.username}</strong> ${data.content} <button class="delete-comment-btn" data-comment-id="${data.comment_id}">❌</button>`;
            if (commentsDiv) commentsDiv.appendChild(newComment);
            this.querySelector('input[name="content"]').value = '';
        })
        .catch(err => console.error('Add comment error:', err));
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
        })
        .catch(err => console.error('Delete comment error:', err));
    }
});

document.querySelectorAll('.post-slider').forEach(slider => {
    const track = slider.querySelector('.slider-track');
    const images = track.querySelectorAll('img');
    let currentIndex = 0;

    const updateSlider = () => {
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
    };

    slider.querySelector('.prev-btn')?.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateSlider();
    });

    slider.querySelector('.next-btn')?.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % images.length;
        updateSlider();
    });
});