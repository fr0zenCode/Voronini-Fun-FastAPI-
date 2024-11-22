const userIdFromHTML = document.getElementById("userData");
const currentUserId = userIdFromHTML.dataset.id;

let offset = 0;
const limit = 10;

// Функция притормаживания
function throttle(callee, timeout) {
    let timer = null

    return function perform(...args) {
        if (timer) return
        timer = setTimeout(() => {
            callee(...args)
            clearTimeout(timer)
            timer = null
        }, timeout)
    }
}

// Функция обработки прокрутки из Гида по ЖС
function checkPosition() {
    if (window.innerHeight + 100 + window.scrollY >= document.body.scrollHeight) {
        loadMorePosts();
    };
}

window.addEventListener('scroll', throttle(checkPosition, 250));
window.addEventListener('resize', throttle(checkPosition, 250));



// Функция для загрузки дополнительных постов
async function loadMorePosts() {

    try {
        offset += limit;
        const response = await fetch(`/feed/load-more-posts?offset=${offset}&limit=${limit}`);
        const data = await response.json();

        const postsZone = document.querySelector('.posts');

        data.posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.className = 'post';
            postElement.id = `post-${post.post_id}`;

            // Проверка на авторство поста для отображения кнопки "Удалить"
            let deleteButton = '';
            if (post.author_id === currentUserId) {
                deleteButton = `<button onclick="delete_post(${post.post_id})" class="delete-post-btn">Удалить</button>`;
            }

            postElement.innerHTML = `
                
                        <div class="post-content">

                            <div class="post-header">
                                <div class="avatar"></div>
                                <span class="author"><b>${post.author_username}</b></span>
                                <span class="time">${post.created_at}</span>
                            </div>

                            <div class="post-text">
                                ${post.text}
                            </div>
                        
                            ${deleteButton}

                        </div>
    
                    `;

            postsZone.appendChild(postElement);

        });

    } catch (error) {
        alert("Ошибка!!!!")
        console.error("Ошибка при загрузке постов:", error);
    }

}

async function send_post() {
    const text = document.getElementById("new-post-text").value;
    if (text == "") {
        return
    }
    const response = await fetch("/feed/new-post", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            author: "Undefined",
            text: text
        })
    })
    if (response.ok) {
        location.reload();
    } else {
        const json = await response.json();
        const res = JSON.parse(json);
        alert(res);
    }

}

async function delete_post(postID) {
    const response = await fetch("/feed/delete-post", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            post_id: postID
        })
    });
    if (response.ok) {
        document.getElementById(postID).remove();
    }
};

function scrollToTop() {
    window.scrollTo({ top: document.getElementById("header"), behavior: 'smooth' });
}
