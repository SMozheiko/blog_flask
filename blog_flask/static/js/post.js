"use strict";
window.addEventListener('load', () => {
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
    })
})