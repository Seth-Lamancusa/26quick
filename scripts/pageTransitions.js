const pages = document.querySelectorAll(".page");
let translate = -100;

slide = (page) => {
    switch (page) {
        case 'user':
            translate = 0;
            break;
        case 'main':
            translate = -100;
            break;
        case 'global':
            translate = -200;
            break;
    }
    pages.forEach(
        page => (page.style.transform = `translateX(${translate}%)`)
    );
}