let elem = document.getElementById('comment-update')
console.log(elem)
elem.addEventListener("click", evt => {
    let div = document.getElementById('comment-div');
    div.style.display = (div.style.display === 'none') ? '' : 'none'
})