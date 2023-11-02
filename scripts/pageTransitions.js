const pages = document.querySelectorAll(".page");
let t = -100;

slide = (page) => {
    switch (page) {
        case 'user':
            t = 0;
            break;
        case 'main':
            t = -100;
            break;
        case 'global':
            t = -200;
            break;
    }
    pages.forEach(
        page => (page.style.transform = `translateX(${t}%)`)
    );
}