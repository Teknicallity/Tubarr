$(document).ready(function () {
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getUserInputUrl() {
    return $(this).find('input').val()
}

const url_input = document.querySelector('#url_input')
const content_info = document.querySelector('#content_info');
const confirmation_input = document.querySelector('#confirmation_input')
let url
document.querySelector('#content_input_form').addEventListener('submit', (event) => {
    event.preventDefault()

    // clean up input
    url = url_input.value.trim();
    if (url.length === 0) {
        return;
    }

    // display url back to user
    url_input.value = ''
    const urlDisplay = document.getElementById('input_url_display')
    urlDisplay.innerText = `${url}`

    content_info.innerHTML = ''

    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: new URLSearchParams({
            'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'url': url
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const info = data.initial_info;

            let errorDisplay;
            if (data.error !== '') {
                errorDisplay = document.getElementById('error_display')
                errorDisplay.innerText = `${data.error}`
                return
            } else {
                if (info.type === 'video') {
                    content_info.innerHTML = `
                    <div id="video_info">
                        <img class="thumbnail" src=${info.thumbnail_url} alt="Video Thumbnail"> 
                        <p class="title">${info.video_title}</p>
                        <p class="channel">${info.channel_name}</p>
                        <p class="date">${info.upload_date}</p>
                        <p class="description">${info.video_description}</p>
                    </div>
                    `;
                } else if (info.type === 'playlist') {
                    content_info.innerHTML = `
                    <div id="playlist_info">
                        <img class="thumbnail" src=${info.thumbnail_url} alt="Thumbnail">
                        <p class="title">${info.playlist_name}</p>
                        <img class="profile-pic" src='' alt="Channel Picture">
                        <div class="info">
                            <p class="channel">${info.channel_name}</p>
                            <p class="video-count"># of videos: ${info.playlist_entry_count}</p>
                        </div>
                    </div>
                    `
                } else if (info.type === 'channel') {
                    content_info.innerHTML = `
                    <div id="channel_info">
                        <p class="title"></p>
                        <img class="profile-pic" src="" alt="Channel Picture">
                        <div class="info">
                            <p class="video-count"></p>
                        </div>
                    </div>
                    `
                }

                confirmation_input.innerHTML = `
                    <input type="text" id="url_display" name="url" value="${url}" readonly>
                    <label class="confirmation_text">Download?</label>
                    <button type="submit">Yes</button>
                    <button type="reset">No</button>
                `
            }


        })
})

// document.querySelector('#confirmation_form').addEventListener('submit', (event) => {
//     event.preventDefault()
//     fetch('/download', {
//         method: 'POST',
//         headers: {'Content-Type': 'application/x-www-form-urlencoded'},
//         body: new URLSearchParams({
//             'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
//             'url': url
//         })
//     })
// })