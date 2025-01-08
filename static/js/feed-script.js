const userIdFromHTML = document.getElementById("userData");
const currentUserId = userIdFromHTML.dataset.id;

const localStorageText = localStorage.getItem("text");
if(localStorageText !== null){
    const textarea = document.getElementById("new-post-text");
    textarea.textContent = localStorageText;
    localStorage.removeItem("text");
}


window.addEventListener("beforeunload", function (e) {
    const text = document.getElementById("new-post-text").value;
    console.log("Не понял");
    if (text.trim() !== "") {
        localStorage.setItem("text", text);
    }
});



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

async function deletePost(postID) {
    const response = await fetch("/feed/delete-post", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            post_id: postID
        })
    });
    console.log(response);
    if (response.ok) {
        document.getElementById(postID).remove();
    }else{
        console.log("Охуел что ли?");
    }
};


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
            postElement.id = `${post.post_id}`;

            // Проверка на авторство поста для отображения кнопки "Удалить"
            let deleteButton = '';
            if (post.author_id === currentUserId) {
                deleteButton = `<button class="delete-post-btn" data-post-id="${post.post_id}">Удалить</button>`;
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

                            <div class="post-comment">
                                <input type="text" placeholder="Введите комментарий...">
                                <button type="button" class="send-comment-btn" id="send-comment-btn">Отправить</button>
                            </div>

                        </div>
    
                    `;

            postsZone.appendChild(postElement);
            
        });

    } catch (error) {
        alert("Ошибка!!!!")
        console.error("Ошибка при загрузке постов:", error);
    }

};

async function send_post() {
    
    const text = document.getElementById("new-post-text").value;
    const errorLabel = document.getElementById("error-lbl");

    if (text == "") {
        errorLabel.textContent = "Пост не может быть пустым!";
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
        errorLabel.textContent = "";
        localStorage.removeItem("text");
        document.getElementById("new-post-text").textContent = "";
    }else{
        errorLabel.textContent = "Посты можно размещать не чаще, чем раз в 5 минут!";
    }
}


async function sendComment(dataForBackend){

    const response = await fetch("http://127.0.0.1:8005/comments/add-comment", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: dataForBackend
    });




    console.log(dataForBackend);
}


const postsZone = document.querySelector('.posts');

// Делегируем обработку кликов на контейнер
postsZone.addEventListener('click', async (event) => {


    if (event.target.classList.contains("send-comment-btn")) {
        const postId = event.target.getAttribute('data-post-id');
        const inputElement = document.querySelector(`input[data-post-id="${postId}"]`);
        if(inputElement.value){
            commentText = inputElement.value;
            console.log("Отправляем комментарий с текстом " + commentText);
            
            const commentDataForBackend = JSON.stringify({
                post_id: postId, 
                author_id: currentUserId, 
                comment_text: commentText
            });
            
            sendComment(commentDataForBackend);
        }
        
    };


    if (event.target.classList.contains('delete-post-btn')) {
        const postId = event.target.getAttribute('data-post-id');
        try {
            await deletePost(postId); // Здесь вызывается функция удаления поста
            // Удаляем пост из DOM
            
        } catch (error) {
            console.error("Ошибка при удалении поста:", error);
        }
    }
});

const refreshPostsButton = document.getElementById("refresh-btn");

async function refreshPosts(){
    const text = document.getElementById("new-post-text").value;
    if(text != ""){
        localStorage.setItem("text", text);
    }
    document.location.reload();
}


refreshPostsButton.addEventListener('click', function(e){
    refreshPosts();
})







// postsZone.addEventListener('click', async (event) => {
//     if (event.target.classList.contains('delete-post-btn')) {
//         const postId = event.target.getAttribute('data-post-id');
//         try {
//             await deletePost(postId); // Здесь вызывается функция удаления поста
//             // Удаляем пост из DOM
            
//         } catch (error) {
//             console.error("Ошибка при удалении поста:", error);
//         }
//     }
// });




