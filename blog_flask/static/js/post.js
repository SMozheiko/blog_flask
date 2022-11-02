"use strict";
window.addEventListener('load', async () => {
    let deleteComments = document.querySelectorAll('.delete-comment');
    deleteComments.forEach((el) => {
        el.addEventListener('click', event => {
            const modal = document.querySelector('#delete-comment-modal');
            const form = document.querySelector('#delete-comment-form');
            form.action = event.target.dataset.action;
            modal.style.display = 'block';
            modal.addEventListener('click', event1 => {
                if (event1.target.tagName === 'BUTTON') {
                    modal.style.display = 'none';
                }
            })
        })
    });
    let like = document.querySelector('.heart');
    like.addEventListener('click', async (event) => {
        const request = new Request(
            event.target.dataset.url,
            {
                method: 'POST'
            }
        );
        const response = await fetch(request).then(
            result => result.json()
        ).catch(error => console.log(error));
        if (response.status === 'ok') {
            event.target.classList.toggle('heart-red');
            event.target.nextElementSibling.innerText = response.likes;
        }
    })
})