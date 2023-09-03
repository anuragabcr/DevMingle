// Invoke Functions Call on Document Loaded

document.addEventListener('DOMContentLoaded', function () {
//  hljs.highlightAll();
    let alertWrapper = document.querySelector('.alert')

    alertWrapper.addEventListener("click", function(event) {
        let target = event.target
        if(target.classList.contains('alert__close')) {
            alertWrapper.style.display = 'none'
            alert("Button clicked!");
        }
    });
});